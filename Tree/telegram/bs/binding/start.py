# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands
from commands_tg import CommandsTg
from summer_module import Start
from api import api_url



class startnew(CommandsTg):

    async def run(self):
        adm = await self.admin_chek(self.from_id, self.peer_id)
        if adm:
            try:
                start = Start(self.mongo_manager, self.settings_info)

                #get_method = await self.methods.users_chek(self.peer_id, self.apis)

                #res = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                               #peer_ids=f"{self.peer_id}")
                #name = res["items"][0]['chat_settings']['title']
                #post = await api_url(f"{self.url_dj}").post_json(create_bs=2, name=name+"(ВК)", Conver=self.peer_id)

                admin_list = []
                admin_list_ids = []
                adm_list = self.apis.get_chat_administrators(self.peer_id)
                for i in adm_list:
                    admin_list.append({"user_id": i.user.id, "admin": True})
                    admin_list_ids.append(i.user.id)
                #print(admin_list)
                # if get_method:
                #
                #     result = await start.run(peer_id=self.peer_id, users=admin_list, users_all=admin_list_ids,
                #                              user_admins=admin_list_ids)
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                              message=result["message"], random_id=0)  # , reply_to=sms_id)
                result = await start.run(peer_id=self.peer_id, users=admin_list, users_all=admin_list_ids,
                                         user_admins=admin_list_ids)
                self.apis.send_message(self.peer_id, result["message"])
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


startnews = command_besed.Command()

startnews.keys = ['/update']
startnews.description = 'Обновление информации о беседе'
startnews.set_dictionary('startnew')
startnews.process = startnew
startnews.topics_blocks = []
startnews.topics_resolution = ["tema1"]
