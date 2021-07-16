
import command_ls
from commands import commands

class user_info(commands):

    async def run(self):
        res = await self.create_mongo.profile_users_add(self.from_id)
        if res[1] > 20:
            user_id = await self.getting_user_id()
            if not user_id:
                user_id = self.from_id
            msg = await self.info_user(user_id, f=1)

            await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                     message=msg, random_id=0)
        else:
            msg = await self.info_user(self.from_id, f=1, res=res)
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                     message=msg, random_id=0)


user_infos = command_ls.Command()

user_infos.keys = ['/профиль']
user_infos.description = 'Профиль'
user_infos.process = user_info
user_infos.topics_blocks = ["target", "consultants"]
user_infos.topics_resolution = []
