
import command_besed
from commands import commands

class outgoing(commands):

    async def run(self):

        if self.message["action"]["member_id"] == self.from_id:
            await self.create_mongo.remove_user_bs(self.from_id, self.peer_id, f=0)
        else:
            await self.create_mongo.remove_user_bs(self.message["action"]["member_id"], self.peer_id, f=1)



outgoings = command_besed.Command()

outgoings.keys = ['chat_kick_user']
outgoings.description = 'Исключение или выход пользователя'
outgoings.process = outgoing
outgoings.topics_blocks = []
outgoings.topics_resolution = ["zluka"]
