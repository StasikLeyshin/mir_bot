

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin



class UserProfile(WorkUser):


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
            "type": "profile"
        }
        return log_dict

    async def _get_user_profile(self, user_id: int, peer_id: int = 0):
        user_id_new = self.user_id
        if self.user_id != user_id:
            await self.get_user(self.user_id)
            user_info = self.users_info[self.user_id].user
            user_info_cmd = await self.lvl_cmd_add_list(user_info.class_dict, "profile")
            if user_info_cmd["profile"]["is_another_user"]:
                user_id_new = user_id
            else:
                is_admin = await self.is_admin(self.user_id, str(peer_id))
                if is_admin["flag"]:
                    user_id_new = user_id
        warn = ""
        ban = ""

        # info = await self.manager_db.user_get_one(user_id_new, self.users_documents)
        # if not info:
        #     info = await self.manager_db.user_get_one(user_id_new, f"{peer_id}")
        #     if not info:
        #         msg = "👽 Такого пользователя не существует"
        #         return_dict = {"message": msg}
        #         return return_dict
        #print(user_id_new)
        res = await self.is_empty_user(user_id_new, peer_id)
        if res and not self.is_telegram:
            return res

        await self.get_user(user_id_new)
        await self.get_user_conversation(user_id_new, f"{peer_id}")

        user_info_dict = self.users_info[user_id_new].user.class_dict
        user_info = self.users_info[user_id_new].user



        lvl_list = await self.lvl_list(user_info.xp)

        if peer_id != 0:
            await self.get_user_conversation(user_id_new, f"{peer_id}")
            user_conversation = self.users_info[user_id_new].user_conversation[f"{peer_id}"]
            user_conversation_dict = self.users_info[user_id_new].user_conversation[f"{peer_id}"].class_dict
            if user_conversation.punishments["warn"]:
                if len(user_conversation_dict["punishments"]["warn"]["warn_list"]) != 0:
                    warn += f"☢ Варны: [{len(user_conversation_dict['punishments']['warn']['warn_list'])}/{lvl_list['limit']['warn_limit']}]\n"
                if user_info_dict['punishments']['warn'].get('count'):
                    warn += f"🤡 Количество варнов: {user_info_dict['punishments']['warn']['count']}\n\n"

            if user_info.punishments["ban"] and user_info_dict['punishments']['ban'].get('count'):
                ban += f"🤡 Количество банов: {user_info_dict['punishments']['ban']['count']}\n\n"

        achievements = f"👻 Количество ачивок: {len(user_info_dict['achievements'])}"

        xp = f"📊 XP: {round(user_info_dict['xp'], 2)}"
        coins = f"💰 Монеты: {user_info_dict['coins']}"
        tribe_points = f"🌐 Репутация в клане: {user_info_dict['tribe_points']}"
        influence = f"😎 Репутация: {user_info_dict['influence']}"
        ban_attempts = f"💣 Количество попыток разбана: {abs(user_info_dict['ban_attempts'])}"
        tribe = f"👥 Клан: {self.tribes[user_info_dict['tribe']]}"
        count_sms = f"💬 Количество сообщений: {user_info_dict['number_sms']['text']}"
        count_sms_spam = f"🗣 Количество спам сообщений: {user_info_dict['number_sms']['spam']}"
        count_sms_swear = f"🤬 Количество оскорбительных сообщений: " \
                          f"{user_info_dict['number_sms']['swear'] + user_info_dict['number_sms']['swear_forward_message']}"
        count_sms_sticker = f"👾 Количество стикер-сообщений: {user_info_dict['number_sms']['sticker']}"

        lvl = f"💹 lvl {lvl_list['lvl']} ["
        for i in range(1, 21):
            if lvl_list["lvl_percent_short"] >= i:
                lvl += "*"
            else:
                lvl += "-"
        lvl += f"] lvl {lvl_list['lvl'] + 1}"

        if self.is_telegram:
            msg = "👤 Профиль {0}\n\n"
        else:
            msg = "👤 Профиль [id" + str(user_id_new) + "|{0}]\n\n"
        msg += f"{lvl}\n\n{warn}{ban}{achievements}\n\n{xp}\n{coins}\n{influence}\n{ban_attempts}\n\n" \
               f"{tribe}\n{tribe_points}\n\n{count_sms}\n{count_sms_spam}\n{count_sms_swear}\n{count_sms_sticker}"

        if user_info.cmd["profile"].get("count"):
            user_info.cmd["profile"]["count"] += 1
        else:
            user_info.cmd["profile"]["count"] = 1
        user_info.update = True
        user_info.log["profile"].append(await self.get_log_users(user_id_new, peer_id))

        await self.add_log(await self.get_log_general(user_id_new, peer_id))

        return_dict = {"message": msg, "user_id": user_id_new}
        return return_dict


def current_time_zero():
    tek = DT.datetime.now()
    dt = DT.datetime.fromisoformat(tek.strftime('%Y-%m-%d'))
    return str(dt.timestamp())[:-2]

if __name__ == "__main__23":
    import datetime as DT
    tek = DT.datetime.now()
    dt = DT.datetime.fromisoformat(tek.strftime('%Y-%m-%d'))
    print(int(current_time_zero()) + 86400)
    #str(dt.timestamp())[:-2]



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

    ban = UserProfile(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(user_id=44, peer_id=2000001))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
