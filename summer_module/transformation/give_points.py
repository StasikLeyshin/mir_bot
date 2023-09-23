

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin


class GivePoints(WorkUser):

    @checking_admin
    async def run(self, user_id: int, peer_id: int, type_points: str, value: int, **kwargs):


        return_dict = await self._give_points(user_id, peer_id, type_points, value)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id, type_points, value):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "decoding": type_points,
            f"{type_points}": value
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, type_points, value):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "give_points",
            "decoding": type_points,
            f"{type_points}": value
        }
        return log_dict

    async def _give_points(self, user_id, peer_id, type_points, value):
        # res = await self.is_empty_user(user_id, peer_id)
        # if res:
        #     return res

        await self.get_user(user_id)
        user_info = self.users_info[user_id].user
        type_points_dict = {
            "xp": user_info.xp,
            "coins": user_info.coins,
            "tribe_points": user_info.tribe_points,
            "influence": user_info.ban_attempts
        }
        #print(type_points_dict, type_points)
        if type_points in type_points_dict:
            #type_points_dict[type_points] += value
            user_info.__dict__[type_points] += value
            #user_info.coins += value
            user_info.update = True
            #print(user_info.coins)

            await self.add_log_user(user_info, "give_points", await self.get_log_users(self.user_id, peer_id,
                                                                                       type_points, value))

            #user_info.log["give_points"].append(await self.get_log_users(self.user_id, peer_id, type_points))

            await self.add_log_user(self.users_info[self.user_id].admin, "give_points",
                                    await self.get_log_users(user_id, peer_id, type_points, value))
            self.users_info[self.user_id].admin.update = True

            # self.users_info[self.user_id].admin.log["ban"].append(
            #     await self.get_log_users(user_id, peer_id, action, cause, ban_info["finish_time"], time_plus))

            await self.add_log(await self.get_log_general(user_id, peer_id, type_points, value))
            msg = f"✅ Данному [id{user_id}|пользователю] успешно начислено {value} {type_points}"
        else:
            msg = "⚠ Такой параметр не найден"

        return_dict = {"message": msg}

        return return_dict




if __name__ == "__main__23":
    st = {'xp': -38.00000000000001, 'tribe_points': -18, 'influence': -1}
    if st.get('coins') or st.get('coins') == 0:
        print('DA')
    print(st.get('coins'))
if __name__ == "__main__":
    from motor import MotorClient
    from mongodb import MongoManager
    import asyncio
    import yaml
    with open('../description_commands.yaml', encoding="utf-8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
    # pprint(read_data)
    loop = asyncio.get_event_loop()
    uri = 'mongodb://localhost:27017'
    client = MotorClient(uri)

    mongo_manager = MongoManager(client)
    #wok = WorkUser(mongo_manager, 55, 100) self.settings_info = await self.manager_db.settings_get_one(self.settings_documents)

    loop.run_until_complete(mongo_manager.settings_update_one(read_data, "settings"))
    settings_info = loop.run_until_complete(mongo_manager.settings_insert_one(read_data, "settings"))

    # test2 = loop.run_until_complete(wok.lvl_cmd_add_list({"xp": 12345}, "profile"))
    # test2 = loop.run_until_complete(wok.lvl_list({"xp": 700}))
    # test2 = loop.run_until_complete(wok.achievements_check(user_info_list=[123456]))
    # test2 = loop.run_until_complete(wok.add_ban_user(user_id=123456, peer_id=2000001, cause="Спам"))
    #test2 = loop.run_until_complete(wok.add_warn_user(user_id=123456, peer_id=2000001, cause="Спам"))

    #  wok = WorkUser(mongo_manager, settings_info,  55, 100)

    ban = GivePoints(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(user_id=123456, peer_id=2000001, type_points="coins", value=2))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
