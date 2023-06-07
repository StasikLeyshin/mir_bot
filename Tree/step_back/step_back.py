
from commands import commands
import command_ls
from command_ls import command_ls_dictionary, command_ls_list
from summer_module.work_ls.work_ls import WorkLs


class step_back(commands):

    async def run(self):

        # res = await self.create_mongo.get_users_ls_status(self.from_id)
        # if res:
        #     if res in command_ls_dictionary:
        #         #print(command_ls_dictionary[f"{res}"][1].parent)
        #         if command_ls_dictionary[f"{res}"][1].parent:
        #             await self.create_mongo.add_users_ls_status(self.from_id, command_ls_dictionary[f"{res}"][1].parent.name)
        #             await command_ls_dictionary[f"{res}"][1].parent.process[0].process(self.v, self.club_id, self.message, self.apis, self.them,
        #                             self.create_mongo,
        #                             self.collection_bots,
        #                             self.document_tokens,
        #                             self.url_dj).run()

        work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
        res = await work_ls.location_tree_check()
        #print(res.ignore_tree, res.location_tree, command_ls_dictionary)
        if not res.ignore_tree:
            if res.location_tree in command_ls_dictionary:
                #print(command_ls_dictionary[f"{res}"][1].parent)
                if command_ls_dictionary[f"{res.location_tree}"][1].parent:

                    #await self.create_mongo.add_users_ls_status(self.from_id, command_ls_dictionary[f"{res}"][1].parent.name)
                    #print(command_ls_dictionary[f"{res.location_tree}"][1].parent)
                    await command_ls_dictionary[f"{res.location_tree}"][1].parent.process[0].process(self.v, self.club_id, self.message, self.apis, self.them,
                                                          self.create_mongo,
                                                          self.collection_bots,
                                                          self.document_tokens,
                                                          self.url_dj,
                                                          self.client,
                                                          tree_questions=self.tree_questions,
                                                          mongo_manager=self.mongo_manager,
                                                          settings_info=self.settings_info).run()
                    await work_ls.location_tree_set(command_ls_dictionary[f"{res.location_tree}"][1].parent.name)

        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                          message="📚 Выбери свой статус",
        #                          random_id=0,
        #                          keyboard=self.level_status())


step_backs = command_ls.Command()

step_backs.keys = ['шаг назад']
step_backs.description = 'Шаг назад'
#step_backs.set_dictionary('question')
step_backs.process = step_back
step_backs.topics_blocks = []
step_backs.topics_resolution = ["tema1"]
