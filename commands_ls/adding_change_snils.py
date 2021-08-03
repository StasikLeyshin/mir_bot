import traceback

import command_ls
from commands import commands

class adding_change_snils(commands):

    async def run(self):
        try:
            chek = self.create_mongo.check_user(self.peer_id)
            flag = 0
            if chek == 6:
                flag = 2
            await self.create_mongo.users_directions_add_start(self.from_id)
            msg = await self.snils_check(self.text, flag=flag)
            g = 1
            for i in msg[1]:
                if flag != 2:
                    if g == len(msg[1]):
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message="\n\n".join(i),
                                                 random_id=0,
                                                 keyboard=self.competition(msg[0]))
                        continue
                    else:
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message="\n\n".join(i),
                                                 random_id=0)
                        continue
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="\n\n".join(i),
                                             random_id=0)
        except Exception as e:
            print(traceback.format_exc())
