

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module import Start
from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin

class ABCBanGive(ABC):
    pass


async def globan_give(user, lvl_list, cause: str = ''):

    ban_info = user.punishments["globan"]

    ban_info["status"] = True
    ban_info["cause"] = cause
    if user.punishments["globan"].get("count"):
        user.punishments["globan"]["count"] += 1
    else:
        user.punishments["globan"]["count"] = 1

    ball = lvl_list['limit']['globan_default_xp'] * lvl_list['multiplier']
    user.xp += ball

    user.update = True

    return True


class GloBan(WorkUser):

    @checking_admin
    async def run(self, user_id: int, peer_id: int, cause: str = '', **kwargs):
        return_dict = await self._add_globan_user(user_id, peer_id, cause)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id, action, cause):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "action": action,
            "cause": cause
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, action, cause):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "globan",
            "action": action,
            "cause": cause,
        }
        return log_dict

    async def _add_globan_user(self, user_id: int, peer_id: int, cause: str = ''):
        action = "kick"
        update = False
        kick_id = []
        error_message = False

        start = Start(self.manager_db, self.settings_info)
        peer_ids = await start.get_all_peer_ids()

        await self.get_user(user_id)
        user_info = self.users_info[user_id].user
        if not user_info.punishments.get("status"):
            await self.get_user(user_id)
            user_info = self.users_info[user_id].user

            lvl_list = await self.lvl_list(user_info.xp)

            await globan_give(user_info, lvl_list, cause)

            # self.users_info[self.user_id].admin.punishments["count_globan"] += 1
            self.users_info[self.user_id].admin.update = True
            # achievements = self.settings_info["ban_admin_awards"]
            # await self.give_achievement(self.user_id, self.users_info[self.user_id].admin.punishments["count_ban"],
            #                             achievements, self.users_info[self.user_id].admin.achievements, "ban_admin")



            ball = lvl_list['limit']['globan_default_xp'] * lvl_list['multiplier']


            #achievements = self.settings_info["ban_awards"]

            action = "kick"
            update = True

            kick_id.append(user_id)

            # await self.give_achievement(user_id, user_info.punishments["ban"]["count"],
            #                             achievements, user_info.achievements, "ban", ball)

            #msg_ach = ""
            #msg_admin_ach = ""
            msg_cause = ""
            #msg_unban = ""
            # if self.users_info[user_id].achievements:
            #     msg_ach = "\n\n👻 Полученные ачивки:\n" + \
            #               "\n".join([i['text'] for i in self.users_info[user_id].achievements])
            #
            # if self.users_info[self.user_id].achievements:
            #     msg_admin_ach = "\n\n👻 Админ, забанивший вас, получает ачивки:\n" + \
            #                     "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])

            if cause:
                msg_cause = f"\n📝 Причина: {cause}"

            # if self.users_info[user_id].user.ban_attempts == -1:
            #     msg_unban = f"\n\n🎁 У вас есть одна бесплатная попытка разбана. " \
            #                 f"Напишите в мои личные сообщения 'разбан' без кавычек."
            # elif self.users_info[user_id].user.ban_attempts > 0:
            #     female_units = ((u'попытка', u'попытки', u'попыток'), 'f')
            #     msg_unban = f"\n\n🎁 У вас есть {await num2text(self.users_info[user_id].user.ban_attempts, female_units)} " \
            #                 f"разбана. " \
            #                 f"Напишите в мои личные сообщения 'разбан' без кавычек."

            #msg = "⛔ [id" + str(user_id) + "|{0}]"
                # msg += f", бан на {certain_time}\n📝 Причина: {cause}\n⏰ Время окончания: {end_time_msg}\n\n" \
                #        f"🎁 У вас есть одна попытка разбана. " \
                #        f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
            #else:
            msg = f"⛔ Данный [id{user_id}|пользователь] добавлен в глобальный бан. {msg_cause}\n"
            # user_ids_kick.append(user_info.user_id)


            if user_info.log.get("globan"):
                user_info.log["globan"].append(await self.get_log_users(self.user_id, peer_id,
                                                                        action, cause))
            else:
                user_info.log["globan"] = [await self.get_log_users(self.user_id, peer_id,
                                                                    action, cause)]
            # user_info.log["ban"].append({
            #     "creator_cmd": False,
            #     "time_issuing": self.current_time,
            #     "action": action,
            #     "user_id": self.user_id,
            #     "peer_id": peer_id,
            #     "cause": cause,
            #     "finish_time": ban_info["finish_time"],
            #     "time_plus": time_plus
            # })
            if self.users_info[self.user_id].admin.log.get("globan"):
                self.users_info[self.user_id].admin.log["globan"].append(
                    await self.get_log_users(user_id, peer_id, action, cause))
            else:
                self.users_info[self.user_id].admin.log["globan"] = \
                    [await self.get_log_users(user_id, peer_id, action, cause)]

            await self.add_log(await self.get_log_general(user_id, peer_id,
                                                          action, cause))



            # self.users_info[self.user_id].admin.log["ban"].append({
            #     "creator_cmd": True,
            #     "time_issuing": self.current_time,
            #     "action": action,
            #     "user_id": user_id,
            #     "peer_id": peer_id,
            #     "cause": cause,
            #     "finish_time": ban_info["finish_time"],
            #     "time_plus": time_plus
            # })

        else:
            action = "kick"
            kick_id.append(user_id)
            msg = f"⚠ Данный [id{user_id}|пользователь] уже находится в глобальном бане."
            error_message = True


        return_dict = {"message": msg, "action": action, "update": update, "kick_id": kick_id,
                       "error_message": error_message, "peer_ids": peer_ids}

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

    ban = GloBan(mongo_manager, settings_info,  55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(user_id=123456, peer_id=2000001, cause="Спам"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)

