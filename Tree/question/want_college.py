from commands import commands
import command_ls


class want_college(commands):

    async def run(self):
        vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "college")
        await self.create_mongo.add_users_ls_status(self.from_id, nap="college")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                 random_id=0,
                                 keyboard=self.menu_incomplete(),
                                 attachment=vopr)

want_colleges = command_ls.Command()

want_colleges.keys = ['Хочу поступать в колледж']
want_colleges.description = 'Хочу поступать в колледж'
want_colleges.set_dictionary('want_college')
want_colleges.process = want_college
want_colleges.topics_blocks = []
want_colleges.topics_resolution = ["tema1"]
