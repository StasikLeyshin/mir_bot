import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.punishments import BanGive
from summer_module.transformation.give_points import GivePoints


class ban(commands):

    async def run(self):
        try:

            user_id = await self.getting_user_id()
            if user_id:
                value = await self.getting_number(999999)
                text_list = self.text.lower().split(" ")
                type_points_dict = {
                    ("xp", "очки"): "xp",
                    ("coins", "монеты"): "coins",
                    ("tribe_points", "трайб поинты"): "tribe_points",
                    ("influence", "репутация"): "influence"
                }
                flag = False
                type_points = ""
                for i in text_list:
                    for j in type_points_dict:
                        if i in j:
                            type_points = type_points_dict[j]
                            flag = True
                            break
                    if flag:
                        break
                give_points = GivePoints(self.mongo_manager, self.settings_info, self.from_id, self.date)
                result = await give_points.run(user_id=int(user_id), peer_id=self.peer_id, type_points=type_points,
                                               value=value)
                if result["message"]:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=result['message'],
                                             random_id=0, keyboard=self.pusto())


        except Exception as e:
            print(traceback.format_exc())





bans = command_besed.Command()

bans.keys = ['/give', '/выдать']
bans.description = 'Выдача Очков'
bans.set_dictionary('give_points')
bans.loyal = True
bans.process = ban
bans.topics_blocks = []
bans.topics_resolution = ["tema1"]

if __name__ == "__main__":

    str = "{0}test 228"
    print(str.format("test"))
