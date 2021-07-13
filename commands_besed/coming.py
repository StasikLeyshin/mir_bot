
import command_besed
from commands import commands
from api.api_execute import kick

class coming(commands):

    async def run(self):
        ch = await self.create_mongo.globan_chek(self.from_id)
        if ch:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=f"⚠ Данный [id{self.from_id}|пользователь] находится в глобалбане.",
                                     random_id=0)
            await self.apis.api_post("execute", code=kick(users=[self.from_id], chat_id=self.chat_id()), v=self.v)
            return
        chek = await self.create_mongo.add_user_bs(self.from_id, self.peer_id, f=1)
        if chek == 2:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=f"⚠ Данный [id{self.from_id}|пользователь] находится в бане.", random_id=0)
            await self.apis.api_post("execute", code=kick(users=[self.from_id], chat_id=self.chat_id()), v=self.v)



comings = command_besed.Command()

comings.keys = ['chat_invite_user_by_link']
comings.description = 'Приход пользователя по ссылке'
comings.process = coming
comings.topics_blocks = []
comings.topics_resolution = ["zluka"]
