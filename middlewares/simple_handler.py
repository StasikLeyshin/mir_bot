
from command_ls import command_ls_dictionary, command_ls_list
from commands_ls import issuing_directions, choice_conversation, response_text_admin
from command_besed import command_bs_dictionary, command_list


from Tree import Node


class SimpleHandler:

    def __init__(self, v, club_id, message, apis, them, create_mongo, collection_bots, document_tokens,
                            url_dj, loop):
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
        #print(command_ls_dictionary)
        #self.root = self.tree_distribution_root()
        #print(self.root.children.question)
        #print(command_ls_dictionary)


    async def selection(self, command_list, text, them, is_bs=False):
        for c in command_list:
            flag = False
            #print(c.keys, text)
            if c.keys:
                for k in c.keys:
                    if c.fully:
                        if k in text:
                            flag = True
                            break
                    else:
                        if k == text or k == text[1:]:
                            # print(c)
                            flag = True
                            break
                        elif k == text.split(" ")[0] or k == text.split(" ")[0][1:]:
                            flag = True
                            break
                        if text != 'chat_invite_user' and text != 'chat_invite_user_by_link':
                            if k in text:
                                flag = True
                                break
                    if c.mandatory:
                        flag = True
                        break
                    # elif k in text:
                    #     flag = True
                    #     break
                    #print(text.split(" ")[0])
                #print(flag)
                if flag:
                    #print(c.description, them)
                    res = await self.selection_them(c, them, is_bs)
                    #print(res)
                    if res == 1:
                        continue
                    if res == 0:
                        continue
                    return res
                    # for m in c.topics_blocks:
                    #     if m == them or m == them[1:]:
                    #         return 0
                    # if len(c.topics_resolution) == 0:
                    #     return await self.check_tree(c)
                    # for n in c.topics_resolution:
                    #     if n == them or n == them[1:]:
                    #         return await self.check_tree(c)
                    # return 0
        if await self.create_mongo.admin_answer_id_check(self.message["peer_id"]):
            for c in command_list:
                if c.name == 'response_text_admin':
                    return c
        if await self.create_mongo.get_users_ls_status(self.from_id, nap=True):
            for c in command_list:
                if c.name == 'answer':
                    return c
            #return command_ls_dictionary["answer"]
        return 0

    async def selection_them(self, c, them, is_bs=False):
        for m in c.topics_blocks:
            if m == them or m == them[1:]:
                return 0
        if len(c.topics_resolution) == 0:
            if not is_bs:
                res = await self.check_tree(c)
            else:
                res = await self.check_tree_bs(c)
            return res
        for n in c.topics_resolution:
            if n == them or n == them[1:]:
                if not is_bs:
                    res = await self.check_tree(c)
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


    async def check_tree_bs(self, cmd):
        #print(cmd.name, command_bs_dictionary)
        if cmd.name in command_bs_dictionary:
            if cmd.score == 0:
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
            text = self.message["action"]
        else:
            text = self.message["text"].lower()
        if flag:
            sel = await self.selection(command_list, text, self.them, flag)
        else:
            sel = await self.selection(command_ls_list, text, self.them, flag)
        print(sel)
        if sel == 1:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.message["peer_id"],
                                     message="😅 Сожалею, но чтобы дойти до этого пункта, необходимо предоставить мне больше информации",
                                     random_id=0)
            return
        if sel:
            if sel != 0:
                self.loop.create_task(sel.process(self.v, self.club_id, self.message, self.apis, self.them,
                                        self.create_mongo,
                                        self.collection_bots,
                                        self.document_tokens,
                                        self.url_dj).run())
            return
        if await self.create_mongo.admin_answer_id_check(self.message["peer_id"]):
            self.loop.create_task(
                response_text_admin(self.v, self.club_id, self.message, self.apis, self.them,
                                    self.create_mongo,
                                    self.collection_bots,
                                    self.document_tokens,
                                    self.url_dj).run())










    async def middleware_bs(self):
        pass
