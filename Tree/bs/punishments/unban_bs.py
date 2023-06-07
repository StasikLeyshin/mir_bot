# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from api.api_execute import kick
from commands import commands
from summer_module.punishments import WarnAdminCheck
from summer_module.punishments.unban import UnbanLs


class UnbanBs(commands):

    async def run(self):
        if "payload" in self.message and self.peer_id == 2000000039:
            try:
                spis = self.message["payload"].replace('"', '').split("@")
                user_id = int(spis[0])
                current_time = int(spis[1])
                task_id = int(spis[2])
                type_punishment = spis[3]

                unban = UnbanLs(self.mongo_manager, self.settings_info, user_id, self.date)

                #if type_punishment == "unban":
                result = await unban.give_permission(task_id=task_id, type_punishment=type_punishment)
                # elif type_punishment == "ban":
                #     result = await unban.give_permission(task_id=task_id, status=True)

                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=result["message"], random_id=0)
                # zawarn = WarnAdminCheck(self.mongo_manager, self.settings_info, self.from_id, self.date)
                #
                # result = await zawarn.apply_punishment(peer_id=self.peer_id, user_id=user_id, current_time=current_time,
                #                                        conversation_message_id_forward=con_id, type_sms=type_sms,
                #                                        type_punishment=type_punishment)
                #print(result)
                # for i in result["messages"]:
                #     if not i.get("error_message"):
                #         if i.get('conversation_message_id'):
                #             res = await self.apis.api_post("messages.send", v=self.v, peer_id=i["peer_id"],
                #                                      message=i["message"], random_id=0,
                #                                            forward=self.answer_msg_other_parameters(i["peer_id"], i["conversation_message_id"]))
                #                                      #conversation_message_ids=i["conversation_message_id"])
                #             #print(res)
                #         else:
                #             await self.apis.api_post("messages.send", v=self.v, peer_id=i["peer_id"],
                #                                      message=i["message"], random_id=0)
                #     if i.get("kick_id"):
                #         await self.apis.api_post("execute", code=kick(users=i["kick_id"],
                #                                                       chat_id=self.chat_id_param(i["peer_id"])),
                #                                  v=self.v)



                # if get_method:
                #
                #     result = await start.run(peer_id=self.peer_id, users=get_method[0], users_all=get_method[1])
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                              message=result["message"], random_id=0)  # , reply_to=sms_id)
            except Exception as e:
                print(traceback.format_exc())
            # star = await self.methods.users_chek(self.peer_id, self.apis)
            # if star:
            #     self.create_mongo.start_bs(self.peer_id, star[0], star[1], star[2])
            #     # result = await self.apis.api_post("messages.getByConversationMessageId", v=self.v, peer_id=self.peer_id,
            #                                       # conversation_message_ids=str(self.conversation_message_id))
            #     #sms_id = result["items"][0]["id"]
            #     #print(sms_id)
            #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                              message="Вдох-выдох ✅", random_id=0)  # , reply_to=sms_id)


unban_ss = command_besed.Command()

unban_ss.keys = ['разбанить', 'не разбанить']
unban_ss.description = 'Реакция на нажатие кнопки админом (не)разбан'
unban_ss.set_dictionary('unban_bs')
unban_ss.fully = True
unban_ss.process = UnbanBs
unban_ss.topics_blocks = []
unban_ss.topics_resolution = ["tema1"]
