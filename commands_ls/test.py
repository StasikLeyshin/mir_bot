import command_ls
from commands import commands
from api import api_url, api, photo_upload

class test(commands):

    async def run(self):
        if self.from_id == 597624554:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=f"✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.",
                                     random_id=0,
                                     attachment="photo597624554_457241703,photo597624554_457241704")




tests = command_ls.Command()

tests.keys = ['тест', 'test']
tests.description = 'бакалавриат / специалитет'
tests.process = test
tests.topics_blocks = ["target", "consultants"]
tests.topics_resolution = []
