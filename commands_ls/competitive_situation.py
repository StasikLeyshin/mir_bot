import command_ls
from commands import commands


class competitive_situation(commands):

    async def run(self):
        res = await self.create_mongo.users_directions_add_start(self.from_id)
        if res:
            msg = await self.snils_check(flag=1)
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=msg[1],
                                     random_id=0,
                                     keyboard=self.competition(msg[0]))









competitive_situations = command_ls.Command()

competitive_situations.keys = ['моя ситуация', 'ситуация']
competitive_situations.description = 'Моя ситуация'
competitive_situations.process = competitive_situation
competitive_situations.topics_blocks = []
competitive_situations.topics_resolution = ["tema1"]
