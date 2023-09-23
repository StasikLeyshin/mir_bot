

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin



class Achievements(WorkUser):


    async def run(self, user_id: int, peer_id: int, **kwargs):


        return_dict = await self._get_achievements(user_id, peer_id)
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
            "type": "achievements"
        }
        return log_dict

    async def _get_achievements(self, user_id: int, peer_id: int = 0):
        user_id_new = self.user_id
        if self.user_id != user_id:
            await self.get_user(self.user_id)
            user_info = self.users_info[self.user_id].user
            user_info_cmd = await self.lvl_cmd_add_list(user_info.class_dict, "achievements")
            if user_info_cmd["achievements"]["is_another_user"]:
                user_id_new = user_id
            else:
                is_admin = await self.is_admin(self.user_id, str(peer_id))
                if is_admin["flag"]:
                    user_id_new = user_id

        res = await self.is_empty_user(user_id_new, peer_id)
        if res and not self.is_telegram:
            return res

        await self.get_user(user_id_new)
        await self.get_user_conversation(user_id_new, f"{peer_id}")

        user_info_dict = self.users_info[user_id_new].user.class_dict
        user_info = self.users_info[user_id_new].user

        #print(user_info_dict['achievements'])

        if len(user_info_dict['achievements']) != 0:
            achievements = f"👻 Количество ачивок: {len(user_info_dict['achievements'])}\n\n"
            achievements_list = "\n\n".join([i["text"] + ' -- ' + str(i["xp"]) for i in user_info_dict['achievements']])
            achievements_msg = achievements + achievements_list
        else:
            achievements_msg = "😪 Ачивок нет"


        if self.is_telegram:
            msg = "👤 Ачивки {0}\n\n"
        else:
            msg = "👤 Ачивки [id" + str(user_id_new) + "|{0}]\n\n"
        msg += f"{achievements_msg}"

        user_info.update = True
        await self.set_count_cmd(user_info, "achievements")

        await self.add_log_user(user_info, "achievements",
                                await self.get_log_users(user_id_new, peer_id))

        await self.add_log(await self.get_log_general(user_id_new, peer_id))

        return_dict = {"message": msg, "user_id": user_id_new}
        return return_dict



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

    ban = Achievements(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(user_id=123456, peer_id=2000001))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
