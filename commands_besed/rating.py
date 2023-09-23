import traceback

import command_besed
from commands import commands

class rating(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            res = await self.create_mongo.profile_users_add(self.from_id)
            if adm:
                msg = await self.info_rating(25)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=msg, random_id=0)
                return
            if res[1] > 35:
                if await self.ls_open_check(self.from_id):
                    msg = await self.info_rating(25)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=msg, random_id=0)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             random_id=0)

        except Exception as e:
            print(traceback.format_exc())




ratings = command_besed.Command()

ratings.keys = ['/рейтингrtrtrt', '/ratingrtrtwrtwrt']
ratings.description = 'Рейтинг'
ratings.process = rating
ratings.topics_blocks = []
ratings.topics_resolution = ["tema1"]
