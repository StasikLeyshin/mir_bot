
from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import BanGive
from summer_module.user_conversation import WorkUser, checking_admin


class WarnGive(WorkUser):

    @checking_admin
    async def run(self, user_id: int, peer_id: int, time_plus: int = 0, cause: str = '', **kwargs):
        info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        if not info and not self.is_telegram:
            msg = f"⚠ Данного [id{user_id}|пользователя], возможно, нет в беседе." \
                  "❗ Обновите информацию командой /update."
            return_dict = {"message": msg, "action": "kick", "update": False, "error_message": True}
            return return_dict

        return_dict = await self._add_warn_user(user_id, peer_id, time_plus, cause)
        await self.update_all_user_new()
        return_dict["peer_id"] = peer_id
        return return_dict

    async def get_log_users(self, user_id, peer_id, cause, finish_time, time_plus, warn_count, warn_limit):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "cause": cause,
            "finish_time": finish_time,
            "time_plus": time_plus,
            "warn_count": warn_count,
            "warn_limit": warn_limit
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, cause, finish_time, time_plus, warn_count, warn_limit):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "warn",
            "cause": cause,
            "finish_time": finish_time,
            "time_plus": time_plus,
            "warn_count": warn_count,
            "warn_limit": warn_limit
        }
        return log_dict

    async def _add_warn_user(self, user_id: int, peer_id: int, time_plus: int = 0, cause: str = ''):
        action = False
        update = False
        error_message = False
        # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        # if info:
        await self.get_user_conversation(user_id, f"{peer_id}")

        if self.users_info[user_id].user_conversation[f"{peer_id}"].punishments["ban"].get("status"):
            msg = f"⚠ Данный [id{user_id}|пользователь] забанен, какой ещё варн?."
            return_dict = {"message": msg, "action": action, "update": update, "error_message": True}

            return return_dict

        warn_info = self.users_info[user_id].user_conversation[f"{peer_id}"].punishments["warn"]

        await self.get_user(user_id)
        user_info = self.users_info[user_id].user
        lvl_list = await self.lvl_list(user_info.xp)

        if not warn_info.get("warn_list"):
            warn_info["warn_list"] = []

        if len(warn_info["warn_list"]) >= lvl_list["limit"]["warn_limit"]:
            cause = "Достигнут лимит варнов"
            return await BanGive(self.manager_db, self.settings_info,
                                 self.user_id, self.current_time,
                                 self.users_info, is_telegram=self.is_telegram).run(user_id=user_id, peer_id=peer_id,
                                                      time_plus=time_plus, cause=cause, repeated=True)

        if time_plus == 0:
            time_plus = lvl_list['limit']['warn_default_time']

        ball = lvl_list['limit']['warn_default_xp'] * lvl_list['multiplier']
        user_info.xp += ball
        user_info.tribe_points += lvl_list['limit']['warn_default_tribe_points']

        # await ban_give(user_info, self.users_info[user_id].user_conversation[f"{peer_id}"], lvl_list,
        #                    self.current_time, time_plus, cause)
        finish_time = self.current_time + time_plus
        warn_info["warn_list"].append(
            {
                "start_time": self.current_time,
                "finish_time": finish_time,
                "status": True,
                "cause": cause
            })
        user_info.punishments["warn"]["count"] = 1
        # if user_info.punishments["warn"].get("count"):
        #     user_info.punishments["warn"]["count"] += 1
        # else:
        #     user_info.punishments["warn"]["count"] = 1

        self.users_info[user_id].user_conversation[f"{peer_id}"].update = True
        user_info.update = True

        self.users_info[self.user_id].admin.punishments["count_warn"] += 1
        self.users_info[self.user_id].admin.update = True
        achievements = self.settings_info["warn_admin_awards"]
        await self.give_achievement(self.user_id, self.users_info[self.user_id].admin.punishments["count_warn"],
                                    achievements, self.users_info[self.user_id].admin.achievements, "warn_admin")

        await self.set_user_xp(self.user_id, self.users_info[self.user_id].admin)

        achievements = self.settings_info["warn_awards"]
        await self.give_achievement(user_id, user_info.punishments["warn"]["count"],
                                    achievements, user_info.achievements, "warn", ball)

        if len(warn_info["warn_list"]) == lvl_list["limit"]["warn_limit"]:
            warn_info["warn_list"] = []
            cause = "Достигнут лимит варнов"

            user_info.log["warn"].append(await self.get_log_users(self.user_id, peer_id,
                                                                  action, finish_time,
                                                                  time_plus, len(warn_info['warn_list']),
                                                                  lvl_list['limit']['warn_limit']))

            self.users_info[self.user_id].admin.log["warn"].append(
                await self.get_log_users(user_id, peer_id, cause,
                                         finish_time, time_plus,
                                         len(warn_info['warn_list']), lvl_list['limit']['warn_limit']))

            await self.add_log(await self.get_log_general(self.user_id, peer_id,
                                                          action, finish_time, time_plus,
                                                          len(warn_info['warn_list']), lvl_list['limit']['warn_limit']))

            return await BanGive(self.manager_db, self.settings_info,
                                 self.user_id, self.current_time,
                                 self.users_info, is_telegram=self.is_telegram).run(user_id=user_id, peer_id=peer_id,
                                                      time_plus=time_plus, cause=cause, repeated=True)

        certain_time = await convert_seconds_to_human_time(time_plus)
        end_time_msg = await unix_to_time(finish_time)

        update = True
        action = True

        msg_ach = ""
        msg_admin_ach = ""
        msg_cause = ""
        if self.users_info[user_id].achievements:
            msg_ach = "\n\n👻 Полученные ачивки:\n" + \
                      "\n".join([i['text'] for i in self.users_info[user_id].achievements])

        if self.users_info[self.user_id].achievements:
            msg_admin_ach = "\n\n👻 Админ, заварнивший вас, получает ачивки:\n" + \
                            "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])

        if cause:
            msg_cause = f"\n📝 Причина: {cause}"

        if self.is_telegram:
            msg = "{0}"
        else:
            msg = "[id" + str(user_id) + "|{0}]"
        msg += f", вам выдан варн [{len(warn_info['warn_list'])}/{lvl_list['limit']['warn_limit']}] " \
               f"на {certain_time}{msg_cause}\n" \
               f"⏰ Время окончания: {end_time_msg}{msg_ach}\n\n📊 XP: {round(user_info.xp, 2)}{msg_admin_ach}"

        user_info.log["warn"].append(await self.get_log_users(self.user_id, peer_id,
                                                              action, finish_time,
                                                              time_plus, len(warn_info['warn_list']),
                                                              lvl_list['limit']['warn_limit']))

        self.users_info[self.user_id].admin.log["warn"].append(
            await self.get_log_users(user_id, peer_id, cause,
                                     finish_time, time_plus,
                                     len(warn_info['warn_list']), lvl_list['limit']['warn_limit']))

        await self.add_log(await self.get_log_general(self.user_id, peer_id,
                                                      action, finish_time, time_plus,
                                                      len(warn_info['warn_list']), lvl_list['limit']['warn_limit']))

        return_dict = {"message": msg, "action": action, "update": update}

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

    #ban = BanGive(mongo_manager, settings_info,  55, 100)
    warn = WarnGive(mongo_manager, settings_info,  55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(warn.run(user_id=123456, peer_id=2000001, cause="Спам"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
