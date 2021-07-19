import command_ls
from commands import commands


class add_snils_anonymously(commands):

    async def run(self):
        self.create_mongo.add_user(self.peer_id, 6)
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="Введите СНИЛС/уникальный номер",
                                 random_id=0)


add_snils_anonymouslys = command_ls.Command()

add_snils_anonymouslys.keys = ['посмотреть анонимно']
add_snils_anonymouslys.description = 'посмотреть анонимно по снилсу'
add_snils_anonymouslys.process = add_snils_anonymously
add_snils_anonymouslys.topics_blocks = []
add_snils_anonymouslys.topics_resolution = ["tema1"]
