# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from api.api_execute import kick
from commands import commands
from summer_module.punishments import WarnAdminCheck


class Zawarn(commands):

    async def run(self):
        #print(self.message)
        if "payload" in self.message and self.peer_id in [2000000039, 2000000051]:
        #if "payload" in self.message and self.peer_id == 2000000007:
            try:

                spis = self.message["payload"].replace('"', '').split("@")
                user_id = int(spis[0])
                current_time = int(spis[1])
                con_id = int(spis[2])
                type_sms = spis[3]
                type_punishment = spis[4]
                zawarn = WarnAdminCheck(self.mongo_manager, self.settings_info, self.from_id, self.date)

                result = await zawarn.apply_punishment(peer_id=self.peer_id, user_id=user_id, current_time=current_time,
                                                       conversation_message_id_forward=con_id, type_sms=type_sms,
                                                       type_punishment=type_punishment)
                #print(result)
                for i in result["messages"]:
                    if not i.get("error_message"):
                        if i.get('conversation_message_id'):
                            res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}",
                                                           name_case="nom")
                            name = f'{res[0]["first_name"]} {res[0]["last_name"]}'
                            res = await self.apis.api_post("messages.send", v=self.v, peer_id=i["peer_id"],
                                                           message=i["message"].format(name), random_id=0,
                                                           forward=self.answer_msg_other_parameters(i["peer_id"], i["conversation_message_id"]))
                                                     #conversation_message_ids=i["conversation_message_id"])
                            #print(res)
                        else:
                            await self.apis.api_post("messages.send", v=self.v, peer_id=i["peer_id"],
                                                     message=i["message"], random_id=0)
                    if i.get("kick_id"):
                        await self.apis.api_post("execute", code=kick(users=i["kick_id"],
                                                                      chat_id=self.chat_id_param(i["peer_id"])),
                                                 v=self.v)



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


zawarns = command_besed.Command()

zawarns.keys = ['Заварнить', 'БАН', 'Глобальный бан']
zawarns.description = 'Реакция на нажатие кнопки админом'
zawarns.set_dictionary('Zwarn')
zawarns.fully = True
zawarns.process = Zawarn
zawarns.topics_blocks = []
zawarns.topics_resolution = ["tema1"]
