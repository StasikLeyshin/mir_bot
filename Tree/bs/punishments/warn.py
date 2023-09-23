import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.punishments import WarnGive


class warn(commands):

    async def run(self):
        try:
            user_id = await self.getting_user_id()
            if user_id:
                cause = await self.txt_warn(self.text)

                ban_give = WarnGive(self.mongo_manager, self.settings_info, self.from_id, self.date)

                result = await ban_give.run(user_id=int(user_id), peer_id=self.peer_id, cause=cause, from_id_check=True)
                if result:
                    res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}", name_case="nom")
                    name = f'{res[0]["first_name"]} {res[0]["last_name"]}'

                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=result["message"].format(name), random_id=0)
                    if result["action"] == "kick":
                        await self.apis.api_post("execute", code=kick(users=result["kick_id"], chat_id=self.chat_id()),
                                                 v=self.v)



            # adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            # print("adm", adm)
            # if adm or self.from_id == 597624554:
            #     vrem = await self.preobrz(self.text)
            #     cause = await self.txt_warn(self.text)
            #     ply = await self.display_time(vrem)
            #     result = "Не получилось, не фортануло:("


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

                # user_id = await self.getting_user_id()
                # if user_id:
                #     await achievements(self.client, int(user_id), self.v).add_warn(self.apis, self.peer_id, self.from_id, vrem, cause)
                #     result = await ban_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id, cause,
                #                                                  self.chat_id(),
                #                                                  user_id, self.from_id, vrem, ply)
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                              message=result[1], random_id=0)
                #
                #     if len(result) == 3:
                #         loop = asyncio.get_running_loop()
                #         for i in result[2]:
                #             try:
                #                 loop.create_task(
                #                     self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                #                                        member_id=user_id,
                #                                        v=self.v))
                #             except:pass
                #         return
                #
                #     if result[0]:
                #         await self.apis.api_post("execute", code=kick(users=[user_id], chat_id=self.chat_id()), v=self.v)
                # return


        except Exception as e:
            print(traceback.format_exc())





warns = command_besed.Command()

warns.keys = ['/наказать', '/варн', '/warn']
warns.description = 'Выдача варна'
warns.loyal = True
warns.set_dictionary('warn')
warns.process = warn
warns.topics_blocks = []
warns.topics_resolution = ["tema1"]
