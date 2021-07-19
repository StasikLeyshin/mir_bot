import command_ls
from commands import commands


class add_snils(commands):

    async def run(self):
        self.create_mongo.add_user(self.peer_id, 5)
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="Введите ваш СНИЛС/уникальный номер",
                                 random_id=0)


add_snilss = command_ls.Command()

add_snilss.keys = ['Добавить СНИЛС/уникальный номер', 'Изменить СНИЛС/уникальный номер']
add_snilss.description = 'Ответ на конкурс'
add_snilss.process = add_snils
add_snilss.topics_blocks = []
add_snilss.topics_resolution = ["tema1"]
