
from datetime import datetime
import time
import functools
import random

from mongodb import MongoManager


class Model:

    def __init__(self, **kwargs):
        self.update = False

    def self_generator(self, kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

    @property
    def class_dict(self):
        return_dict = self.__dict__.copy()
        del return_dict['update']
        return return_dict


class User(Model):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.user_id: int = 0
        self.telegram_user_id: int = 0
        self.punishments: dict = {"ban": {}, "warn": {}, "globan": {}}
        self.achievements: list = []
        self.cmd: dict = {"roulette": {}, "chance": {}, "profile": {}, "report": {},
                          "reputation_plus": {}, "reputation_minus": {}, "my_tribe": {},
                          "tribe_rating": {}}
        self.number_sms: dict = {"text": 0, "spam": 0, "swear": 0, "sms_voice": 0, "sms_video_circle": 0, "sms_link": 0,
                                 "photo": 0, "sticker": 0, "swear_forward_message": 0
                                 # "activity":
                                 #     {
                                 #         "day_list": [],
                                 #         "count": 0
                                 #     }
                                 }
        # self.reports: dict = {}
        self.xp: float = 0
        self.coins: int = 0
        self.tribe_points: int = 0  # трайб поинты, начисляются за заслуги перед кланом(беседы) /репорт, помощь
        self.influence: int = 4
        self.ban_attempts: int = -1
        self.tribe: str = "NoName"
        self.log: dict = {"ban": [], "warn": [], "roulette": [], "chance": [], "profile": [], "report": [],
                          "reputation_plus": [], "reputation_minus": [], "my_tribe": [],
                          "tribe_rating": []
                          }
        self.start_time = 0

        #self.kwargs = kwargs
        # if flag:
        self.self_generator(kwargs)
        # else:
        #     self.self_generator() [1LVL ******---- 2LVL]


class User_conversation(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.admin: bool = False
        self.kicked: bool = False
        self.output: bool = False
        self.punishments: dict = {"ban": {}, "warn": {}}
        self.log: dict = {"chat_returned_user": [], "chat_invite_user": [],
                          "chat_invite_user_by_link": [], "chat_kick_user": [], "chat_exit_user": []}
        self.start_time = 0
        self.role: str = "child"
        self.self_generator(kwargs)


class Tribe(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = ""
        self.cut: str = ""
        self.tribe_points: int = 0
        self.war: dict = {}

        self.log: list = []
        self.self_generator(kwargs)


class Admin(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.telegram_user_id: int = 0
        self.achievements: list = []
        self.punishments: dict = {"count_warn": 0, "count_ban": 0}
        self.role: str = "beginner"
        self.status = True
        self.xp: int = 0
        self.log: dict = {"ban": [], "warn": [], "chat_invite_user": [],
                          "chat_kick_user": []}
        self.self_generator(kwargs)


class Log(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.from_id: int = 0
        self.peer_id: int = 0
        self.current_time: int = 0
        self.self_generator(kwargs)


class ConversationZl(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.peer_id_zl = 0
        self.peer_id = 0
        self.self_generator(kwargs)


class ConversationSt(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.peer_id_zl = 0
        self.peer_id = 0
        self.self_generator(kwargs)


class PeerIds(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.peer_id = 0
        self.self_generator(kwargs)


class Zawarn(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.from_id: int = 0
        self.peer_id: int = 0
        self.conversation_message_id_forward: int = 0
        self.conversation_message_id_original: int = 0
        self.current_time: int = 0
        self.type_sms: str = "swear"
        self.status: bool = False
        self.self_generator(kwargs)


class Unban(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.questions_answers: list = []
        self.count: int = 0
        self.random_value = ""
        self.active = False
        self.peer_ids: list = []
        self.self_generator(kwargs)


class UserLs(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.location_tree: str = "help"
        self.ignore_tree = False
        self.stop_location_tree = False
        self.log: dict = {}
        self.self_generator(kwargs)


class TaskUserBot(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 0
        self.peer_ids: list = []
        self.permission = True
        self.self_generator(kwargs)


class SettingTime(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = 1
        self.start_time: int = 0
        self.finish_time: int = 0
        self.log: list = []
        self.self_generator(kwargs)


class UserObject:
    def __init__(self, kwargs):
        for k, v in kwargs.iteritems():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [obj(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, obj(v) if isinstance(v, dict) else v)





class UserInfo:
    def __init__(self):
        self._user = None
        self.user_conversation = {}
        self._admin = None
        self.achievements = []

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user_info: User):
        self._user = user_info

    # @property
    # def user_conversation(self):
    #     return self._user_conversation
    #
    # @user_conversation.setter
    # def user_conversation(self, user_info: User_conversation):
    #     self._user_conversation = user_info

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, user_info: Admin):
        self._admin = user_info


def checking_admin(fun):
    async def wrapper(self, *args, **kwargs):
        if not kwargs.get("repeated"):
            is_admin = await self.is_admin(self.user_id, f'{kwargs["peer_id"]}')

            if is_admin["flag"]:
                await self.get_admin(self.user_id, is_admin["role"])

                if kwargs.get("from_id_check"):
                    is_admin = await self.is_admin(kwargs["user_id"], f'{kwargs["peer_id"]}')
                    if is_admin["flag"]:
                        msg = f"⚠ Данный [id{kwargs['user_id']}|пользователь] админ!"
                        return_dict = {"message": msg, "action": False, "error_message": True}
                        return return_dict
            else:
                return False
        answer = await fun(self, *args, **kwargs)
        return answer

    return wrapper


class WorkUser:
    def __init__(self, manager_db, settings_info=None, user_id: int = 0, current_time: int = 0, users_info=None,
                 is_telegram=False):
        if users_info is None:
            users_info = {}
        self.manager_db = manager_db
        self.settings_info = settings_info

        self.user_id: int = user_id
        self.users_info = users_info

        self.current_time = current_time

        self.is_telegram = is_telegram

        self.users_documents: str = "users"
        self.users_admin_documents: str = "users_admin"
        self.logs_documents = "logs"
        self.conversations_zl = "conversations_zl"
        self.conversations_st = "conversations_st"
        self.peer_ids = "peer_ids"
        self.zawarn_documents = "zawarn"
        self.unban_documents = "unban"
        self.task_user_bot_documents = "task_user_bot"
        self.work_ls_documents = "work_ls"
        self.setting_time_documents = "setting_time"
        self.tribe_documents = "tribes"

        self.collection_django = "test4"
        self.django_unban_documents = "article_answers_unban_new1"

        self.club_id = -5411326
        self.user_id_bot = 799863315

        self.tribes = {
            "NoName": "Без клана",
            "musk_deer": "🦌 Кабарги",
            "sea_lion": "🐋 Сивучи",
            "manul": "🐈 Манулы",
            "kulan": "🐴 Куланы"
        }

    async def display_time(self, seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

    async def create_user_info(self, user_id):
        if not self.users_info.get(user_id):
            self.users_info[user_id] = UserInfo()

    async def get_admin(self, user_id: int, role: str):
        await self.create_user_info(user_id)
        if not self.users_info[user_id].admin:
            self.users_info[user_id].admin = Admin(user_id=user_id, role=role)
            self.users_info[user_id].admin.self_generator(
                await self.manager_db.user_insert_one(self.users_info[user_id].admin.class_dict,
                                                      self.users_admin_documents))

    async def get_user(self, user_id: int):
        await self.create_user_info(user_id)

        if not self.users_info[user_id].user:
            if not self.is_telegram:
                self.users_info[user_id].user = User(user_id=user_id, start_time=self.current_time)
                self.users_info[user_id].user.self_generator(
                    await self.manager_db.user_insert_one(self.users_info[user_id].user.class_dict,
                                                          self.users_documents))
            else:
                self.users_info[user_id].user = User(telegram_user_id=user_id, start_time=self.current_time)
                self.users_info[user_id].user.self_generator(
                    await self.manager_db.user_insert_one(self.users_info[user_id].user.class_dict,
                                                          self.users_documents, self.is_telegram))


    async def get_user_conversation(self, user_id: int, users_documents_bs: str):
        await self.create_user_info(user_id)

        if not self.users_info[user_id].user_conversation.get(users_documents_bs):
            self.users_info[user_id].user_conversation[users_documents_bs] = User_conversation(
                user_id=user_id, start_time=self.current_time)
            self.users_info[user_id].user_conversation[users_documents_bs].self_generator(
                await self.manager_db.user_insert_one(
                    self.users_info[user_id].user_conversation[users_documents_bs].class_dict,
                    users_documents_bs))

    async def create_user(self, user_id: int, users_documents_bs: str):
        await self.get_user(user_id)
        await self.get_user_conversation(user_id, str(users_documents_bs))

    async def update_all_user(self, user_id: int, users_documents_bs: str, admin_id: int):
        await self.manager_db.user_update_one(self.users_info[user_id].user.class_dict, self.users_documents)
        await self.manager_db.user_update_one(self.users_info[user_id].user_conversation.class_dict, users_documents_bs)
        await self.manager_db.user_update_one(self.users_info[admin_id].admin.class_dict, self.users_admin_documents)

    async def update_all_user_new(self):
        for i in self.users_info:
            if self.users_info[i].user and self.users_info[i].user.update:
                self.users_info[i].user.update = False
                await self.manager_db.user_update_one(self.users_info[i].user.class_dict, self.users_documents,
                                                      self.is_telegram)
            if self.users_info[i].user_conversation:
                for peer_id in self.users_info[i].user_conversation:
                    if self.users_info[i].user_conversation[peer_id].update:
                        self.users_info[i].user_conversation[peer_id].update = False
                        await self.manager_db.user_update_one(self.users_info[i].user_conversation[peer_id].class_dict,
                                                              peer_id)
            #print(self.users_info[i])
            if self.users_info[i].admin and self.users_info[i].admin.update:
                self.users_info[i].admin.update = False
                await self.manager_db.user_update_one(self.users_info[i].admin.class_dict, self.users_admin_documents)

    async def get_conversation_zl(self, peer_id_zl: int, is_user_bot: bool = False):
        con_zl = ConversationZl(peer_id_zl=peer_id_zl)
        if is_user_bot:
            documents = self.conversations_st
        else:
            documents = self.conversations_zl
        con_zl.self_generator(await self.manager_db.conversation_zl_insert_one(con_zl.class_dict, documents))
        return con_zl

    async def update_conversation_zl(self, conversation_zl, is_user_bot: bool = False):
        if is_user_bot:
            documents = self.conversations_st
        else:
            documents = self.conversations_zl
        await self.manager_db.conversation_zl_update_one(conversation_zl.class_dict, documents)


    async def get_peer_ids(self, peer_id: int):
        peer_ids = PeerIds(peer_id=peer_id)
        peer_ids.self_generator(await self.manager_db.peer_ids_insert_one(peer_ids.class_dict, self.peer_ids))
        return peer_ids

    async def update_peer_ids(self, peer_ids):
        await self.manager_db.conversation_zl_update_one(peer_ids.class_dict, self.peer_ids)

    async def get_tribe(self):
        tribes = {}
        for i in self.settings_info['tribe']:
            i = i['settings']
            tribe = Tribe(cut=i['cut'], name=i['name'])
            tribe.self_generator(await self.manager_db.tribe_insert_one(tribe.class_dict, self.tribe_documents))
            count = await self.manager_db.tribe_users_count(i['cut'], self.users_documents)
            tribes[i['cut']] = count

        minval = min(tribes.values())
        res = [k for k, v in tribes.items() if v == minval]
        return random.choice(res)

    async def set_user_xp(self, user_id, user):
        if self.users_info[user_id].achievements:
            for i in self.users_info[user_id].achievements:
                user.xp += i["xp"]
                if i.get("tribe_points"):
                    user.tribe_points += i["tribe_points"]

    async def set_count_cmd(self, user_info, type_cmd):
        if user_info.cmd.get(type_cmd):
            if user_info.cmd[type_cmd].get("count"):
                user_info.cmd[type_cmd]["count"] += 1
            else:
                user_info.cmd[type_cmd]["count"] = 1
        else:
            user_info.cmd[type_cmd] = {"count": 1}
    async def is_empty_user(self, user_id: int, peer_id: int):
        info = await self.manager_db.user_get_one(user_id, self.users_documents)
        if not info:
            info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
            if not info:
                msg = "👽 Такого пользователя не существует"
                return_dict = {"message": msg}
                return return_dict
        return False

    async def add_log_user(self, user_info, type_name: str, log_dict: dict):
        if user_info.log.get(str(type_name)):
            user_info.log[str(type_name)].append(log_dict)
        else:
            user_info.log[str(type_name)] = [log_dict]

    async def lvl_cmd_add_list(self, user, cmd):
        command_level = self.settings_info["command_level"]
        xp = user["xp"]
        cmd_dict = {}
        sum_xp = 0
        for i in command_level:
            sum_xp += i["xp"]
            if xp >= sum_xp and xp != 0:
                if i.get("cmd_list"):
                    for j in i["cmd_list"]:
                        if cmd == j["cmd"]:
                            cmd_dict[cmd] = j
                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
            elif xp <= 0:
                if i.get("cmd_list"):
                    for j in i["cmd_list"]:
                        if cmd == j["cmd"]:
                            cmd_dict[cmd] = j
                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
                break
            else:
                break
            # cmd_dict["limit"] = i["limit"]
            # cmd_dict["multiplier"] = i["multiplier"]
        return cmd_dict

    async def lvl_cmd_get_list(self, xp):
        command_level = self.settings_info["command_level"]
        cmd_dict = {"cmd_list": []}
        sum_xp = 0
        for i in command_level:
            sum_xp += i["xp"]
            if xp >= sum_xp and xp != 0:
                if i.get("cmd_list"):
                    for cmd in i["cmd_list"]:
                        flag = False
                        k = 0
                        for j in cmd_dict["cmd_list"]:
                            if cmd["cmd"] == j["cmd"]:
                                cmd_dict["cmd_list"][k] = cmd
                                flag = True
                            k += 1
                        if not flag:
                            cmd_dict["cmd_list"].append(cmd)

                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
            elif xp <= 0:
                if i.get("cmd_list"):
                    if i.get("cmd_list"):
                        for cmd in i["cmd_list"]:
                            flag = False
                            k = 0
                            for j in cmd_dict["cmd_list"]:
                                if cmd["cmd"] == j["cmd"]:
                                    cmd_dict["cmd_list"][k] = cmd
                                    flag = True
                                k += 1
                            if not flag:
                                cmd_dict["cmd_list"].append(cmd)
                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
                break
            else:
                break
            # cmd_dict["limit"] = i["limit"]
            # cmd_dict["multiplier"] = i["multiplier"]
        return cmd_dict


    async def lvl_list(self, xp, role=None):
        command_level = self.settings_info["command_level"]
        cmd_dict = {}
        sum_xp = 0
        end_xp = 0
        for i in command_level:
            cmd_dict["lvl"] = i["lvl"]
            sum_xp += i["xp"]
            end_xp = i["xp"]
            if xp >= sum_xp and xp != 0:
                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
            elif xp <= 0:
                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
                break
            else:
                break

        if end_xp > 0:
            cmd_dict["lvl_percent_short"] = int((xp - (sum_xp - end_xp)) / end_xp * 20)
            cmd_dict["lvl_percent"] = int((xp - (sum_xp - end_xp)) / end_xp * 100)
        else:
            cmd_dict["lvl_percent_short"] = 0
            cmd_dict["lvl_percent"] = 0
        if cmd_dict["lvl"] != 0:
            cmd_dict["lvl"] -= 1

        if role:
            role_user_limit = self.settings_info["role_user_limit"].get(role)
            if role_user_limit:
                for i in role_user_limit:
                    cmd_dict["limit"][i] = role_user_limit[i]

        return cmd_dict

    async def give_achievement(self, user_id, count, achievements, user_achievements, type_achievement, xp=None,
                               multiplier=1, admin_id=None):
        if not admin_id:
            admin_id = self.user_id
        for i in achievements:
            if i["count"] == count:
                flag = False
                for j in user_achievements:
                    if i['text'] in j["text"]:
                        flag = True
                        break
                if not flag:
                    if xp:
                        ach = {'text': f'{self.settings_info[f"{type_achievement}_awards_smiley"]} {i["text"]}',
                               "admin": admin_id,
                               "count": count,
                               "xp": xp,
                               "type": type_achievement,
                               "current_time": self.current_time}
                    else:
                        if self.settings_info.get(f"{type_achievement}_awards_smiley"):
                            smile = str(self.settings_info.get(f"{type_achievement}_awards_smiley")) + " "
                        else:
                            smile = ""
                        ach = {'text': f'{smile}{i["text"]}',
                               "admin": admin_id,
                               "count": count,
                               "xp": i["xp"] * multiplier,
                               "tribe_points": i.get("tribe_points"),
                               "type": type_achievement,
                               "current_time": self.current_time}
                    user_achievements.append(ach)
                    #if self.users_info[user_id].achievements.get(user_id):
                    self.users_info[user_id].achievements.append(ach)
                    #else:
                        #self.achievements[user_id] = [ach]

    async def is_admin(self, user_id: int, users_documents_bs: str = ''):
        flag = False
        return_dict = {"flag": flag}
        for i in self.settings_info["user_id_admins"]:
            if user_id == i:
                flag = True
                return_dict = {"flag": flag,
                               "role": self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1]}
                break
        if not flag and users_documents_bs:
            info = await self.manager_db.user_get_one(user_id, users_documents_bs)
            if info:
                if info["admin"]:
                    flag = True
                    return_dict = {"flag": flag,
                                   "role": self.settings_info["role_admin"][0]}
        info = await self.manager_db.user_get_one(user_id, self.users_admin_documents)
        if info:
            if info["status"]:
                flag = True
                return_dict = {"flag": flag,
                               "role": info["role"]}
            else:
                flag = False
                return_dict = {"flag": flag}
        return return_dict

    async def add_log(self, kwargs):

        log = Log(user_id=self.user_id, current_time=self.current_time)
        log.self_generator(kwargs)

        await self.manager_db.log_insert_one(log.class_dict, self.logs_documents)

    async def add_sms_log(self, kwargs):

        log = Log(user_id=self.user_id, current_time=self.current_time)
        log.self_generator(kwargs)

        await self.manager_db.log_insert_one(log.class_dict, f"{kwargs['peer_id']}_sms")

    async def get_sms_log(self, user_id: int, peer_id: int, time_interval: int = 60, type_sms: str = None):
        return await self.manager_db.log_sms_count(user_id,
                                                   self.current_time, time_interval,
                                                   f"{peer_id}_sms", type_sms)





    # def checking_admin(repeated=False, from_id_check=False):
    #     def decorator(func):
    #         @functools.wraps(func)
    #         async def wrapper(self, *args, **kwargs):
    #             if not repeated:
    #                 is_admin = await self.is_admin(self.user_id, f'{kwargs["peer_id"]}')
    #
    #                 if is_admin["flag"]:
    #                     await self.create_admin(self.user_id, is_admin["role"])
    #
    #                     if from_id_check:
    #                         is_admin = await self.is_admin(kwargs["user_id"], f'{kwargs["peer_id"]}')
    #                         if is_admin["flag"]:
    #                             msg = f"⚠ Данный [id{kwargs['user_id']}|пользователь] админ!"
    #                             return_dict = {"message": msg, "action": False}
    #                             return return_dict
    #                 else:
    #                     return False
    #
    #                 # info = await self.manager_db.user_get_one(kwargs["user_id"], f"{kwargs['peer_id']}")
    #                 # if not info:
    #                 #     msg = f"⚠ Данного [id{kwargs['user_id']}|пользователя], возможно, нет в беседе." \
    #                 #           "❗ Обновите информацию командой /update."
    #                 #     return_dict = {"message": msg, "action": "kick"}
    #                 #     return return_dict
    #
    #             answer = await func(self, *args, **kwargs)
    #             return answer
    #
    #         return wrapper
    #
    #     return decorator

    @checking_admin
    async def test(self, user_id, peer_id, repeated=False, from_id_check=False):
        print("Doshlo")

if __name__ == "__main__":
    from motor import MotorClient
    import asyncio
    import yaml
    with open('description_commands.yaml', encoding="utf-8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
    # pprint(read_data)
    loop = asyncio.get_event_loop()
    uri = 'mongodb://localhost:27017'
    client = MotorClient(uri)

    mongo_manager = MongoManager(client)
    #wok = WorkUser(mongo_manager, 55, 100) self.settings_info = await self.manager_db.settings_get_one(self.settings_documents)

    settings_info = loop.run_until_complete(mongo_manager.settings_insert_one(read_data, "settings"))
    # loop.run_until_complete(mongo_manager.settings_update_one(read_data, "settings"))
    # test2 = loop.run_until_complete(wok.lvl_cmd_add_list({"xp": 12345}, "profile"))
    # test2 = loop.run_until_complete(wok.lvl_list({"xp": 700}))
    # test2 = loop.run_until_complete(wok.achievements_check(user_info_list=[123456]))
    # test2 = loop.run_until_complete(wok.add_ban_user(user_id=123456, peer_id=2000001, cause="Спам"))
    #test2 = loop.run_until_complete(wok.add_warn_user(user_id=123456, peer_id=2000001, cause="Спам"))

    #  wok = WorkUser(mongo_manager, settings_info,  55, 100)

    #  ban = BanGive(mongo_manager, settings_info,  55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    #  test2 = loop.run_until_complete(ban.add_ban_user(user_id=123456, peer_id=2000001, cause="Спам"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    # print(test2)

class Work_user:

    def __init__(self, manager_db, user_id: int, current_time: int):

        #self.client = client
        self.user_id: int = user_id
        self.current_time: int = current_time

        self.users_documents: str = "users"
        self.users_admin_documents: str = "users_admin"
        #self.users_documents_bs: str = users_documents_bs
        self.settings_documents: str = "settings"

        self.achievements: dict = {}

        self.settings_info = None
        self.admin_info = None

        self.manager_db = manager_db  # MongoManager(self.client)
        # self.user = User(user_id=self.user_id)
        # self.user_conversation = None

        self.users = {
            self.user_id: {
                "user": User(user_id=self.user_id, start_time=self.current_time),
                "user_conversation": User_conversation(user_id=self.user_id)
            }
        }

    async def display_time(self, seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

    async def user_update(self, user_id):
        user = User(user_id=user_id, start_time=self.current_time)
        user.self_generator(await self.manager_db.user_insert_one(user.class_dict, self.users_documents))
        if self.users.get(user_id):
            self.users[user_id]["user"] = user
        else:
            self.users[user_id] = {}
            self.users[user_id]["user"] = user
        return user

    async def user_conversation_update(self, user_id, users_documents_bs):
        user_conversation = User_conversation(user_id=user_id, start_time=self.current_time)
        user_conversation.self_generator(await self.manager_db.user_insert_one(user_conversation.class_dict,
                                                                               users_documents_bs))
        if self.users.get(user_id):
            self.users[user_id]["user_conversation"] = user_conversation
        else:
            self.users[user_id] = {}
            self.users[user_id]["user_conversation"] = user_conversation
        return user_conversation


    async def create_user(self, user_id, users_documents_bs):
        self.users[user_id]["user"] = await self.user_update(user_id)
        self.users[user_id]["user_conversation"] = await self.user_conversation_update(user_id, users_documents_bs)

    async def create_admin(self, user_id, role):
        self.admin_info = Admin(user_id=user_id, role=role)
        self.admin_info.self_generator(
            await self.manager_db.user_insert_one(self.admin_info.class_dict, self.users_admin_documents))

    async def user_update_all(self, user_id, users_documents_bs):
        await self.manager_db.user_update_one(self.users[user_id]["user"].class_dict, self.users_documents)
        await self.manager_db.user_update_one(self.users[user_id]["user_conversation"].class_dict, users_documents_bs)
        await self.manager_db.user_update_one(self.admin_info.class_dict, self.users_admin_documents)

    async def lvl_cmd_add_list(self, user, cmd):
        #settings = await self.manager_db.settings_get_one(self.settings_documents)
        command_level = self.settings_info["command_level"]
        xp = user["xp"]
        cmd_dict = {}
        sum_xp = 0
        for i in command_level:
            sum_xp += i["xp"]
            if xp >= sum_xp:
                if i.get("cmd_list"):
                    for j in i["cmd_list"]:
                        if cmd == j["cmd"]:
                            cmd_dict[cmd] = j
            else:
                break
            cmd_dict["limit"] = i["limit"]
        return cmd_dict

    async def lvl_list(self, user):
        command_level = self.settings_info["command_level"]
        xp = user["xp"]
        cmd_dict = {}
        sum_xp = 0
        end_xp = 0
        for i in command_level:
            cmd_dict["lvl"] = i["lvl"]
            sum_xp += i["xp"]
            end_xp = i["xp"]
            if xp >= sum_xp or sum_xp == 0:
                cmd_dict["limit"] = i["limit"]
                cmd_dict["multiplier"] = i["multiplier"]
            else:
                break

        if end_xp <= 0:
            cmd_dict["lvl_percent_short"] = int((xp - (sum_xp - end_xp)) / end_xp * 10)
            cmd_dict["lvl_percent"] = int((xp - (sum_xp - end_xp)) / end_xp * 100)
        else:
            cmd_dict["lvl_percent_short"] = 0
            cmd_dict["lvl_percent"] = 0
        if cmd_dict["lvl"] != 0:
            cmd_dict["lvl"] -= 1

        return cmd_dict

    async def is_admin(self, user_id: int, users_documents_bs: str):
        flag = False
        return_dict = {"flag": flag}
        for i in self.settings_info["user_id_admins"]:
            if user_id == i:
                flag = True
                return_dict = {"flag": flag,
                               "role": self.settings_info["role_admin"][len(self.settings_info["role_admin"]) - 1]}
                break
        if not flag:
            info = await self.manager_db.user_get_one(user_id, users_documents_bs)
            if info:
                if info["admin"]:
                    flag = True
                    return_dict = {"flag": flag,
                                   "role": self.settings_info["role_admin"][0]}
        if not flag:
            info = await self.manager_db.user_get_one(user_id, self.users_admin_documents)
            if info:
                if info["status"]:
                    flag = True
                    return_dict = {"flag": flag,
                                   "role": info["role"]}
        return return_dict

    async def give_achievement(self, user_id, count, achievements, user_achievements, type_achievement, xp=None):
        for i in achievements:
            if i["count"] == count:
                flag = False
                for j in user_achievements:
                    if j['text'] == i["text"]:
                        flag = True
                        break
                if not flag:
                    if xp:
                        ach = {'text': f'{self.settings_info[f"{type_achievement}_awards_smiley"]} {i["text"]}',
                               "admin": self.user_id,
                               "count": count,
                               "xp": xp,
                               "type": type_achievement,
                               "time_issuing": self.current_time}
                    else:
                        ach = {'text': f'{self.settings_info[f"{type_achievement}_awards_smiley"]} {i["text"]}',
                               "admin": self.user_id,
                               "count": count,
                               "xp": i["xp"],
                               "type": type_achievement,
                               "time_issuing": self.current_time}
                    user_achievements.append(ach)
                    if self.achievements.get(user_id):
                        self.achievements[user_id].append(ach)
                    else:
                        self.achievements[user_id] = [ach]

    def control(fun):
        async def wrapper(self, *args, **kwargs):
            # self.users[self.user_id]["user"].self_generator(
            #     await self.manager_db.user_insert_one(self.users[self.user_id]["user"].class_dict,
            #                                           self.users_documents))
            await self.user_update(self.user_id)

            self.settings_info = await self.manager_db.settings_get_one(self.settings_documents)

            if fun.__name__ == "user_profile_info" or fun.__name__ == "achievements_check":
                user_info_list_new = []

                user_info_general = await self.lvl_cmd_add_list(self.users[self.user_id]["user"].class_dict, "profile")
                if user_info_general["profile"]["is_another_user"]:
                    for user_id in kwargs["user_info_list"]:
                        user_info_list_new.append(await self.user_update(user_id))
                else:
                    is_admin = await self.is_admin(self.users[self.user_id]["user"], kwargs["peer_id"])
                    if is_admin:
                        for user_id in kwargs["user_info_list"]:
                            user_info_list_new.append(await self.user_update(user_id))
                    else:
                        user_info_list_new = [self.users[self.user_id]["user"]]
                kwargs["user_info_list"] = user_info_list_new
                answer = await fun(self, *args, **kwargs)

            # if fun.__name__ == "add_ban_users":
            #     user_info_list_new = []
            #
            #     is_admin = await self.is_admin(self.user_id, self.users_documents_bs)
            #
            #     if is_admin:
            #         for user_id in kwargs["user_info_list"]:
            #             user_info_list_new.append(await self.user_update(user_id))
            #     else:
            #         return False
            #     kwargs["user_info_list"] = user_info_list_new
            #     answer = await fun(self, *args, **kwargs)

            if fun.__name__ == "add_ban_user" or fun.__name__ == "add_warn_user":

                if not kwargs.get("flag_in_class"):
                    is_admin = await self.is_admin(self.user_id, f'{kwargs["peer_id"]}')

                    if is_admin["flag"]:
                        #kwargs["user_info"] = await self.user_update(kwargs["user_info"])
                        #await self.user_update(kwargs["user_id"])
                        #await self.create_user(kwargs["user_id"])
                        await self.create_admin(self.user_id, is_admin["role"])
                        # self.admin_info = Admin(user_id=self.user.user_id)
                        # self.admin_info.self_generator(
                        #     await self.manager_db.user_insert_one(self.admin_info.class_dict, self.users_admin_documents))

                        is_admin = await self.is_admin(kwargs["user_id"], f'{kwargs["peer_id"]}')
                        if is_admin["flag"]:

                            msg = f"⚠ Данный [id{kwargs['user_id']}|пользователь] админ!"
                            return_dict = {"message": msg, "action": False}
                            return return_dict

                        info = await self.manager_db.user_get_one(kwargs["user_id"], f"{kwargs['peer_id']}")
                        if not info:
                            msg = f"⚠ Данного [id{kwargs['user_id']}|пользователя], возможно, нет в беседе." \
                                  "❗ Обновите информацию командой /update."
                            return_dict = {"message": msg, "action": "kick"}
                            return return_dict

                    else:
                        # msg = f"⚠ Вы не админ!\n" \
                        #       f"🚫 За повторную попытку, буду снижать xp."
                        # return_dict = {"message": msg, "action": False}
                        return False
                #kwargs["user_info"] = user_info_list_new

                answer = await fun(self, *args, **kwargs)

                if answer["update"]:
                    await self.user_update_all(kwargs["user_id"], kwargs["peer_id"])

                # if answer["action"]:
                #     kwargs["user_info"].log.append({
                #         "cmd": answer["log"]["cmd"],
                #         "creator_cmd": False,
                #         "current_time": self.current_time,
                #         "action": answer["action"],
                #         "user_id": self.user_id,
                #         "cause": kwargs["cause"],
                #         "finish_time": answer["log"]["finish_time"],
                #         "time_plus": answer["log"]["time_plus"]
                #     })
                #await self.manager_db.user_update_one(kwargs["user_info"].class_dict, self.users_documents)

            if fun.__name__ == "give_plus_rep":
                is_admin = await self.is_admin(self.user_id, f'{kwargs["peer_id"]}')

                if is_admin["flag"]:
                    await self.create_admin(self.user_id, is_admin["role"])

                    # kwargs["user_info"] = await self.user_update(kwargs["user_info"])
                    # self.admin_info = Admin(user_id=self.users[self.user_id]["user"].user_id)
                    # self.admin_info.self_generator(
                    #     await self.manager_db.user_insert_one(self.admin_info.class_dict, self.users_admin_documents))


                answer = await fun(self, *args, **kwargs)

            return answer

        return wrapper

    @control
    async def user_profile_info(self, user_info_list: list):
        # self.user.self_generator(await self.manager_db.user_insert_one(self.user.class_dict, self.users_documents))
        #
        # user_info_list = await self.user_info_list_add(user_id_list)
        #
        user_info_detail = []
        user_ids = []

        for user_info in user_info_list:
            warn = ""
            ban = ""
            user_info_dict = user_info.class_dict
            lvl_list = await self.lvl_list(user_info_dict)

            if user_info.punishments["warn"]:
                    if len(user_info_dict["punishments"]["warn"]["warn_list"]) != 0:
                        warn += f"☢ Варны: [{len(user_info_dict['punishments']['warn']['warn_list'])}/{lvl_list['limit']['warn_limit']}]\n"
                    warn += f"🤡 Количество варнов: {user_info_dict['punishments']['warn']['count']}\n\n"

            if user_info.punishments["ban"]:
                ban += f"🤡 Количество банов: {user_info_dict['punishments']['ban']['count']}\n\n"

            achievements = f"👻 Количество ачивок: {len(user_info_dict['achievements'])}"

            xp = f"📊 XP: {user_info_dict['xp']}"
            coins = f"💰 Деньги: {user_info_dict['coins']}"
            tribe_points = f"🌐 Репутация в клане: {user_info_dict['tribe_points']}"
            influence = f"😎 Репутация: {user_info_dict['influence']}"
            tribe = f"👥 Клан: {user_info_dict['tribe']}"
            count_sms = f"💬 Количество сообщений: {user_info_dict['number_sms']['text']}"

            lvl = f"lvl {lvl_list['lvl']} ["
            for i in range(1, 11):
                if lvl_list["lvl_percent_short"] >= i:
                    lvl += "*"
                else:
                    lvl += "-"
            lvl += f"] lvl {lvl_list['lvl'] + 1}"

            msg = "👤 Профиль {0}\n"
            msg += f"{lvl}\n{warn}{ban}{achievements}\n\n{xp}\n{coins}\n{influence}\n\n" \
                  f"{tribe}\n{tribe_points}\n\n{count_sms}"

            user_info_detail.append(msg)
            user_ids.append(user_info_dict["user_id"])

        return user_info_detail, user_ids

    @control
    async def achievements_check(self, user_info_list: list):
        # self.user.self_generator(await self.manager_db.user_insert_one(self.user.class_dict, self.users_documents))
        # user_info_list = await self.user_info_list_add(user_id_list)
        user_info_detail = []
        user_ids = []

        for user_info in user_info_list:
            if user_info.achievements:
                msg = '👻 Ачивки {0}'
                for i in user_info.achievements:
                    msg += f"{i['text']} - {i['xp']}\n"
            else:
                msg = '👻 У {0} ачивок нет (つ . •́ _ʖ •̀ .)つ'
            user_info_detail.append(msg)
            user_ids.append(user_info.user_id)
        return user_info_detail, user_ids

    @control
    async def add_ban_user(self, user_id: int, peer_id: int, time_plus: int = 0, cause: str = '',
                           flag_in_class: bool = False):

        # user_info_detail = []
        # user_ids = []
        # user_ids_kick = []
        action = "kick"
        update = False
        # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        # if info:
        await self.user_conversation_update(user_id, peer_id)
        ban_info = self.users[user_id]["user_conversation"].punishments["ban"]
        if not ban_info.get("status"):
            await self.user_update(user_id)
            user_info = self.users[user_id]["user"]


            user_info_dict = user_info.class_dict
            lvl_list = await self.lvl_list(user_info_dict)
            await ban_give(user_info, self.users[user_id]["user_conversation"], lvl_list,
                               self.current_time, time_plus, cause)
            # if time_plus == 0:
            #     time_plus = lvl_list['limit']['ban_default_time']
            #
            # ban_info["start_time"] = self.current_time
            # ban_info["finish_time"] = self.current_time + time_plus
            # ban_info["status"] = True
            # ban_info["cause"] = cause
            # if ban_info.get("count"):
            #     user_info.punishments["ban"]["count"] += 1
            # else:
            #     user_info.punishments["ban"]["count"] = 1

            self.admin_info.punishments["count_ban"] += 1
            achievements = self.settings_info["ban_admin_awards"]
            await self.give_achievement(self.user_id, self.admin_info.punishments["count_ban"],
                                        achievements, self.users[self.user_id]["user"].achievements, "ban")


            ball = lvl_list['limit']['ban_default_xp'] * lvl_list['multiplier']
            user_info.xp += ball
            user_info.tribe_points += lvl_list['limit']['ban_default_tribe_points']

            certain_time = await self.display_time(time_plus)

            value = datetime.fromtimestamp(ban_info["finish_time"])
            end_time_msg = value.strftime('%d.%m.%Y %H:%M')

            achievements = self.settings_info["ban_awards"]

            action = "kick"
            update = True

            await self.give_achievement(user_id, user_info.punishments["ban"]["count"],
                                        achievements, user_info.achievements, "ban", ball)

            msg_ach = ""
            msg_admin_ach = ""
            if self.achievements.get(user_id):
                msg_ach = "\n\n👻 Полученные ачивки:\n" + \
                          "\n".join([i['text'] for i in self.achievements.get(user_id)])

            if self.achievements.get(self.user_id):
                msg_admin_ach = "\n\n👻 Админ, забанивший вас, получает ачивки:\n" + \
                                "\n".join([i['text'] for i in self.achievements.get(self.user_id)])

            msg = "{0} "
            if cause:
                msg += f", бан на {certain_time}\n📝 Причина: {cause}\n⏰ Время окончания: {end_time_msg}\n\n" \
                       f"🎁 У вас есть одна попытка разбана. " \
                       f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
            else:
                msg += f", бан на {certain_time}\n⏰ Время окончания: {end_time_msg}\n\n" \
                       f"🎁 У вас есть одна попытка разбана." \
                       f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
            #user_ids_kick.append(user_info.user_id)

            user_info.log["ban"].append({
                "creator_cmd": False,
                "current_time": self.current_time,
                "action": action,
                "user_id": self.user_id,
                "peer_id": peer_id,
                "cause": cause,
                "finish_time": ban_info["finish_time"],
                "time_plus": time_plus
            })

            self.admin_info.log["ban"].append({
                "creator_cmd": True,
                "current_time": self.current_time,
                "action": action,
                "user_id": user_id,
                "peer_id": peer_id,
                "cause": cause,
                "finish_time": ban_info["finish_time"],
                "time_plus": time_plus
            })

        else:
            msg = f"⚠ Данный [id{user_id}|пользователь] уже находится в бане."
        # else:
        #     msg = f"⚠ Данного [id{user_id}|пользователя], возможно, нет в беседе, но я попробую его исключить."

        return_dict = {"message": msg, "action": action, "update": update}

        return return_dict

    @control
    async def add_warn_user(self, user_id: int, peer_id: int, time_plus: int = 0, cause: str = '',
                            flag_in_class: bool = False):

        action = False
        update = False
        # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        # if info:
        await self.user_conversation_update(user_id, peer_id)
        warn_info = self.users[user_id]["user_conversation"].punishments["warn"]

        await self.user_update(user_id)
        user_info = self.users[user_id]["user"]
        user_info_dict = user_info.class_dict
        lvl_list = await self.lvl_list(user_info_dict)


        if not warn_info.get("warn_list"):
            warn_info["warn_list"] = []


        if len(warn_info["warn_list"]) >= lvl_list["limit"]["warn_limit"]:
            #warn_info["warn_list"] = []
            cause = "Достигнут лимит варнов"
            return await self.add_ban_user(user_id=user_id, time_plus=time_plus, cause=cause, flag_in_class=True)



        ball = lvl_list['limit']['warn_default_xp'] * lvl_list['multiplier']
        user_info.xp += ball
        user_info.tribe_points += lvl_list['limit']['warn_default_tribe_points']


        if time_plus == 0:
            time_plus = lvl_list['limit']['warn_default_time']

        warn_info["warn_list"].append(
            {
                "start_time": self.current_time,
                "finish_time": self.current_time + time_plus,
                "status": True,
                "cause": cause
            })
        user_info.punishments["warn"]["count"] = 1

        certain_time = await self.display_time(time_plus)
        value = datetime.fromtimestamp(self.current_time + time_plus)
        end_time_msg = value.strftime('%d.%m.%Y %H:%M')

        # action = True
        update = True

        self.admin_info.punishments["count_warn"] += 1
        achievements = self.settings_info["warn_admin_awards"]
        await self.give_achievement(self.user_id, self.admin_info.punishments["count_warn"],
                                    achievements, self.users[self.user_id]["user"].achievements, "warn")

        achievements = self.settings_info["warn_awards"]
        await self.give_achievement(user_info.user_id, user_info.punishments["warn"]["count"],
                                    achievements, user_info.achievements, "warn", ball)


        if len(warn_info["warn_list"]) == lvl_list["limit"]["warn_limit"]:
            warn_info["warn_list"] = []
            return await self.add_ban_user(user_id=user_id, time_plus=time_plus, cause=cause, flag_in_class=True)

        msg_ach = ""
        msg_admin_ach = ""
        if self.achievements.get(user_info.user_id):
            msg_ach = "\n\n👻 Полученные ачивки:\n" + \
                      "\n".join([i['text'] for i in self.achievements.get(user_info.user_id)])

        if self.achievements.get(self.user_id):
            msg_admin_ach = "\n\n👻 Админ, заварнивший вас, получает ачивки:\n" + \
                            "\n".join([i['text'] for i in self.achievements.get(self.user_id)])

        if cause:
            msg = "{0}," \
                  f" вам выдан варн [{len(warn_info['warn_list'])}/{lvl_list['limit']['warn_limit']}]" \
                  f"на {certain_time} \n📝 Причина: {cause}\n" \
                  f"⏰ Время окончания: {end_time_msg}{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
        else:
            msg = "{0}," \
                  f" вам выдан варн [{len(warn_info['warn_list'])}/{lvl_list['limit']['warn_limit']}]" \
                  f"на {certain_time}\n" \
                  f"⏰ Время окончания: {end_time_msg}{msg_ach}\n\n📊 XP: {user_info.xp}{msg_admin_ach}"
        # else:
        #     msg = f"⚠ Данного [id{user_id}|пользователя], возможно, нет в беседе\n" \
        #           f"❗ Обновите информацию командой /update."

        return_dict = {"message": msg, "action": action, "update": update}
        return return_dict

    @control
    async def give_plus_rep(self, user_id: int, influence: int = 0):
        action = False
        if influence:pass

        if self.users[self.user_id]["user"].influence > 1:
            self.users[self.user_id]["user"].influence -= 1





        # user_info.log.append({
        #     "cmd": "plus_rep",
        #     "creator_cmd": True,
        #     "current_time": self.current_time,
        #     "action": action,
        #     "user_id": self.user_id,
        #     "cause": cause,
        #     "finish_time": self.current_time + time_plus,
        #     "time_plus": time_plus
        # })
        # return_dict = {"message": msg, "action": action}
        # return return_dict




    @control
    async def add_ban_users(self, user_info_list: list, time_plus: int = 0, cause: str = ''):

        user_info_detail = []
        user_ids = []
        user_ids_kick = []



        for user_info in user_info_list:
            if not user_info.punishments["ban"].get("status"):

                user_info_dict = user_info.class_dict
                lvl_list = await self.lvl_list(user_info_dict)

                if time_plus == 0:
                    time_plus = lvl_list[0]['limit']['ban_default_time']

                user_info.punishments["ban"]["start_time"] = self.current_time
                user_info.punishments["ban"]["finish_time"] = self.current_time + time_plus
                user_info.punishments["ban"]["status"] = True
                user_info.punishments["ban"]["count"] += 1

                certain_time = await self.display_time(time_plus)

                value = datetime.fromtimestamp(user_info.punishments["ban"]["finish_time"])
                end_time_msg = value.strftime('%d.%m.%Y %H:%M')

                achievements = lvl_list[1]["ban_awards"]

                count = 0

                for i in achievements:
                    if i["count"] == user_info.punishments["ban"]["count"]:
                        flag = False
                        for j in user_info.achievements:
                            if j['text'] == i["text"]:
                                flag = True
                                break
                        if not flag:
                            user_info.achievements.append({'text': f'{lvl_list[1]["ban_awards_smiley"]} {i["text"]}',
                                                           "admin": self.user_id,
                                                           "count": user_info.punishments["ban"]["count"],
                                                           "xp": lvl_list[0]['limit']['ban_default_xp'],
                                                           "type": "ban",
                                                           "time_issuing": self.current_time})
                            count += 1

                if count != 0:
                    msg_ach = "\n\n👻 Полученные ачивки:\n" +\
                              "\n".join([i['name'] for i in user_info.achievements[-count:]])
                else:
                    msg_ach = ""

                msg = "{0} "
                if cause:
                    msg += f", бан на {certain_time}\n📝 Причина: {cause}\n⏰ Время окончания: {end_time_msg}\n\n" \
                           f"🎁 У вас есть одна попытка разбана на одну беседу. " \
                           f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}"
                else:
                    msg += f", бан на {certain_time}\n⏰ Время окончания: {end_time_msg}\n\n" \
                           f"🎁 У вас есть одна попытка разбана на одну беседу." \
                           f"Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}"

                user_ids_kick.append(user_info.user_id)
            else:
                msg = f"⚠ Данный [id{user_info.user_id}|пользователь] уже находится в бане."
            user_info_detail.append(msg)
            #user_ids.append(user_info.user_id)
        #if len(user_info_list) == 1:


        return user_info_detail, user_ids


class Work_user_conversation:

    def __init__(self, client, user_id, users_documents_bs):

        self.client = client
        self.user_id = user_id
        self.users_documents_bs = f"{users_documents_bs}"

        self.manager_db = MongoManager(self.client)
        self.user = User_conversation(user_id=self.user_id)

    # async def add_user_bs(self, user_info_list: list):
    #     self.user.self_generator(await self.manager_db.user_insert_one(self.user.class_dict, self.users_documents_bs))

class obj:
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [obj(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, obj(v) if isinstance(v, dict) else v)

    def __getattr__(self, item):
        return False

    @property
    def class_dict(self):
        return self.__dict__


class A:
    def __init__(self):
        self.user_id = 13423243
        self.user_info = {}

    def metod(self):
        print(B().user_info)

    def set_user_info(self, user_info):
        self.user_info[self.user_id] = user_info


class B(A):
    def __init__(self):
        super().__init__()


if __name__ == "__main__5":
    aa = A()
    aa.set_user_info(True)
    aa.metod()


if __name__ == "__main__4":
    d = {'a': 1, 'b': {'c': 2, 'gg': {'c': 3}}, 'd': ["hi", {'foo': "bar"}]}
    ob = obj(d)
    if ob.b.gg:
        print(ob.b.g)
    print(ob.class_dict)


if __name__ == "__main__1":
    sms = "🥴 Smile 🥴🥶"
    print(sms)
    import emoji

    #text = input('Введите текст ')
    #print(emoji.demojize(sms.split(" ")[0]))

    if len(sms.split(" ")[0]) != len(emoji.demojize(sms.split(" ")[0])):
        print("Yes")
if __name__ == "__main__2":
    from motor import MotorClient
    import asyncio
    #
    # uri = 'mongodb://localhost:27017'
    # client = MotorClient(uri)
    # wok = Work_user(client, 12345)
    # loop = asyncio.get_event_loop()
    # toke = loop.run_until_complete(wok.user_profile_info(12345))

    #User(test=228, slov={"user_id": 1})

    import yaml
    from pprint import pprint

    # with open('description_commands.yaml') as f:
    #     templates = yaml.safe_load(f)
    #
    # pprint(templates)

    with open('description_commands.yaml', encoding="utf-8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
    #pprint(read_data)
    loop = asyncio.get_event_loop()
    uri = 'mongodb://localhost:27017'
    client = MotorClient(uri)

    mongo_manager = MongoManager(client)
    wok = Work_user(mongo_manager, 55, 100)
    loop.run_until_complete(mongo_manager.settings_insert_one(read_data, "settings"))
    #loop.run_until_complete(mongo_manager.settings_update_one(read_data, "settings"))
    #test2 = loop.run_until_complete(wok.lvl_cmd_add_list({"xp": 12345}, "profile"))
    #test2 = loop.run_until_complete(wok.lvl_list({"xp": 700}))
    #test2 = loop.run_until_complete(wok.achievements_check(user_info_list=[123456]))
    #test2 = loop.run_until_complete(wok.add_ban_user(user_id=123456, peer_id=2000001, cause="Спам"))
    test2 = loop.run_until_complete(wok.add_warn_user(user_id=123456, peer_id=2000001, cause="Спам"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    #pprint(test2)
    print(test2)
    #test_1()
