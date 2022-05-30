from commands import commands
import command_ls


class studying_university_college(commands):

    async def run(self):
        vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "student")
        await self.create_mongo.add_users_ls_status(self.from_id, nap="student")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                 random_id=0,
                                 keyboard=self.menu_incomplete(),
                                 attachment=vopr)

studying_university_colleges = command_ls.Command()

studying_university_colleges.keys = ['Уже учусь в вузе/колледже']
studying_university_colleges.description = 'Уже учусь в вузе/колледже'
studying_university_colleges.set_dictionary('studying_university_college')
studying_university_colleges.process = studying_university_college
studying_university_colleges.topics_blocks = []
studying_university_colleges.topics_resolution = ["tema1", "mirea_official"]
