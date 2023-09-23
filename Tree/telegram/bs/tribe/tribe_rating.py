import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.tribe.my_tribe import MyTribe
from summer_module.tribe.tribe_rating import TribeRating
from summer_module.user_profile import UserProfile


class MyTribeBs(commands):

    async def run(self):
        try:

            if await self.ls_open_check(self.from_id):


                user_info = TribeRating(self.mongo_manager, self.settings_info, self.from_id, self.date)
                result = await user_info.run(peer_id=self.peer_id)

                if result.get("message"):
                    name_list = []
                    for i in result["user_ids"]:
                        res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{i}")
                        if len(res) > 0:
                            name = f'{res[0]["first_name"]} {res[0]["last_name"]}'
                            name_list.append(name)
                        else:
                            name_list.append("Неизвестный")
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=result["message"].format(users=name_list), random_id=0)
            else:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                         random_id=0)



        except Exception as e:
            print(traceback.format_exc())





my_tribes = command_besed.Command()

my_tribes.keys = ['rghynmyndtsrtrfedws']
my_tribes.description = 'Рейтинг трайбов'
my_tribes.set_dictionary('tribe_rating')
my_tribes.process = MyTribeBs
my_tribes.topics_blocks = []
my_tribes.topics_resolution = ["tema1"]
