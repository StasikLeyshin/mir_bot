from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.punishments.unban import UnbanLs
from summer_module.user_profile import UserProfile
from summer_module.work_ls.work_ls import WorkLs
from api import api


class UserProfileLs(commands):

    async def run(self):
        user_id = await self.getting_user_id()
        if not user_id:
            user_id = self.from_id
        user_info = UserProfile(self.mongo_manager, self.settings_info, self.from_id, self.date)
        result = await user_info.run(user_id=int(user_id), peer_id=0)

        name = ""
        if result.get("user_id"):
            res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{result['user_id']}",
                                           name_case="gen")
            name = f'{res[0]["first_name"]} {res[0]["last_name"]}'

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                 message=result["message"].format(name), random_id=0)






automatic_unbans = command_ls.Command()

automatic_unbans.keys = ['inf', 'info', 'профиль']
automatic_unbans.description = 'профиль пользователя'
automatic_unbans.process = UserProfileLs
#endless_questionss.mandatory = True
automatic_unbans.topics_blocks = []
automatic_unbans.topics_resolution = ["tema1"]

