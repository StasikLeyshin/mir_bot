import traceback
import asyncio
from datetime import datetime
import traceback

import command_besed
from commands import commands
from record_achievements import record_achievements
from api.api_execute import kick


class achievement(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                user_id = await self.getting_user_id()
                if user_id:
                    ach = await self.txt_achievement(self.text)
                    #res = await self.create_mongo.profile_users_add(user_id, f"{ach[0]}", ach[1])
                    result = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}")
                    name = f'{result[0]["first_name"]} {result[0]["last_name"]}'
                    res = await record_achievements(self.create_mongo, user_id).run(achievement=ach[0], ach_kol=float(ach[1]))
                    adm = await self.create_mongo.admin_check(user_id, self.peer_id)
                    if not adm:
                        if res[0] == 1:
                            timestamp = 604800 + int(self.date)
                            value = datetime.fromtimestamp(timestamp)
                            time = value.strftime('%d.%m.%Y %H:%M')
                            await self.create_mongo.ban_check(user_id, self.peer_id, "Рейтинг достиг отметки ниже -30",
                                                              604800,
                                                              self.date, self.from_id)
                            ply = await self.display_time(604800)
                            msg = f"[id{user_id}|{name}], вам бан на {ply}\n📝 Причина: Рейтинг достиг отметки ниже -30\n⏰ Время окончания: {time}\n\n" \
                                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.\n\n📊 Рейтинг: {res[2]}"

                            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                     message=msg, random_id=0)
                            await self.apis.api_post("execute", code=kick(users=[user_id], chat_id=self.chat_id()),
                                                     v=self.v)
                            return

                        elif res[0] == 2:
                            res_new = await self.create_mongo.globan_add(user_id, self.date, self.from_id,
                                                                    "Рейтинг достиг отметки ниже -50")
                            if res_new[0] == 1:
                                msg = f"Данный [id{user_id}|пользователь] добавлен в глобальный бан.\n\n" \
                                      f"📝 Причина: Рейтинг достиг отметки ниже -50.\n\n" \
                                      f"P.S. Оттуда ещё никто не возвращался..."
                            elif res_new[0] == 2:
                                msg = f"Данный [id{user_id}|пользователь] уже есть в глобальном бане.\n\n" \
                                      f"P.S. И он оттуда скорее всего не вернётся..."

                            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                     message=msg, random_id=0)
                            loop = asyncio.get_running_loop()
                            for i in res_new[1]:
                                try:
                                    loop.create_task(
                                        self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                                                           member_id=user_id,
                                                           v=self.v))
                                except:
                                    pass
                            return

                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"[id{user_id}|{name}], вам выдана новая ачивка:\n\n"
                                                     f"{ach[0]}\n\n📊 Рейтинг: {res[2]}",
                                             random_id=0)
        except Exception as e:
            print(traceback.format_exc())


achievements = command_besed.Command()

achievements.keys = ['/ачивка', '/достижение', '/награда']
achievements.description = 'Глобальный бан'
achievements.process = achievement
achievements.topics_blocks = []
achievements.topics_resolution = ["tema1"]
