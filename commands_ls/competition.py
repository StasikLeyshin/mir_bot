import command_ls
from commands import commands


class competition(commands):

    async def run(self):
        #self.create_mongo.add_user(self.peer_id, 5)
        res = await self.create_mongo.users_directions_add_start(self.from_id)
        f = 0
        if res:
            f = 1
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="Выберите нужную функцию",
                                 random_id=0,
                                 keyboard=self.competition(f))



competitions = command_ls.Command()

competitions.keys = ['конкурс544545', '/конкурс454545']
competitions.description = 'Ответ на конкурс'
competitions.process = competition
competitions.topics_blocks = []
competitions.topics_resolution = ["tema1"]
