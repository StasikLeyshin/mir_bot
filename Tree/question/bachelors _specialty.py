from commands import commands
import command_ls


class bachelors_specialty(commands):

    async def run(self):
        vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "bachelors")
        await self.create_mongo.add_users_ls_status(self.from_id, nap="bachelors")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                 random_id=0,
                                 keyboard=self.menu_incomplete(),
                                 attachment=vopr)


bachelors_specialtys = command_ls.Command()

bachelors_specialtys.keys = ['Поступаю в бакалавриат/специалитет']
bachelors_specialtys.description = 'Показать вопросы бакалавриат/специалитет'
bachelors_specialtys.set_dictionary('bachelors_specialty')
bachelors_specialtys.process = bachelors_specialty
bachelors_specialtys.topics_blocks = []
bachelors_specialtys.topics_resolution = ["tema1", "mirea_official"]
