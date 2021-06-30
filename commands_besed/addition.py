import command_besed
from commands import commands
from api.api_execute import kick

class addition(commands):

    async def run(self):

        if self.message["action"]["member_id"] == self.from_id:
            chek = await self.create_mongo.add_user_bs(self.from_id, self.peer_id, f=1)
            if chek == 2:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"⚠ Данный [id{self.from_id}|пользователь] находится в бане.",
                                         random_id=0)
                await self.apis.api_post("execute", code=kick(users=[self.from_id], chat_id=self.chat_id()), v=self.v)
                return
        else:
            chek = await self.create_mongo.add_user_bs(self.message["action"]["member_id"], self.peer_id, f=1)
            if chek == 2:
                adm = await self.create_mongo.admin_check(self.from_id, self.peer_id, f=1)
                if adm:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"⚠ Данного [id{self.message['action']['member_id']}|пользователя], "
                                                     f"находившегося в бане, пригласил администратор."
                                                     f"Так уж и быть, сниму с него бан.😌",
                                             random_id=0)
                    await self.create_mongo.ban_remove(self.message["action"]["member_id"], self.peer_id)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"⚠ Данный [id{self.message['action']['member_id']}|пользователь] находится в бане.",
                                             random_id=0)
                    await self.apis.api_post("execute", code=kick(users=[self.message["action"]["member_id"]], chat_id=self.chat_id()), v=self.v)
                    return



additions = command_besed.Command()

additions.keys = ['chat_invite_user']
additions.description = 'Возвращение или приход пользователя'
additions.process = addition
additions.topics_blocks = []
additions.topics_resolution = ["zluka"]
