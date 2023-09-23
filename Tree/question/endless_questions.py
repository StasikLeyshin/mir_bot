from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.work_ls.work_ls import WorkLs


class endless_questions(commands):

    async def run(self):
        #print("DOSHLO")
        res = await self.create_mongo.get_users_ls_status_questions(self.from_id)
        if not res:
            await self.create_mongo.add_users_ls_status_questions(self.from_id, 11)

        if self.text.lower() == "помощь по приёму":
            await self.create_mongo.add_users_ls_status_questions(self.from_id, 11)
            text_new = self.tree_questions.search(level=11)
            work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
            res = await work_ls.location_tree_check()
            res.ignore_tree = True
            await work_ls.location_tree_update()
        else:

            if int(res) == 11 and self.text.lower() == "шаг назад":

                work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
                res = await work_ls.location_tree_check()
                res.ignore_tree = False
                await work_ls.location_tree_update()

                await step_back(self.v, self.club_id, self.message, self.apis, self.them,
                                                      self.create_mongo,
                                                      self.collection_bots,
                                                      self.document_tokens,
                                                      self.url_dj,
                                                      self.client,
                                                      tree_questions=self.tree_questions,
                                                      mongo_manager=self.mongo_manager,
                                                      settings_info=self.settings_info).run()
                return
            text_new = self.tree_questions.search(text=self.text, level=int(res))
            if not text_new:
                return
        #print(res, text_new)
        keyboard = self.generations_keyboard(text_new[2])
        await self.create_mongo.add_users_ls_status_questions(self.from_id, int(text_new[0]))

        msg = text_new[1].replace("Если вы хотите вернуться на предыдущий шаг, отправьте цифру 1.", "")
        msg = msg.replace("(укажите цифрой)", "")
        msg = msg.replace("(цифрой)", "")
        msg = msg.replace("Если вы хотите вернуться на предыдущий шаг отправьте цифру 1.", "")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=msg,
                                 random_id=0,
                                 keyboard=keyboard)


        # vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "magistracy")
        # await self.create_mongo.add_users_ls_status(self.from_id, nap="magistracy")
        #
        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                          message="✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
        #                          random_id=0,
        #                          keyboard=self.menu_incomplete(),
        #                          attachment=vopr)




endless_questionss = command_ls.Command()

endless_questionss.keys = ['помощь по приёму']
endless_questionss.description = 'Помощь по приёму'
endless_questionss.set_dictionary('endless_questions')
endless_questionss.process = endless_questions
#endless_questionss.mandatory = True
endless_questionss.topics_blocks = []
endless_questionss.topics_resolution = ["tema1"]
