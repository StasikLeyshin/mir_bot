import command_ls
from commands import commands
from api import api_url, api, photo_upload

class response_text_admin(commands):

    async def run(self):
        if self.from_id in self.admin_list:
            result = await self.create_mongo.admin_answer_otv(admin_id=self.from_id, answer=self.text, vrem=self.date,
                                                              f=1)
            if result:
                for i in result[1]:
                    await self.apis.api_post("messages.edit", v=self.v, peer_id=int(i),
                                             message="Администратор ответил на вопрос.", random_id=0,
                                             message_id=result[1][i],
                                             keep_forward_messages=1)

                await self.apis.api_post("messages.send", v=self.v, peer_id=int(result[6]),
                                         message=self.text, random_id=0,
                                         forward=self.answer_msg_parameters(int(result[6]), int(result[3])))
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="Ответ на данный вопрос успешно отправлен.", random_id=0,
                                         forward=self.answer_msg())

response_text_admins = command_ls.Command()

response_text_admins.keys = []
response_text_admins.description = 'Ответ на вопрос администратора'
response_text_admins.name = 'response_text_admin'
#answers.set_dictionary('answer')
response_text_admins.process = response_text_admin
response_text_admins.topics_blocks = []
response_text_admins.topics_resolution = ["tema1", "mirea_official"]
