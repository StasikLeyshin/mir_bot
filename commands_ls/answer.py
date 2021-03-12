

import command_ls
from commands import commands
from api import api_url, api, photo_upload

class answer(commands):

    async def run(self):

        user_chek = self.create_mongo.users_get_chek(self.peer_id)
        if user_chek == 1:
            text_spis = self.text.split(" ")
            if len(text_spis) >= 3:
                ans = self.create_mongo.answer(text_spis[1])
                if ans == 1:
                    ans_chek = self.create_mongo.answer_chek(self.peer_id, text_spis[1])
                    if ans_chek[0] == 1:
                        #del text_spis[:-2]
                        del text_spis[0]
                        del text_spis[0]
                        await api_url(f"{self.url_dj}").post_json(answer=" ".join(text_spis), user_id_mongo=ans_chek[1],
                                                                  number=ans_chek[2])
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message=f"✏ Ваш ответ на вопрос успешно записан",
                                                 random_id=0)
                elif ans == 0:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"😳 Вы сумели ответить на несуществующий вопрос, да вы хацкер!",
                                             attachment="video327673759_456239046",
                                             random_id=0)
                elif ans == 2:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"⏰ Тик-так, тик-так, время на ответ уже ушло:(",
                                             random_id=0)


answers = command_ls.Command()

answers.keys = ['ответ', '/ответ']
answers.description = 'Ответ'
answers.process = answer
answers.topics_blocks = []
answers.topics_resolution = ["consultants"]
