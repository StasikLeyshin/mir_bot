import os
import asyncio
import time

import command_ls
from commands import commands
from api import api_url, api, photo_upload

class answers_img(commands):

    async def run(self):
        '''files = os.listdir("generating_questions/img")
        post = ""
        loop = asyncio.get_running_loop()
        for i in files:
            if "png" in i:
                try:
                    res = loop.create_task(photo_upload(self.apis,
                                         self.v, self.peer_id,
                                         f"{i}",
                                         "generating_questions/img/").upload())
                    #print(res)
                    """res = await photo_upload(self.apis,
                                         self.v, self.peer_id,
                                         f"{i}",
                                         "generating_questions/img/").upload()"""
                except Exception as e:
                    print(e)
                #print(res)
                if len(post) > 1:
                    post += f",{res}"
                else:
                    post += f"{res}"
        #await time.sleep(2)
        print(post)'''
        #print(1111111111111)
        vopr = self.create_mongo.questions_get()
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=f"✏ Чтобы узнать ответ на вопрос, напишите номер интересующего вас вопроса.\n{vopr}",
                                 random_id=0)




answers_imgs = command_ls.Command()

answers_imgs.keys = ['вопросы', 'вопр']
answers_imgs.description = 'Вопросы'
answers_imgs.process = answers_img
answers_imgs.topics_blocks = ["target", "consultants"]
answers_imgs.topics_resolution = []
