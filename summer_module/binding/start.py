
from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import BanGive
from summer_module.user_conversation import WorkUser, checking_admin, User_conversation


def users_chek():
    #response = await apis.api_get("messages.getConversationMembers", peer_id=peer_id, v=self.v)
    #if "error" not in response:
    users = []
    users_vse = []
    users_adm = []
    response = {"items": [{"is_admin": True, "member_id": 123}, {"member_id": 44}, {"member_id": 1234}]}
    for element in response["items"]:
        if element.get("is_admin"):
            users.append({"user_id": element["member_id"], "admin": True})
            #users[element["member_id"]] = {"admin": True}
            users_adm.append(element["member_id"])
            # users.append({"user_id": element["member_id"], "admin": True})
            users_vse.append(element["member_id"])
        else:
            users.append({"user_id": element["member_id"], "admin": False})
            #users[element["member_id"]] = {"admin": False}
            # users.append({"user_id": element["member_id"], "admin": False})
            users_vse.append(element["member_id"])

    return users, users_vse, users_adm
    #return False


class Start(WorkUser):

    async def run(self, peer_id: int, users: list, users_all: list, user_admins: list):
        #return_dict = await self._start_user_conversation(peer_id, users)
        #return return_dict

        #res = await users_chek()
        #print(res)
        return await self._start_user_conversation(peer_id, users, users_all, user_admins)

    async def _start_user_conversation(self, peer_id: int, users: list, users_all: list, user_admins: list):
        users_new = []
        for i in users:
            users_new.append(User_conversation(user_id=i['user_id'],
                                               start_time=self.current_time,
                                               admin=i['admin']).class_dict)
            await self.get_user(user_id=i['user_id'])
            user_info = self.users_info[i['user_id']].user
            if user_info.tribe == "NoName":
                user_info.tribe = await self.get_tribe()
                user_info.update = True
                await self.update_all_user_new()


        await self.manager_db.user_insert_update_all(users_new, users_all, user_admins, str(peer_id))

        await self.get_peer_ids(peer_id)

        msg = "✅ Данные успешно обновлены."

        return_dict = {"message": msg, "action": False, "update": False}
        return return_dict

    async def get_all_peer_ids(self):
        result = await self.manager_db.peer_ids_get_all(self.peer_ids)
        return result


if __name__ == "__main__11":
    tribes = {"name": 0, "name2": 0, "name3": 0, "name4": 0}
    #key = min(tribes, key=lambda k: tribes[k])
    minval = min(tribes.values())
    res = [k for k, v in tribes.items() if v == minval]
    print(res)


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

    #ban = BanGive(mongo_manager, settings_info,  55, 100)
    #con = ConversationInput(mongo_manager, settings_info,  55, 100)
    con = Start(mongo_manager, settings_info)

    res = users_chek()
    users_all = res[1]
    print(res)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(con.run(peer_id=2000001, users=res[0], users_all=users_all, user_admins=res[2]))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
