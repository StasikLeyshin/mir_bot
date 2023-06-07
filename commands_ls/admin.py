
import command_ls
from commands import commands
from api import api_url, api, photo_upload

class admin(commands):

    async def run(self):
        if self.from_id not in self.admin_list:
            nom = await self.create_mongo.admin_answer_check(self.from_id)
            slov = {}
            for i in self.admin_list:
                msg = await self.apis.api_post("messages.send", v=self.v, peer_id=i,
                                               message="👤 Пользователь задал вопрос, чтобы ответить на вопрос нажмите на кнопку и напишите текст ответа.",
                                               random_id=0,
                                               keyboard=self.keyboard_answer_admin(f"{self.from_id}@{nom}"),
                                               forward=self.answer_msg_other_parameters(self.peer_id, self.conversation_message_id))
                slov[f"{i}"] = msg

            await self.create_mongo.admin_answer_add(self.from_id, self.text, self.message_id, self.conversation_message_id,
                                                     slov, self.date)
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="✅ Вопрос администратору успешно отправлен. Ожидайте ответа.", random_id=0,
                                     forward=self.answer_msg())






admins = command_ls.Command()

admins.keys = ['админ5аккпкпку', '/админк45пр65654е', '?еп45пкекеп']
admins.fully = True
admins.description = 'Перессылка сообщений админу'
admins.process = admin
admins.topics_blocks = []
admins.topics_resolution = ["tema1", "mirea_official"]
