# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands

from punishments import warn_give_out
from api.api_execute import kick

class zawarn(commands):

    async def run(self):
        if "payload" in self.message and self.peer_id == 2000000024:
            spis = self.message["payload"].replace('"', '').split("@")
            user_id = spis[0]
            vrem = spis[1]
            con_id = spis[2]
            result = await self.create_mongo.chek_zawarn(user_id, vrem)
            print(result)
            if result[0] == 1:
                vrem = 86400
                cause = "Использование ненормативной лексики"
                ply = await self.display_time(vrem)
                result_new = await warn_give_out(self.v).ban_give(self.apis, self.create_mongo, result[1], cause,
                                                                  self.chat_id_param(result[1]), str(user_id),
                                                                  str(self.from_id), vrem, ply)

                await self.apis.api_post("messages.send", v=self.v, peer_id=result[1],
                                         message=result_new[1], random_id=0,
                                         forward=self.answer_msg_other_parameters(result[1], con_id))
                if len(result_new) == 3:
                    loop = asyncio.get_running_loop()
                    for i in result_new[2]:
                        try:
                            loop.create_task(
                                self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                                                   member_id=user_id,
                                                   v=self.v))
                        except:
                            pass
                    return

                if result_new[0]:
                    await self.apis.api_post("execute", code=kick(users=[user_id], chat_id=self.chat_id_param(result[1])),
                                             v=self.v)
                if result_new[1] != "Это вообще кто?😳":
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"Данный [id{user_id}|пользователь] был успешно заварнен ✅", random_id=0)
            elif result[0] == 0:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"Данный [id{user_id}|пользователь] уже был заварнен ❌",
                                         random_id=0)










zawarns = command_besed.Command()

zawarns.keys = ['заварнить']
zawarns.description = 'Выдача варна по кнопке'
zawarns.process = zawarn
zawarns.topics_blocks = []
zawarns.topics_resolution = ["tema1"]