
from datetime import datetime


from summer_module.user_conversation import WorkUser, UserLs
import numpy as np


class WorkLs(WorkUser):

    #@checking_admin
    # async def run(self, **kwargs):
    #
    #     return_dict = await self._unban(peer_id_number, answer_number)
    #     await self.update_all_user_new()
    #     return return_dict

    def __init__(self, manager_db, settings_info=None, user_id: int = 0, current_time: int = 0, users_info=None):
        super().__init__(manager_db, settings_info, user_id, current_time, users_info)
        self.user_ls = None

    async def location_tree_check(self):
        #print(self.manager_db)
        self.user_ls = UserLs(user_id=self.user_id)
        self.user_ls.self_generator(await self.manager_db.user_insert_one(self.user_ls.class_dict,
                                                                          self.work_ls_documents))
        return self.user_ls

    async def location_tree_set(self, location_tree):
        self.user_ls.location_tree = location_tree
        await self.manager_db.user_update_one(self.user_ls.class_dict, self.work_ls_documents)

    async def location_tree_update(self):
        await self.manager_db.user_update_one(self.user_ls.class_dict, self.work_ls_documents)




    async def get_log_users(self, user_id, peer_id, action, cause, finish_time, time_plus):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "action": action,
            "cause": cause,
            "finish_time": finish_time,
            "time_plus": time_plus
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, action, cause, finish_time, time_plus):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "ban",
            "action": action,
            "cause": cause,
            "finish_time": finish_time,
            "time_plus": time_plus
        }
        return log_dict


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

    unban = UnbanLs(mongo_manager, settings_info,  123456, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(unban.record_list_peer_ids())
    #test2 = loop.run_until_complete(unban.run(answer_number=4))
    #test2 = loop.run_until_complete(unban.task_user_bot_unban())
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)

