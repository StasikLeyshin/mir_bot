import command_ls
from commands import commands


class help(commands):

    async def run(self):

        chek = self.create_mongo.check_user(self.peer_id)

        if chek != 0:
            self.create_mongo.add_user(self.peer_id, 0)

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="🌐 Команды бота:\n\n"
                                         "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n"
                                         "📈 Направления — подберёт перспективные направления по проходным баллам",
                                 random_id=0,
                                 keyboard=self.menu())



helps = command_ls.Command()

helps.keys = ['команды', 'начать', 'help']
helps.description = 'Вопросы'
helps.process = help
helps.topics_blocks = []
helps.topics_resolution = ["tema1"]
