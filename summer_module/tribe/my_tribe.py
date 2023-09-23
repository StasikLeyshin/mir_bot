

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin, Tribe


class MyTribe(WorkUser):


    async def run(self, peer_id: int, **kwargs):


        return_dict = await self._get_tribe_rating(peer_id)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "my_tribe"
        }
        return log_dict

    def get_name(self, dictionary):
        return dictionary['tribe_points']

    async def _get_tribe_rating(self, peer_id: int = 0):
        await self.get_user(self.user_id)
        user_info = self.users_info[self.user_id].user
        user_info_cmd = await self.lvl_cmd_add_list(user_info.class_dict, "my_tribe")
        msg = ""
        error = False
        user_ids = []
        if "my_tribe" in user_info_cmd or (await self.is_admin(self.user_id, str(peer_id)))['flag']:

            #tribe = Tribe(cut=user_info.tribe)
            #tribe.self_generator(await self.manager_db.tribe_insert_one(tribe.class_dict, self.tribe_documents))
            count = 0
            users_list = await self.manager_db.tribe_users_get(user_info.tribe, self.users_documents)
            #print(users_list)
            for i in users_list:
                count += i['tribe_points']
            #users_list.sort(key=self.get_name)
            users_list = sorted(users_list, key=self.get_name, reverse=True)
            #print(users_list)

            k = 0
            people_list = []
            user_ids = []
            for i in users_list:
                if k == 25:
                    break
                people_list.append(str(k + 1) + ". -- " + f"[id{i['user_id']}|" + "{users[" + str(k) + "]} -- " + "]" + str(i['tribe_points']))
                user_ids.append(i['user_id'])
                k += 1

            msg = f"👥 Ваш Клан: {self.tribes[user_info.tribe]}\n🌐 Очки клана: {count}\n\n" \
                  f"👑 Топ 25 участников:\n" + "\n".join(people_list)

            if user_info.cmd["my_tribe"].get("count"):
                user_info.cmd["my_tribe"]["count"] += 1
            else:
                user_info.cmd["my_tribe"]["count"] = 1
            user_info.update = True

            await self.add_log_user(user_info, "my_tribe", await self.get_log_users(self.user_id, peer_id))

            #user_info.log["my_tribe"].append(await self.get_log_users(user_id_new, peer_id))

            await self.add_log(await self.get_log_general(self.user_id, peer_id))
        else:
            error = True
        return_dict = {"message": msg, "error": error, "user_ids": user_ids}
        return return_dict




if __name__ == "__main__":
    # der = [-1, -14, 0, 0, 23, 32]
    # der.sort()
    # print(sorted(der, reverse=True))

    st = "{users[0]}   {users[1]}  {users[2]}".format(users=[1, 2, 3])
    print(st)

if __name__ == "__main__11":
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

    ban = MyTribe(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(peer_id=2000001))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
