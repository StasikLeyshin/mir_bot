
import traceback

import command_ls
from commands import commands
from api import api_url, api, photo_upload

class answer_admin(commands):

    async def run(self):
        try:
            if "payload" in self.message and self.from_id in self.admin_list:
                print("test")
                spis = self.message["payload"].replace('"', '').split("@")
                user_id = spis[0]
                count_id = spis[1]
                result = await self.create_mongo.admin_answer_otv(user_id, self.from_id, self.text, count_id, self.date)
                if result:
                    # await self.apis.api_post("messages.send", v=self.v, peer_id=user_id,
                    #                          message=self.text,
                    #                          random_id=0)
                    for i in result[1]:
                        if int(i) != int(self.from_id):
                            await self.apis.api_post("messages.edit", v=self.v, peer_id=int(i),
                                                     message="Администратор начал отвечать на вопрос.", random_id=0,
                                                     message_id=result[1][i],
                                                     keep_forward_messages=1)
                    if result[4]:
                        for j in result[4]:
                            await self.apis.api_post("messages.edit", v=self.v, peer_id=int(j),
                                                     message="👤 Пользователь задал вопрос, чтобы ответить на вопрос нажмите на кнопку и напишите текст ответа.", random_id=0,
                                                     message_id=result[4][j],
                                                     keyboard=self.keyboard_answer_admin(f"{self.from_id}@{result[5]}"),
                                                     keep_forward_messages=1)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="Вы начали отвечать на данный вопрос, напишите ответ.", random_id=0,
                                             forward=self.answer_msg_other_parameters(user_id, result[3]))

        except Exception as e:
            print(traceback.format_exc())





answer_admins = command_ls.Command()

answer_admins.keys = ['ответить', '/ответить']
answer_admins.description = 'Ответ админа на вопрос'
answer_admins.process = answer_admin
answer_admins.topics_blocks = []
answer_admins.topics_resolution = ["tema1"]
