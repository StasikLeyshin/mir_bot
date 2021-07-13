# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick

class ban(commands):

    async def run(self):
        try:
            #adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                vrem = await self.preobrz(self.text)
                cause = await self.txt_warn(self.text)
                ply = await self.display_time(vrem)
                result = "Не получилось, не фортануло:("
                # if "reply_message" in self.message or self.fwd_messages != []:
                #     if "reply_message" in self.message:
                #         user_id = self.message["reply_message"]["from_id"]
                #     else:
                #         user_id = self.fwd_messages["from_id"]
                #     user_id = str(user_id)
                #     result = await ban_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id, cause, self.chat_id(),
                #                                                  user_id, self.from_id, vrem, ply)
                #
                # elif len(self.text.lower().split(' ')) > 1:
                #     if "vk.com/" in self.text.lower():
                #         t = await self.opredel_skreen(self.text.lower().split(' ')[1], self.text.lower())
                #         #test = await vk.api.utils.resolve_screen_name(screen_name=t)
                #         test = await self.apis.api_post("utils.resolveScreenName", v=self.v, screen_name=t)
                #         if test["type"] == "group":
                #             user_id = "-" + str(test["object_id"])
                #         else:
                #             user_id = test["object_id"]
                #         user_id = str(user_id)
                #         result = await ban_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id, cause, self.chat_id(),
                #                                     user_id, self.from_id, vrem, ply)
                #
                #     elif "[id" in str(self.text.lower()) or "[club" in str(self.text.lower()):
                #         i = self.text.lower().split(' ')[1]
                #         user_id = await self.opredel_skreen(i, self.text.lower())
                #         result = await ban_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id, cause, self.chat_id(),
                #                                     user_id, self.from_id, vrem, ply)

                user_id = await self.getting_user_id()
                if user_id:
                    result = await ban_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id, cause,
                                                                 self.chat_id(),
                                                                 user_id, self.from_id, vrem, ply)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=result[1], random_id=0)

                    if len(result) == 3:
                        loop = asyncio.get_running_loop()
                        for i in result[2]:
                            try:
                                loop.create_task(
                                    self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                                                       member_id=user_id,
                                                       v=self.v))
                            except:pass
                        return

                    if result[0]:
                        await self.apis.api_post("execute", code=kick(users=[user_id], chat_id=self.chat_id()), v=self.v)
                return


        except Exception as e:
            print(traceback.format_exc())





bans = command_besed.Command()

bans.keys = ['/бан', '/ban', '/Бан', '/Ban']
bans.description = 'Выдача бана'
bans.process = ban
bans.topics_blocks = []
bans.topics_resolution = ["tema1"]
