import random

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import WarnGive
from summer_module.user_conversation import WorkUser, checking_admin


class MessageAnalysis(WorkUser):

    async def run(self, peer_id: int, type_sms: str, message: dict, **kwargs):
        #return_dict = await self._add_bs_user(self.user_id, peer_id_zl)
        return_dict = await self._message_analysis(peer_id, type_sms, message)
        await self.update_all_user_new()
        return return_dict

    async def _message_analysis(self, peer_id: int, type_sms: str, message: dict):
        action = False
        update = False
        is_delete = False
        msg = ""
        kick_id = []
        lvl_list = None

        msg_type_sms = {
            "sms_link": {
                "msg": f"⚠ Обнаружена ссылка на подозрительный источник от данного [id{self.user_id}|пользователя]\n"
                       f"👮‍♂ Дальнейшее повторение таких инцидентов может подлежать наказанию.",
                "cause": "Ссылка на подозрительный источник",
                "is_delete": True
            },
            "sms_video_circle": {
                "msg": f"⚠ Использование кружков, товарищ [id{self.user_id}|пользователь], не желательно,\n"
                       f"👮‍♂ Дальнейшее повторение таких инцидентов может подлежать наказанию.",
                "cause": "Использование кружков",
                "is_delete": False
            },
            "sms_voice": {
                "msg": f"⚠ Использование голосовых сообщений, товарищ [id{self.user_id}|пользователь], не желательно,\n"
                       f"👮‍♂ Дальнейшее повторение таких инцидентов может подлежать наказанию.",
                "cause": "Использование голосовых сообщений",
                "is_delete": False
            }

        }

        await self.get_user_conversation(self.user_id, f"{peer_id}")

        await self.get_user(self.user_id)

        user_conversation = self.users_info[self.user_id].user_conversation[f"{peer_id}"]
        user_info = self.users_info[self.user_id].user

        if user_info.number_sms.get(type_sms):
            user_info.number_sms[type_sms] += 1
        else:
            user_info.number_sms[type_sms] = 1
        user_info.update = True
        await self.log_user(peer_id, type_sms, message)

        lvl_list = await self.lvl_list(user_info.xp, user_conversation.role)

        achievements = self.settings_info["sms_awards"]
        await self.give_achievement(self.user_id, user_info.number_sms["text"],
                                    achievements, user_info.achievements, "sms", multiplier=lvl_list["multiplier"],
                                    admin_id=self.club_id)

        await self.set_user_xp(self.user_id, self.users_info[self.user_id].user)

        adm = await self.is_admin(self.user_id, str(peer_id))

        if not adm["flag"]:
            if user_conversation.punishments["ban"].get("status"):
                end_time_msg = await unix_to_time(user_conversation.punishments["ban"]["finish_time"])
                msg = f"⚠ [id{self.user_id}|Вы] находитесь в бане до {end_time_msg}.\n👋 До свидания."
                action = "kick"
                kick_id.append(self.user_id)
                return_dict = {"message": msg, "action": action, "update": update,
                               "kick_id": kick_id, "peer_id": peer_id, "is_delete": is_delete}
                #await self.log_user(peer_id, type_sms)
                return return_dict
            if type_sms == "swear":
                await self.get_admin(self.club_id,
                                     self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1])
                cause = "Использование ненормативной лексики"
                #await self.log_user(peer_id, type_sms)
                return await WarnGive(self.manager_db, self.settings_info, self.club_id, self.current_time,
                                      self.users_info).run(user_id=self.user_id, peer_id=peer_id, cause=cause,
                                                           repeated=True)
            if type_sms == "swear_forward_message":
                await self.get_admin(self.club_id,
                                     self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1])
                cause = "Использование ненормативной лексики в пересланном сообщении"
                #await self.log_user(peer_id, type_sms)
                return await WarnGive(self.manager_db, self.settings_info, self.club_id, self.current_time,
                                      self.users_info).run(user_id=self.user_id, peer_id=peer_id, cause=cause,
                                                           repeated=True)

            if type_sms == "sms_link" or type_sms == "sms_voice" or type_sms == "sms_video_circle":
                #lvl_list = await self.lvl_list(user_info.xp, user_conversation.role)
                if lvl_list["limit"][type_sms] < 0:pass
                    #await self.log_user(peer_id, type_sms)
                elif user_info.number_sms[type_sms] == 1:
                    is_delete = msg_type_sms[type_sms]["is_delete"]
                    msg = msg_type_sms[type_sms]["msg"]
                    #action = "delete"
                    # msg = f"⚠ Обнаружена ссылка на подозрительный источник от данного [id{self.user_id}|пользователя]\n" \
                    #       f"👮‍♂ Дальнейшее повторение таких инцидентов может подлежать наказанию."
                    #action = "delete"

                elif lvl_list["limit"][type_sms] < user_info.number_sms[type_sms]:
                    user_info.xp += lvl_list["limit"]["sms_default_xp"]
                    await self.get_admin(self.club_id,
                                         self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1])
                    cause = msg_type_sms[type_sms]["cause"]
                    result = await WarnGive(self.manager_db, self.settings_info, self.club_id, self.current_time,
                                            self.users_info).run(user_id=self.user_id, peer_id=peer_id, cause=cause,
                                                                 repeated=True)
                    result["is_delete"] = msg_type_sms[type_sms]["is_delete"]
                    return result
                else:
                    is_delete = msg_type_sms[type_sms]["is_delete"]
                    msg = random.choice(["Я предупреждал. Снимаю xp", "Вы не внемли мне. Снимаю опыт."])
                    user_info.xp += lvl_list["limit"]["sms_default_xp"]
                    user_info.tribe_points += lvl_list["limit"]["sms_default_tribe_points"]

            # if type_sms == "spam":
            #     count_sms = await self.get_sms_log(self.user_id, peer_id, lvl_list["limit"]["sms_time_interval"],
            #                                        type_sms)
            #     if count_sms > lvl_list["limit"]["sms_spam_limit"]:
            #         await self.get_admin(self.club_id,
            #                              self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1])
            #         cause = "Превышение допустимого лимита спама в сообщениях"
            #         return await WarnGive(self.manager_db, self.settings_info, self.club_id, self.current_time,
            #                               self.users_info).run(user_id=self.user_id, peer_id=peer_id, cause=cause,
            #                                                    repeated=True)
            #
            # else:
            #     count_sms = await self.get_sms_log(self.user_id, peer_id, lvl_list["limit"]["sms_time_interval"])
            #     #print(count_sms)
            #     if count_sms > lvl_list["limit"]["sms_limit"]:
            #         await self.get_admin(self.club_id,
            #                              self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1])
            #         cause = "Превышение допустимого лимита сообщений"
            #         return await WarnGive(self.manager_db, self.settings_info, self.club_id, self.current_time,
            #                               self.users_info).run(user_id=self.user_id, peer_id=peer_id, cause=cause,
            #                                                    repeated=True)

        if type_sms != "spam":
            is_coins = random.choices([1, 0], weights=[lvl_list['limit']['chance'], 100])[0]
            if is_coins == 1 and user_info.coins == 0:
                if user_info.coins == 0:
                    msg += "\n\n🎉 Поздравляю, вам выпала первая монетка!\n\n"
                else:
                    msg += "\n\n🎁 Поздравляю, вы получили монетку!\n\n"
                user_info.coins += lvl_list['limit']['default_coins']

        msg_ach = ""
        if self.users_info[self.user_id].achievements:
            msg_ach = "\n\n👻 Полученные ачивки:\n" + \
                      "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])
        msg += msg_ach

        return_dict = {"message": msg, "action": action, "update": update,
                       "kick_id": kick_id, "peer_id": peer_id, "is_delete": is_delete, "admin": adm["flag"]}
        return return_dict

    async def get_log_users(self, peer_id, type_sms, message):
        log_dict = {
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type_sms": type_sms,
        }
        return log_dict

    async def get_log_general(self, peer_id, type_sms, message):
        log_dict = {
            "user_id": self.user_id,
            "from_id": self.user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "sms",
            "type_sms": type_sms,
        }
        for i in log_dict:
            message[i] = log_dict[i]
        return message

    async def log_user(self, peer_id, type_sms, message):
        #user_conversation = self.users_info[self.user_id].user_conversation[f"{peer_id}"]
        #user_conversation.log["sms"].append(await self.get_log_users(peer_id, type_sms))

        # if self.users_info[self.user_id].admin:
        #     self.users_info[self.user_id].admin.log["sms"].append(await self.get_log_users(user_id,
        #                                                                                                 peer_id,
        #                                                                                                 attempt, cause))
        #     self.users_info[self.user_id].admin.update = True

        await self.add_log(await self.get_log_general(peer_id, type_sms, message))
        await self.add_sms_log(await self.get_log_general(peer_id, type_sms, message))

        #user_conversation.update = True



if __name__ == "__main__":
    from collections import Counter
    test = Counter(random.choices(['монета', 'нет монеты'], weights=[1, 100])[0]for _ in range(100000))
    print(test)
    is_coins = random.choices([1, 0], weights=[99, 100])
    print(is_coins)

if __name__ == "__main__123":
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
    con = MessageAnalysis(mongo_manager, settings_info,  123456, 300)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(con.run(peer_id=2000001, type_sms="text", message={"id": 2324}))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
