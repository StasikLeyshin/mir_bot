import command_ls
from commands import commands
from api import api_url, api, photo_upload

class undergraduate_specialty(commands):

    async def run(self):
        vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "bac")
        self.create_mongo.add_user(self.peer_id, 0, nap="bac")
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=f"✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                 random_id=0,
                                 attachment=vopr)


undergraduate_specialtys = command_ls.Command()

undergraduate_specialtys.keys = ['бакалавриат / специалитетенр', 'бакалавриатенрнр', 'специалитетерр']
undergraduate_specialtys.description = 'бакалавриат / специалитет'
undergraduate_specialtys.process = undergraduate_specialty
undergraduate_specialtys.topics_blocks = ["target", "consultants"]
undergraduate_specialtys.topics_resolution = []
