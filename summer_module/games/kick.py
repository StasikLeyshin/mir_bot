

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin



class KickGame(WorkUser):


    async def run(self, user_id: int, peer_id: int, **kwargs):


        return_dict = await self._get_user_profile(user_id, peer_id)
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
            "type": "kick_game"
        }
        return log_dict

    async def _get_user_profile(self, user_id: int, peer_id: int = 0):
        kick = False
        return_dict = {"message": "", "kick": kick}
        if self.user_id != user_id:
            user_id_new = user_id
        else:
            return return_dict

        adm = await self.is_admin(user_id_new, str(peer_id))

        if not adm["flag"]:


            await self.get_user(user_id_new)
            await self.get_user(self.user_id)
            #await self.get_user_conversation(user_id_new, f"{peer_id}")

            #user_info_dict = self.users_info[user_id_new].user.class_dict
            user_info = self.users_info[self.user_id].user
            user_info_new = self.users_info[user_id_new].user

            if user_info.tribe != user_info_new.tribe and user_info.tribe != "NoName":
                kick = True

                user_info.update = True

                await self.set_count_cmd(user_info, "kick_game")


                await self.add_log_user(user_info, "kick_game",
                                        await self.get_log_users(user_id_new, peer_id))

                await self.add_log(await self.get_log_general(user_id_new, peer_id))

                return_dict = {"message": "", "kick": kick}

        return return_dict



if __name__ == "__main__":
   d = {'1': 3, '4': 15}
   d.pop('4')
   d.setdefault(5, 'five')
   d.sorted()
   print(d)
if __name__ == "__main__23":
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

    ban = Kick(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(user_id=123456, peer_id=2000001))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
