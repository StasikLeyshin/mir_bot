import command_ls
from commands import commands
from api import api_url, api, photo_upload

class magistracy(commands):

    async def run(self):
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=f"Мы работаем над тем, чтобы тут появились ответы на вопросы, а пока их нет, "
                                         f"вы можете просто написать нам в лс, и мы обязательно ответим!",
                                 random_id=0)



magistracys = command_ls.Command()

magistracys.keys = ['магистратура']
magistracys.description = 'Магистратура'
magistracys.process = magistracy
magistracys.topics_blocks = ["target", "consultants"]
magistracys.topics_resolution = []
