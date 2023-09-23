import re

from Tree.message_analysis.message_analysis import MessageAnalysisProcessing
from command_ls import command_ls_dictionary, command_ls_list
from commands_ls import issuing_directions, choice_conversation, response_text_admin
from command_besed import command_bs_dictionary, command_list
from commands_tg import CommandsTg
from message_handling import processing, processing_new

from Tree import Node
from summer_module.work_ls.work_ls import WorkLs


class SimpleHandler:

    def __init__(self, v, club_id, message, apis, them, create_mongo, collection_bots, document_tokens,
                            url_dj, loop, client=None, tree_questions=None, mongo_manager=None, settings_info=None,
                 is_telegram=False):
        self.v = v
        self.club_id = club_id
        self.message = message
        self.from_id = message["from_id"]
        self.apis = apis
        self.them = them
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.url_dj = url_dj
        self.loop = loop
        self.client = client
        self.tree_questions = tree_questions
        self.mongo_manager = mongo_manager
        self.settings_info = settings_info
        self.is_telegram = is_telegram
        #print("SIMPLE HANDLER", self.tree_questions)
        #print(command_ls_dictionary)
        #self.root = self.tree_distribution_root()
        #print(self.root.children.question)
        #print(command_ls_dictionary)


    async def selection(self, command_list, text, them, is_bs=False):

        for c in command_list:
            flag = False
            flag_regular = False
            #print(text, c.keys)
            if c.keys:
                for k in c.keys:
                    if c.fully:
                        for i in text.split(" "):
                            if k == i:
                                flag = True
                                break
                        if flag:
                            break
                    if c.loyal:
                        if k in text:
                            flag = True
                            break
                    else:
                        if k == text or k == text[1:]:
                            flag = True
                            break
                        elif k == text.split(" ")[0] or k == text.split(" ")[0][1:]:
                            flag = True
                            break
                        # if text != 'chat_invite_user' and text != 'chat_invite_user_by_link':
                        #     if k in text:
                        #         flag = True
                        #         break
                        if c.regular:
                            result = re.findall(r"" + str(k), text)
                            if result:
                                flag_regular = True
                                flag = True
                                break
                    if c.mandatory:
                        flag = True
                        break

                if flag:
                    res = await self.selection_them(c, them, is_bs, command_list)
                    if res == 1:
                        continue
                    if res == 0:
                        continue
                    if self.is_telegram and not issubclass(res.process, CommandsTg):
                        continue
                    if flag_regular:
                        return res, result[0]
                    else:
                        return res

        if not is_bs:
            res = await self.tree_analysis(command_list)
            if res != 1:
                return res

        # for c in command_list:
        #     if c.name == 'test':
        #         return c

        # for c in command_list:
        #     if c.name == 'endless_questions':
        #         return c

        # if await self.create_mongo.admin_answer_id_check(self.message["peer_id"]):
        #     for c in command_list:
        #         if c.name == 'response_text_admin':
        #             return c
        # if await self.create_mongo.get_users_ls_status(self.from_id, nap=True):
        #     for c in command_list:
        #         if c.name == 'answer':
        #             return c
            #return command_ls_dictionary["answer"]
        return 0

    async def selection_them(self, c, them, is_bs=False, command_list=None):
        for m in c.topics_blocks:
            if m == them or m == them[1:]:
                return 0
        if len(c.topics_resolution) == 0:
            if not is_bs:
                #res = await self.check_tree(c)
                res = await self.check_tree_new(c, command_list)
            else:
                res = await self.check_tree_bs(c)
            return res
        for n in c.topics_resolution:
            if n == them or n == them[1:]:
                if not is_bs:
                    #res = await self.check_tree(c)
                    res = await self.check_tree_new(c, command_list)
                else:
                    res = await self.check_tree_bs(c)
                return res
        return 0


    async def check_tree(self, cmd):
        #print(cmd.name, command_ls_dictionary)
        if cmd.name in command_ls_dictionary:
            res = await self.create_mongo.get_users_ls_status(self.from_id)
            #print("res ", res, command_ls_dictionary[cmd.name][1].root.name)
            if res:
                #print(cmd.name, command_ls_dictionary[cmd.name])
                if command_ls_dictionary[cmd.name][1].name == res:
                    await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                    return cmd
                if command_ls_dictionary[cmd.name][1].parent:
                    if command_ls_dictionary[cmd.name][1].parent.name == res:
                        await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                        return cmd
                if command_ls_dictionary[cmd.name][1].children:
                    for i in command_ls_dictionary[cmd.name][1].children:
                        if i.name == res:
                            await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                            return cmd
                if command_ls_dictionary[cmd.name][1].root.name == cmd.name:
                    await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                    return cmd
                return 1
            else:
                await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                return cmd

        else:
            return cmd

    async def tree_analysis(self, command_list):
        if self.is_telegram:
            #print("Третий user_id: ", int(str(self.from_id) + str(self.message["message"].message_id)))
            work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info,
                             user_id=int(str(self.from_id) + str(self.message["message"]["message_id"])))
        else:
            work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
        res = await work_ls.location_tree_check()
        #print(res.ignore_tree)
        if res.ignore_tree:
            #print("DA")
            for c in command_list:
                if c.name == res.location_tree:
                    if self.is_telegram and not issubclass(c.process, CommandsTg):
                        print(c.name)
                        continue
                    return c
        return 1

    async def check_tree_new(self, cmd, command_list=None):
        #print(cmd.name, command_ls_dictionary)
        if cmd.name in command_ls_dictionary:
            #res = await self.create_mongo.get_users_ls_status(self.from_id)
            if self.is_telegram:
                #print(self.message)
                work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info,
                                 user_id=int(str(self.from_id) + str(self.message["message"]["message_id"])))
            else:
                work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
            res = await work_ls.location_tree_check()
            #print("res ", res, command_ls_dictionary[cmd.name][1].root.name)
            #if res:
                #print(cmd.name, command_ls_dictionary[cmd.name])is_root

            if command_ls_dictionary[cmd.name][1].root.name == cmd.name:
                #await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                await work_ls.location_tree_set(cmd.name)
                return cmd

            #print(res.location_tree)
            if res.ignore_tree:
                for c in command_list:
                    if c.name == res.location_tree:
                        return c
            if command_ls_dictionary[cmd.name][1].name == res.location_tree:
                #await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                await work_ls.location_tree_set(cmd.name)
                return cmd

            if command_ls_dictionary[cmd.name][1].parent:
                if command_ls_dictionary[cmd.name][1].parent.name == res.location_tree:
                    #await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                    await work_ls.location_tree_set(cmd.name)
                    return cmd

            if command_ls_dictionary[cmd.name][1].children:
                for i in command_ls_dictionary[cmd.name][1].children:
                    if i.name == res.location_tree:
                        #await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
                        await work_ls.location_tree_set(cmd.name)
                        return cmd

            return 1
            # else:
            #     await self.create_mongo.add_users_ls_status(self.from_id, cmd.name)
            #     return cmd

        else:
            if self.is_telegram:
                work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info,
                                 user_id=int(str(self.from_id) + str(self.message["message"]["message_id"])))
            else:
                work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
            res = await work_ls.location_tree_check()
            if res.ignore_tree:
                for c in command_list:
                    if c.name == res.location_tree:
                        if self.is_telegram and not issubclass(c.process, CommandsTg):
                            continue
                        return c
            return cmd

    async def check_tree_bs(self, cmd):
        #print(cmd.name, command_bs_dictionary)
        if cmd.name in command_bs_dictionary:
            #if cmd.score == 0:
            print(cmd.name)
            return cmd
        else:
            return cmd





    # async def tree_distribution_root(self):
    #
    #     root = Node('help', process=command_ls_dictionary['help'])
    #     command_ls_dictionary['help'].append(root)
    #     question = Node('question', parent=root, process=command_ls_dictionary['question'])
    #     command_ls_dictionary['question'].append(question)
    #
    #     # right = Node("B", parent=left, red="bar")
    #     #
    #     # rig = Node("C", parent=root, test=Te)
    #     return root

    #async def is_tree(self):


    async def middleware_ls(self, flag=False):
        if "action" in self.message:
            text = self.message["action"]["type"]
        else:
            text = self.message["text"].lower()

        if flag:
            #print(self.message)
            sel = await self.selection(command_list, text, self.them, flag)
            #print(sel)
            if sel:
                if sel != 0:
                    #print(sel.description)
                    #print("SEL ", self.message["text"].lower())
                    self.loop.create_task(sel.process(self.v, self.club_id, self.message, self.apis, self.them,
                                                      self.create_mongo,
                                                      self.collection_bots,
                                                      self.document_tokens,
                                                      self.url_dj,
                                                      self.client,
                                                      tree_questions=self.tree_questions,
                                                      mongo_manager=self.mongo_manager,
                                                      settings_info=self.settings_info).run())
                return
            if self.them == "tema1":
                if not self.is_telegram:
                    self.loop.create_task(MessageAnalysisProcessing(self.v, self.club_id, self.message, self.apis, self.them,
                                                         self.create_mongo,
                                                         self.collection_bots,
                                                         self.document_tokens,
                                                         self.url_dj, client=self.client, tree_questions=self.tree_questions,
                                                         mongo_manager=self.mongo_manager,
                                                         settings_info=self.settings_info).run())

                # self.loop.create_task(processing_new(self.v, self.club_id, self.message, self.apis, self.them,
                #                                      self.create_mongo,
                #                                      self.collection_bots,
                #                                      self.document_tokens,
                #                                      self.url_dj, client=self.client, tree_questions=self.tree_questions,
                #                                      mongo_manager=self.mongo_manager,
                #                                      settings_info=self.settings_info).run())
            # self.loop.create_task(processing(self.v, self.club_id, self.message, self.apis, self.them,
            #                                  self.create_mongo,
            #                                  self.collection_bots,
            #                                  self.document_tokens,
            #                                  self.url_dj, client=self.client).run())
            return
        else:
            sel = await self.selection(command_ls_list, text, self.them, flag)
            # print(sel)
            # print(sel.description)
            if isinstance(sel, tuple):
                self.message["text"] = sel[1]
                sel = sel[0]
            if sel == 1:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.message["peer_id"],
                                         message="😅 Сожалею, но чтобы дойти до этого пункта, необходимо предоставить мне больше информации",
                                         random_id=0)
                return
            if sel:
                if sel != 0:
                    #print("SEL ", sel.name)
                    self.loop.create_task(sel.process(self.v, self.club_id, self.message, self.apis, self.them,
                                                      self.create_mongo, self.collection_bots,
                                                      self.document_tokens, self.url_dj, self.client,
                                                      tree_questions=self.tree_questions,
                                                      mongo_manager=self.mongo_manager,
                                                      settings_info=self.settings_info).run())
                return
            # if await self.create_mongo.admin_answer_id_check(self.message["peer_id"]):
            #     self.loop.create_task(
            #         response_text_admin(self.v, self.club_id, self.message, self.apis, self.them,
            #                             self.create_mongo,
            #                             self.collection_bots,
            #                             self.document_tokens,
            #                             self.url_dj, self.client).run())
        #print("SEL ", sel, self.message)










    async def middleware_bs(self):
        pass
