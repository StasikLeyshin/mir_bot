# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands
from api.api_execute import kick
from api.methods import messages_edit

class show(commands):

    async def run(self):
        try:
            #adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            #if adm:
            if str(self.from_id) == "597624554":
                result = await self.create_mongo.get_users_released(self.peer_id)
                #print(result)
                de = self.chunks(result, 25)
                l = list(de)
                #print(l)
                msg = messages_edit(self.v, self.club_id, self.apis, self.peer_id, "🤡 Начинаю запуск модуля шоу.")
                await msg.start_send()
                await asyncio.sleep(1)
                await msg.finish("⏰ До начала шоу осталось 5 секунд")
                await asyncio.sleep(1)
                await msg.finish("⏰ До начала шоу осталось 4 секунд")
                await asyncio.sleep(1)
                await msg.finish("⏰ До начала шоу осталось 3 секунд")
                await asyncio.sleep(1)
                await msg.finish("⏰ До начала шоу осталось 2 секунд")
                await asyncio.sleep(1)
                await msg.finish("⏰ До начала шоу осталось 1 секунд")
                await asyncio.sleep(1)
                await msg.finish("🎉🎊 Шоу начинается! 🎊🎉")
                for i in l:
                    await self.apis.api_post("execute", code=kick(users=i, chat_id=self.chat_id()), v=self.v)
                    await asyncio.sleep(0.5)
        except Exception as e:
            print(traceback.format_exc())








shows = command_besed.Command()

shows.keys = ['/шоу', 'начать шоу']
shows.description = 'Привязка беседы'
shows.process = show
shows.topics_blocks = []
shows.topics_resolution = ["tema1"]
