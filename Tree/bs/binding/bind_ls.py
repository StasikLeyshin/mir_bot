
from commands import commands
import command_ls


class BindLs(commands):

    async def run(self):
        if self.from_id == 597624554:
            for i in range(2000000060, 2000000120):
                try:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=i,
                                             message="начнём", random_id=0)
                except:
                    pass



bind_lss = command_ls.Command()

bind_lss.keys = ['/начать привязку']
bind_lss.description = 'начать привязку'

bind_lss.process = BindLs
#endless_questionss.mandatory = True
bind_lss.topics_blocks = []
bind_lss.topics_resolution = ["zluka"]
