
import json
import traceback
import requests

import command_besed
from commands import commands
from api import api_url, api, photo_upload


class user_info(commands):


    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                user_id = await self.getting_user_id()
                if not user_id:
                    user_id = self.from_id

                msg = await self.info_user(user_id)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=msg, random_id=0)
                return
            res = await self.create_mongo.profile_users_add(self.from_id)
            if res[1] > 20:
                if await self.ls_open_check(self.from_id):
                    user_id = await self.getting_user_id()
                    if not user_id:
                        user_id = self.from_id
                    msg = await self.info_user(user_id)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=msg, random_id=0)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             random_id=0)

            else:
                if await self.ls_open_check(self.from_id):
                    msg = await self.info_user(self.from_id, res)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=msg, random_id=0)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             random_id=0)

                #user_id = await self.getting_user_id()
                # info = await self.create_mongo.user_info(self.from_id, self.peer_id)
                #
                # result = await self.apis.api_post("users.get", v=self.v, user_ids=f"{self.from_id}", name_case="gen")
                # name = f'{result[0]["first_name"]} {result[0]["last_name"]}'
                #
                # res = await self.create_mongo.profile_users_add(self.from_id)
                #
                # warn = ""
                # ban = ""
                # if "count_old" in info["warn"]:
                #     warn = f"☢ Варны: [{info['warn']['count']}/3]\n🤡 Количество варнов: {info['warn']['count_old']}\n\n"
                # if "count" in info["ban"]:
                #     ban = f"🤡 Количество банов: {info['ban']['count']}\n\n"
                #
                # awards = ""
                # if len(res[0]) >= 1:
                #     if res[0][0] == "0":
                #         awards = f"📊 Рейтинг: {res[1]}\n👻 Ачивки:\n📛 Ачивок нет"
                #     else:
                #         awards = f"📊 Рейтинг: {res[1]}\n👻 Ачивки:\n" + "\n".join(res[0][0])
                #
                # #p = requests.get('https://vk.com/foaf.php?id=' + str(self.from_id))
                # s = await api_url('https://vk.com/foaf.php?id=' + str(self.from_id)).get_html()
                # l = self.fin(s, "<ya:created dc:date=", "/>\n")
                # q = l[1:-7]
                # q = q[:-9]
                # q = q.replace('-', '.')
                # q = q.split(".")
                # q = str(q[2]) + "." + str(q[1]) + "." + str(q[0])

                # if info:
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                              message=f"👤 Профиль [id{self.from_id}|{name}]\n\n"
                #                                      f"📆 Дата регистрации: {q}\n\n"
                #                                      f"{warn}{ban}{awards}",
                #                              random_id=0)

                # msg = await self.info_user(self.from_id)
                # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                          message=msg, random_id=0)
        except Exception as e:
            print(traceback.format_exc())








user_infos = command_besed.Command()

user_infos.keys = ['/профиль']
user_infos.description = 'Для тестов'
user_infos.process = user_info
user_infos.topics_blocks = []
user_infos.topics_resolution = ["tema1"]


