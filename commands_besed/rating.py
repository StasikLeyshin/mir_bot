import traceback

import command_besed
from commands import commands

class rating(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                msg = await self.info_rating(25)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=msg, random_id=0)

        except Exception as e:
            print(traceback.format_exc())




ratings = command_besed.Command()

ratings.keys = ['/рейтинг', '/rating']
ratings.description = 'Рейтинг'
ratings.process = rating
ratings.topics_blocks = []
ratings.topics_resolution = ["tema1"]
