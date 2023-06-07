

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin

class ABCBanGive(ABC):
    pass


async def ban_give(user, user_conversation, lvl_list,
                   current_time: int, time_plus: int = 0, cause: str = ''):

    ban_info = user_conversation.punishments["ban"]

    ban_info["start_time"] = current_time
    ban_info["finish_time"] = current_time + time_plus
    ban_info["status"] = True
    ban_info["cause"] = cause
    ban_info["unban"] = False
    if user.punishments["ban"].get("count"):
        user.punishments["ban"]["count"] += 1
    else:
        user.punishments["ban"]["count"] = 1

    ball = lvl_list['limit']['ban_default_xp'] * lvl_list['multiplier']
    user.xp += ball
    user.tribe_points += lvl_list['limit']['ban_default_tribe_points']

    user_conversation.update = True
    user.update = True

    return True




class BanGive(WorkUser):

    @checking_admin
    async def run(self, user_id: int, peer_id: int, time_plus: int = 0, cause: str = '', **kwargs):
        info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        if not info:
            msg = f"⚠ Данного [id{user_id}|пользователя], возможно, нет в беседе." \
                  "❗ Обновите информацию командой /update."
            return_dict = {"message": msg, "action": "kick", "update": False, "kick_id": [user_id], "peer_id": peer_id,
                           "error_message": True}
            return return_dict

        return_dict = await self._add_ban_user(user_id, peer_id, time_plus, cause)
        await self.update_all_user_new()
        return_dict["peer_id"] = peer_id
        return return_dict

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

    async def _add_ban_user(self, user_id: int, peer_id: int, time_plus: int = 0, cause: str = ''):
        action = "kick"
        update = False
        kick_id = []
        error_message = False
        # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        # if info:
        await self.get_user_conversation(user_id, f"{peer_id}")
        ban_info = self.users_info[user_id].user_conversation[f"{peer_id}"].punishments["ban"]
        if not ban_info.get("status"):
            await self.get_user(user_id)
            user_info = self.users_info[user_id].user

            #user_info_dict = user_info.class_dict
            lvl_list = await self.lvl_list(user_info.xp)

            if time_plus == 0:
                time_plus = lvl_list['limit']['ban_default_time']

            await ban_give(user_info, self.users_info[user_id].user_conversation[f"{peer_id}"], lvl_list,
                               self.current_time, time_plus, cause)

            self.users_info[self.user_id].admin.punishments["count_ban"] += 1
            self.users_info[self.user_id].admin.update = True
            achievements = self.settings_info["ban_admin_awards"]
            await self.give_achievement(self.user_id, self.users_info[self.user_id].admin.punishments["count_ban"],
                                        achievements, self.users_info[self.user_id].admin.achievements, "ban_admin")



            ball = lvl_list['limit']['ban_default_xp'] * lvl_list['multiplier']
            # user_info.xp += ball
            # user_info.tribe_points += lvl_list['limit']['ban_default_tribe_points']

            #certain_time = await self.display_time(time_plus)
            certain_time = await convert_seconds_to_human_time(time_plus)

            # value = datetime.fromtimestamp(ban_info["finish_time"])
            # end_time_msg = value.strftime('%d.%m.%Y %H:%M')
            end_time_msg = await unix_to_time(ban_info["finish_time"])

            achievements = self.settings_info["ban_awards"]

            action = "kick"
            update = True

            kick_id.append(user_id)

            await self.give_achievement(user_id, user_info.punishments["ban"]["count"],
                                        achievements, user_info.achievements, "ban", ball)

            msg_ach = ""
            msg_admin_ach = ""
            msg_cause = ""
            msg_unban = ""
            if self.users_info[user_id].achievements:
                msg_ach = "\n\n👻 Полученные ачивки:\n" + \
                          "\n".join([i['text'] for i in self.users_info[user_id].achievements])

            if self.users_info[self.user_id].achievements:
                msg_admin_ach = "\n\n👻 Админ, забанивший вас, получает ачивки:\n" + \
                                "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])

            if cause:
                msg_cause = f"\n📝 Причина: {cause}"

            if self.users_info[user_id].user.ban_attempts == -1:
                msg_unban = f"\n\n🎁 У вас есть одна бесплатная попытка разбана. " \
                            f"Напишите в мои личные сообщения 'разбан' без кавычек."
            elif self.users_info[user_id].user.ban_attempts > 0:
                female_units = ((u'попытка', u'попытки', u'попыток'), 'f')
                msg_unban = f"\n\n🎁 У вас есть {await num2text(self.users_info[user_id].user.ban_attempts, female_units)} " \
                            f"разбана. " \
                            f"Напишите в мои личные сообщения 'разбан' без кавычек."

            msg = "[id" + str(user_id) + "|{0}]"
                # msg += f", бан на {certain_time}\n📝 Причина: {cause}\n⏰ Время окончания: {end_time_msg}\n\n" \
                #        f"🎁 У вас есть одна попытка разбана. " \
                #        f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
            #else:
            msg += f", бан на {certain_time}{msg_cause}\n⏰ Время окончания: {end_time_msg}{msg_unban}" \
                   f"{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
            # user_ids_kick.append(user_info.user_id)

            user_info.log["ban"].append(await self.get_log_users(self.user_id, peer_id,
                                                                 action, cause, ban_info["finish_time"], time_plus))
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
            self.users_info[self.user_id].admin.log["ban"].append(
                await self.get_log_users(user_id, peer_id, action, cause, ban_info["finish_time"], time_plus))

            await self.add_log(await self.get_log_general(user_id, peer_id,
                                                          action, cause, ban_info["finish_time"], time_plus))



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
            msg = f"⚠ Данный [id{user_id}|пользователь] уже находится в бане."
            error_message = True

        return_dict = {"message": msg, "action": action, "update": update, "kick_id": kick_id,
                       "error_message": error_message}

        return return_dict




