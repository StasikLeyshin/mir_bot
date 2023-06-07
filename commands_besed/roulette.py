
import json
import traceback
from datetime import datetime
import random
import asyncio

import command_besed
from commands import commands
from api import api_url, api, photo_upload
from punishments import ban_give_out
from api.api_execute import kick


class roulette(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"😎 ВЫ ПОБЕДИЛИ, БЕЗОГОВОРОЧНО ПОБЕДИЛИ, +1000000ККККК ВАМ НА СЧЁТ", random_id=0)
                return
            res = await self.create_mongo.profile_users_add(self.from_id)
            if res[1] < -10:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"⛔ Вам запрещено участие в рулетке. Слишком мало баллов.",
                                         random_id=0)
                return
            res = await self.create_mongo.profile_users_add(self.from_id, roulette=self.date, f=3)
            if not res[0]:
                timestamp = res[1][0]
                value = datetime.fromtimestamp(timestamp)
                time = value.strftime('%d.%m.%Y %H:%M')
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"🔌 Ваш пистолет на подзарядке, приходите после {time}", random_id=0)
                return
            if res[0]:
                txt = await self.txt_roulette(self.text)
                if not txt:
                    txt = 1
                if self.is_int(txt):
                    if int(txt) >= 1:
                        if int(txt) < 6:
                            ran = random.randint(1, 6)
                            if ran > int(txt):
                                ach = ""
                                res = await self.create_mongo.profile_users_add(self.from_id, roulette=self.date)
                                bal = await self.create_mongo.profile_users_add(self.from_id, scores=int(txt) * 2)
                                if res[1] in self.roulette_awards:
                                    res_new = await self.create_mongo.profile_users_add(self.from_id,
                                                                                        f"{self.roulette_awards[int(res[1])][0]}",
                                                                                        self.roulette_awards[int(res[1])][1])
                                    ach = f"\n\n👻 [id{self.from_id}|Вы] получили ачивку:\n\n{self.roulette_awards[int(res[1])][0]}\n\n" \
                                          f"📊 Рейтинг: {res_new[1]}"
                                else:
                                    ach = f"\n\n📊 Рейтинг: {bal[1]}"
                                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                         message=f"🤠 Сегодня фортуна на вашей стороне, вы победили.{ach}",
                                                         random_id=0)
                            else:
                                res = await self.create_mongo.profile_users_add(self.from_id, roulette=self.date, f=4)
                                bal = await self.create_mongo.profile_users_add(self.from_id, scores=-8)
                                # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                #                          message=f"К сожалению вы проиграли.{ach}",
                                #                          random_id=0)

                                result = await self.ban_rating(self.from_id, "-5411326", bal[1], self.peer_id,
                                                               "Рейтинг достиг отметки ниже -30", self.date)
                                if not result:
                                    ach = f"\n\n📊 Рейтинг: {bal[1]}"
                                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                             message=f"😭 К сожалению вы проиграли.{ach}",
                                                             random_id=0)
                                    return
                                else:
                                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                             message=f"{result[1]}",
                                                             random_id=0)
                                # vrem = 86400
                                # cause = "Проигрыш в рулетке"
                                # ply = await self.display_time(vrem)
                                #result = await ban_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id,
                                #                                              cause,
                                #                                              self.chat_id(),
                                #                                              str(self.from_id), "-5411326", vrem, ply)
                                # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                #                          message=result[1], random_id=0)

                                if len(result) == 3:
                                    loop = asyncio.get_running_loop()
                                    for i in result[2]:
                                        try:
                                            loop.create_task(
                                                self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                                                                   member_id=self.from_id,
                                                                   v=self.v))
                                        except:
                                            pass
                                    return

                                if result[0]:
                                    await self.apis.api_post("execute", code=kick(users=[self.from_id], chat_id=self.chat_id()),
                                                             v=self.v)
                                return

                        else:
                            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                     message=f"😳 Как я столько пуль в барабан заряжу, только если солью или дробью, но так не интересно",
                                                     random_id=0)
                    elif int(txt) == 0:
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message=f"Холостой пистолет не заряжаем",
                                                 random_id=0)
                    else:
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message=f"😳 Это куда ж минус то, пуля назад лететь будет??",
                                                 random_id=0)
        except Exception as e:
            print(traceback.format_exc())









roulettes = command_besed.Command()

roulettes.keys = ['/roulette', '/рулетка']
roulettes.description = 'Для тестов'
roulettes.process = roulette
roulettes.topics_blocks = []
roulettes.topics_resolution = ["tema1"]
