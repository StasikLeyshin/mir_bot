
import command_besed
from commands import commands

class conversation_zluka(commands):

    async def run(self):
        adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)
        if "174516461" in str(self.from_id) or adm == 1:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=f"{self.peer_id} Держи родная ☺", random_id=0)



conversation_zlukas = command_besed.Command()

conversation_zlukas.keys = ['начнём']
conversation_zlukas.description = 'Отправка id беседы злюке'
conversation_zlukas.process = conversation_zluka
conversation_zlukas.topics_blocks = []
conversation_zlukas.topics_resolution = ["tema1"]
