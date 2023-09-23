import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.punishments import BanGive


class ban(commands):

    async def run(self):
        try:
            adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)
            if adm == 1 or self.from_id == 597624554:
                user_id = await self.getting_user_id()
                if user_id:
                    await self.apis.api_post("execute", code=kick(users=[int(user_id) ], chat_id=self.chat_id()),
                                             v=self.v)


        except Exception as e:
            print(traceback.format_exc())





bans = command_besed.Command()

bans.keys = ['/кик', '/kick']
bans.description = 'Кик пользователя'
bans.set_dictionary('kick')
bans.loyal = True
bans.process = ban
bans.topics_blocks = []
bans.topics_resolution = ["tema1"]
