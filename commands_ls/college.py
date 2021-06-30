import command_ls
from commands import commands
from api import api_url, api, photo_upload

class college(commands):

    async def run(self):
        vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "col")
        self.create_mongo.add_user(self.peer_id, 0, nap="col")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=f"✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                 random_id=0,
                                 attachment=vopr)



colleges = command_ls.Command()

colleges.keys = ['колледж']
colleges.description = 'Колледж'
colleges.process = college
colleges.topics_blocks = ["target", "consultants"]
colleges.topics_resolution = []