class Test:
    def __init__(self, kwargs):
        for k, v in kwargs.iteritems():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [obj(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, obj(v) if isinstance(v, dict) else v)

    def __setattr__(self, name, value):
        print("Test")
        self.__dict__[name] = value


class obj:
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [obj(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, obj(v) if isinstance(v, dict) else v)

    def __getattr__(self, item):
        # setattr(self, i, kwargs[i])
        print(item)
        return False

    # def __getattribute__(self, item):
    #     print(item)
    #     return object.__getattribute__(self, item)

    def __setattr__(self, name, value):
        print("Test", name, value)
        self.__dict__[name] = value

    @property
    def class_dict(self):
        return self.__dict__


if __name__ == "__main__2":
    #test = Test({"test": 228})
    #test.name = "red"
    #test.age["red"] = 2

    #d = {'a': 1, 'b': {'c': 2, 'gg': {'c': 3}}, 'd': ["hi", {'foo': "bar"}]}
    d = {'user_id': 1, 'b': {'c': 2, 'gg': {'c': 3}}, 'd': ["hi", {'foo': "bar"}], 'xp': 30}
    ob = obj(d)
    #ob.b.c = 228
    #ob.test = 38
    ob.d.append('hello')
    # if ob.b.gg:
    #     print(ob.b.g)
    print(ob.class_dict)

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

    ban = BanGive(mongo_manager, settings_info,  55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(ban.run(user_id=123456, peer_id=2000001, cause="Спам"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)




# async def add_ban_user(user_id: int, peer_id: int, time_plus: int = 0, cause: str = '',
#                            flag_in_class: bool = False):
#
#         # user_info_detail = []
#         # user_ids = []
#         # user_ids_kick = []
#         action = "kick"
#         update = False
#         # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
#         # if info:
#         await self.user_conversation_update(user_id, peer_id)
#         ban_info = self.users[user_id]["user_conversation"].punishments["ban"]
#         if not ban_info.get("status"):
#             await self.user_update(user_id)
#             user_info = self.users[user_id]["user"]
#
#
#             user_info_dict = user_info.class_dict
#             lvl_list = await self.lvl_list(user_info_dict)
#             await ban_give(user_info, self.users[user_id]["user_conversation"], lvl_list,
#                                self.current_time, time_plus, cause)
#
#             self.admin_info.punishments["count_ban"] += 1
#             achievements = self.settings_info["ban_admin_awards"]
#             await self.give_achievement(self.user_id, self.admin_info.punishments["count_ban"],
#                                         achievements, self.users[self.user_id]["user"].achievements, "ban")
#
#
#             ball = lvl_list['limit']['ban_default_xp'] * lvl_list['multiplier']
#             user_info.xp += ball
#             user_info.tribe_points += lvl_list['limit']['ban_default_tribe_points']
#
#             certain_time = await self.display_time(time_plus)
#
#             value = datetime.fromtimestamp(ban_info["finish_time"])
#             end_time_msg = value.strftime('%d.%m.%Y %H:%M')
#
#             achievements = self.settings_info["ban_awards"]
#
#             action = "kick"
#             update = True
#
#             await self.give_achievement(user_id, user_info.punishments["ban"]["count"],
#                                         achievements, user_info.achievements, "ban", ball)
#
#             msg_ach = ""
#             msg_admin_ach = ""
#             if self.achievements.get(user_id):
#                 msg_ach = "\n\n👻 Полученные ачивки:\n" + \
#                           "\n".join([i['text'] for i in self.achievements.get(user_id)])
#
#             if self.achievements.get(self.user_id):
#                 msg_admin_ach = "\n\n👻 Админ, забанивший вас, получает ачивки:\n" + \
#                                 "\n".join([i['text'] for i in self.achievements.get(self.user_id)])
#
#             msg = "{0} "
#             if cause:
#                 msg += f", бан на {certain_time}\n📝 Причина: {cause}\n⏰ Время окончания: {end_time_msg}\n\n" \
#                        f"🎁 У вас есть одна попытка разбана. " \
#                        f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
#             else:
#                 msg += f", бан на {certain_time}\n⏰ Время окончания: {end_time_msg}\n\n" \
#                        f"🎁 У вас есть одна попытка разбана." \
#                        f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
#             #user_ids_kick.append(user_info.user_id)
#
#             user_info.log["ban"].append({
#                 "creator_cmd": False,
#                 "current_time": self.current_time,
#                 "action": action,
#                 "user_id": self.user_id,
#                 "peer_id": peer_id,
#                 "cause": cause,
#                 "finish_time": ban_info["finish_time"],
#                 "time_plus": time_plus
#             })
#
#             self.admin_info.log["ban"].append({
#                 "creator_cmd": True,
#                 "current_time": self.current_time,
#                 "action": action,
#                 "user_id": user_id,
#                 "peer_id": peer_id,
#                 "cause": cause,
#                 "finish_time": ban_info["finish_time"],
#                 "time_plus": time_plus
#             })
#
#         else:
#             msg = f"⚠ Данный [id{user_id}|пользователь] уже находится в бане."
#         # else:
#         #     msg = f"⚠ Данного [id{user_id}|пользователя], возможно, нет в беседе, но я попробую его исключить."
#
#         return_dict = {"message": msg, "action": action, "update": update}
#
#         return return_dict
