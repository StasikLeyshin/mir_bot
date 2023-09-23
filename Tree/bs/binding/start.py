# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands
from summer_module import Start
from api import api_url



class startnew(commands):

    async def run(self):
        adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)
        if adm == 1 or self.from_id == 597624554:
            try:
                start = Start(self.mongo_manager, self.settings_info)

                get_method = await self.methods.users_chek(self.peer_id, self.apis)

                res = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                               peer_ids=f"{self.peer_id}")
                name = res["items"][0]['chat_settings']['title']
                post = await api_url(f"{self.url_dj}").post_json(create_bs=2, name=name+"(ВК)", Conver=self.peer_id)

                if get_method:

                    result = await start.run(peer_id=self.peer_id, users=get_method[0], users_all=get_method[1],
                                             user_admins=get_method[2])
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=result["message"], random_id=0)  # , reply_to=sms_id)
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
