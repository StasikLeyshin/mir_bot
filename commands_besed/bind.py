# -*- coding: utf-8 -*-
import asyncio

import command_besed
from commands import commands

from api.methods import messages_edit

class bind(commands):

    async def run(self):
        adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)
        if adm == 1:

            post = self.create_mongo.update(self.club_id, self.peer_id)
            if post == 1:
                msg = messages_edit(self.v, self.club_id, self.apis, self.peer_id, "Начинаю запись данных👁")
                await msg.strat_send()
                await asyncio.sleep(1)
                #await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id, message="Беседа успешно привязна ✅", random_id=0)
                await msg.finish("Беседа успешно привязна ✅")
            #self.apis.
    '''async def bind(self):
        ad = methods(self.v, self.club_id)
        adm = await ad.admin_chek(self.message)
        print(adm)
        if adm == 1:pass'''



binds = command_besed.Command()

binds.keys = ['привязать', 'привязка']
binds.description = 'Пришлю картинку с котиком'
binds.process = bind