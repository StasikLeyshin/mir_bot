import traceback
import asyncio

import command_besed
from commands import commands


class globan(commands):

    async def run(self):
        adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
        if adm:
            user_id = await self.getting_user_id()
            if user_id:
                cause = await self.txt_warn(self.text)
                res = await self.create_mongo.globan_add(user_id, self.date, self.from_id, cause)
                if res[0] == 1:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"Данный [id{user_id}|пользователь] добавлен в глобальный бан. "
                                                     f"Оттуда ещё никто не возвращался...", random_id=0)
                elif res[0] == 2:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"Данный [id{user_id}|пользователь] уже есть в глобальном бане. "
                                                     f"И он оттуда скорее всего не вернётся...", random_id=0)
                loop = asyncio.get_running_loop()
                for i in res[1]:
                    try:
                        loop.create_task(self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                                                            member_id=user_id,
                                                            v=self.v))
                    except Exception as e:
                        print(traceback.format_exc())



globans = command_besed.Command()

globans.keys = ['/globan', '/глобан']
globans.description = 'Глобальный бан'
globans.process = globan
globans.topics_blocks = []
globans.topics_resolution = ["tema1"]
