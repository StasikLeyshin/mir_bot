from commands import commands
import command_ls


class magistracy(commands):

    async def run(self):
        vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "magistracy")
        await self.create_mongo.add_users_ls_status(self.from_id, nap="magistracy")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                 random_id=0,
                                 keyboard=self.menu_incomplete(),
                                 attachment=vopr)


magistracys = command_ls.Command()

magistracys.keys = ['Поступаю в магистратуру']
magistracys.description = 'Показать вопросы магистратуры'
magistracys.set_dictionary('magistracy')
magistracys.process = magistracy
magistracys.topics_blocks = []
magistracys.topics_resolution = ["tema1"]
