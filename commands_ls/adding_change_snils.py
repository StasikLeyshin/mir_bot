import command_ls
from commands import commands


class adding_change_snils(commands):

    async def run(self):
        chek = self.create_mongo.check_user(self.peer_id)
        flag = 0
        if chek == 6:
            flag = 2
        await self.create_mongo.users_directions_add_start(self.from_id)
        msg = await self.snils_check(self.text, flag=flag)
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=msg[1],
                                 random_id=0,
                                 keyboard=self.competition(msg[0]))
