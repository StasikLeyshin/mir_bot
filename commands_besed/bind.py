# -*- coding: utf-8 -*-
import asyncio

import command_besed
from commands import commands
from api import api_url

from api.methods import messages_edit

class bind(commands):

    async def run(self):
        #print("test")
        adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)
        #adm = 1
        #print(adm)
        if adm == 1:

            #post = self.create_mongo.update(self.collection_bots, self.document_tokens, self.club_id, self.peer_id)
            post = await api_url(f"{self.url_dj}").post_json(club_id=self.club_id, peer_id=self.peer_id, status=2)
            print(post)
            if "peer_id" in post:
                if post["peer_id"] == 1:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="Привязал ✅", random_id=0) #Беседа успешно привязна ✅
                    #messages_edit(self.v, self.club_id, self.apis, self.peer_id, "Беседа успешно записана ✅")
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="Беседа уже была добавлена ⛔", random_id=0)
                #messages_edit(self.v, self.club_id, self.apis, self.peer_id, "Беседа уже была добавлена ⛔")
                #msg = messages_edit(self.v, self.club_id, self.apis, self.peer_id, "Начинаю запись данных 👁")
                #await msg.strat_send()
                #await asyncio.sleep(1)
                #await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id, message="Беседа успешно привязна ✅", random_id=0)
                #await msg.finish("Беседа успешно записана ✅\n⚠ Во избежания спама, сообщение самоуничтожится через 5 секунд")
                #await asyncio.sleep(5)
                #await msg.del_sms()
            #self.apis.
    '''async def bind(self):
        ad = methods(self.v, self.club_id)
        adm = await ad.admin_chek(self.message)
        print(adm)
        if adm == 1:pass'''



binds = command_besed.Command()

binds.keys = ['привязать', 'привязка']
binds.description = 'Привязка группы'
binds.process = bind
binds.topics_blocks = ["consultants"]
binds.topics_resolution = []
