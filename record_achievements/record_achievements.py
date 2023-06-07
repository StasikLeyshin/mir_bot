import functools
from datetime import datetime
import random

from mongodb import user_profile
from api.api_execute import inf, kick, kick_bs
from api import api_url


class record_achievements:

    def __init__(self, create_mongo, user_id):
        self.create_mongo = create_mongo
        self.user_id = user_id
        self.warn_awards = {
            1: "С почином, добро пожаловать на контроль",
            3: "На бан уже заработал, будем посмотреть",
            5: "Как ты только бан не получил? Или получил? Ну, всякое бывает",
            10: "FBI OPEN UP!",
            20: "Админ, ты в курсе, что есть перманентный бан? Двадцать варнов это уже ту мач"
        }
        self.ban_awards = {
            1: "Любопытно, стоит ли ждать назад?",
            2: "Посмотрите на это, урок не был усвоен. Не делайте так",
            5: "КТО ИЗ АДМИНОВ ТВОЙ ДРУГ? ПРИЗНАВАЙСЯ!",
            7: "Админ, он неисправим, одумайся",
            10: "Никаких больше вечеринок. Я отказываюсь давать разбан"
        }

    async def run(self, kol_warn=0, kol_ban=0, achievement=" ", ach_kol=0, res=0):
        msg = []
        ban = 0
        warn_chek = False
        ban_chek = False
        if int(kol_warn) in self.warn_awards:
            msg.append(f"🏅 {self.warn_awards[int(kol_warn)]}")
            res = await self.create_mongo.profile_users_add(self.user_id, f"🏅 {self.warn_awards[int(kol_warn)]}", -3)
            warn_chek = True
        if int(kol_ban) in self.ban_awards:
            msg.append(f"🎖 {self.ban_awards[int(kol_ban)]}")
            res = await self.create_mongo.profile_users_add(self.user_id, f"🎖 {self.ban_awards[int(kol_ban)]}", -8)
            ban_chek = True

        if not warn_chek and kol_warn != 0:
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-3)
        if not ban_chek and kol_ban != 0:
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-8)

        if achievement != " ":
            res = await self.create_mongo.profile_users_add(self.user_id, f"{achievement}", ach_kol)

        if res[1] <= -50:
            ban = 2
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-8)
            return ban, msg, res[1]

        if res[1] <= -30:
            ban = 1
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-8)
            if res[1] <= -50:
                ban = 2

            return ban, msg, res[1]

        return ban, msg, res[1]


class achievements:

    def __init__(self, client, user_id, v):

        self.client = client

        self.user_id = user_id
        self.v = v

        self.ach = []

        self.score = 0
        self.warn_awards = {
            1: "С почином, добро пожаловать на контроль",
            3: "На бан уже заработал, будем смотреть",
            5: "Как ты только бан не получил? Или получил? Ну, всякое бывает",
            10: "FBI OPEN UP!",
            20: "Админ, ты в курсе, что есть перманентный бан? Двадцать варнов это уже ту мач"
        }
        self.ban_awards = {
            1: "Любопытно, стоит ли ждать назад?",
            2: "Посмотрите на это, урок не был усвоен. Не делайте так",
            5: "КТО ИЗ АДМИНОВ ТВОЙ ДРУГ? ПРИЗНАВАЙСЯ!",
            7: "Админ, он неисправим, одумайся",
            10: "Никаких больше вечеринок. Я отказываюсь давать разбан"
        }
        self.sms_awards = {
            100: ["Ууф, сотка сообщений, у нас любитель початиться", 2],
            1000: ["Ого, тысяча сообщений, еще не флудер года, но всё впереди", 6],
            2000: ["That's a lot of masseges! How abount a little more? Две тысячи сообщений пройдено!", 9],
            5000: ["ГЛАВНЫЙ ФЛУДЕР ГОДА НАЙДЕН! ПЯТЬ ТЫСЯЧ СООБЩЕНИЙ ЕСТЬ!", 12],
            10000: ["ДЕСЯТЬ ТЫСЯЧ СООБЩЕНИЙ!!! ДЕСЯЯЯЯЯТЬ! НАСПАМИЛ НА БЕЗБЕДНУЮ ЖИЗНЬ", 15],
            20000: ["ТЫ ЧЕГО ДЕЛАЕШЬ, ТЫ ЧТО, БОГАТЫРЬ ЧТО ЛИ, КУДА СТОЛЬКО, КУДА??????", 20],
            30000: [
                "ТЫ ЧЕГО ТУТ ДЕЛАЕШЬ? выйди траву потрогай, в зал сходи, жену погладь, сколько можно в чате сидеть.",
                40],
            50000: ["ЭТОТ ЧЕЛОВЕК СПАМЕР. ОФИЦИАЛЬНО!", 50]
        }
        self.reputation_plus_awards = {
            1: ["А вы, я погляжу, хороший малый", 1],
            5: ["Добрый чел, позитивный", 3],
            10: ["Поднял репутацию уже десяти Си-Джеям!", 6],
            50: ["Репутация не палка: в руки не возьмёшь, а вы взяли... 50 раз", 9],
            200: ["ТЫ ПОТРЯСАЮЩИЙ 👉🏻👈🏻", 12]
        }
        self.reputation_minus_awards = {
            1: ["Токсик обнаружен", -0.001],
            2: ["Злой чел, негативный", -0.01],
            5: ["Самый душный в чате", -0.02],
            7: ["Ну давай, давай, нападай", -0.04],
            9: ["Я ведь не отстану, каждому токсику по перевоспитанию", -0.06],
            10: ["Вот это ты конечно натоксичил", -0.07],
            13: ["Сжёг рейтинг уже тринадцати людям", -0.08],
            16: ["Токсим токсим токсим каждый день", -0.09],
            20: ["Партия недовольна вами, минус тарелка рис", -0.1],
            30: ["ТРИЦАТОЧКА, ТРИ И ЦАТОЧКА, ТОКСИК ВСЕХ ТОКСИКОВ НАЙДЕН", -0.11]
        }
        self.roulette_awards = {
            1: ["🔫 Угадай куда я шмальну", 0.5],
            3: ["💥 НАТАЛЬЯ МОРСКАЯ ПЕХОТА", 1.666],
            5: ["☀ It's high noon", 2.333],
            7: ["☠ Самый меткий стрелок на фронтире", 6.666],
            10: ["🎲 Любимчик Фортуны", 7.777],
            18: ["❄ Финский снайпер", 11.999]
        }
        self.ban = {
            -50: self.add_global_ban,
            -30: self.add_ban
        }

        self.score_minus = {
            "warn": -8,
            "ban": -14
        }
        self.reputation_minus = {
            (20, 999): 0.02,
            (6, 20): 0.009,
            (0, 5): 0.005,
            (0, -5): -0.03,
            (-6, -10): -0.06,
            (-10, -999): -0.08
        }

        self.reputation_plus_sl = {
            0: 3,
            20: 4,
            30: 5,
            40: 6,
            50: 7,
            60: 8,
            100: 9,
            140: 10,
            180: 11,
            200: 12
        }

        self.reputation_minus_sl = {
            20: 2,
            30: 3,
            40: 4,
            50: 5,
            60: 6,
            70: 7,
            120: 8,
            170: 9,
            200: 10
        }

    def is_int(self, txt):
        try:
            int(txt)
            return True
        except:
            return False

    def chat_id(self, peer_id):
        return str(int(peer_id) - 2000000000)

    # поиск по html
    def fin(self, s, first, last):
        try:
            start = s.index(str(first)) + len(str(first))
            end = s.index(str(last), start)
            return s[start:end]
        except ValueError:
            return ""

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

    async def check_global_ban(self, apis, us):
        if us.__dict__.get("globan"):
            print(us.__dict__)
            if us.globan[str(us.globan["count"])]["status"]:
                peer_ids = await us.get_globan_peer_ids()
                await apis.api_post("execute",
                                    code=kick_bs(users=self.user_id, chat_id=[self.chat_id(i) for i in peer_ids]),
                                    v=self.v)
                return True
        return False


    async def reputation_calculation(self, us, rep=False):
        if rep:
            us.change_score_bs_profile(self.score)
            us.change_score_bs_profile(0.001, flag=True)
            us.user_info_update()
            return round(us.score, 3)

        influence = 0
        if self.score < 0:
            for i in self.reputation_minus:
                if i[1] <= self.score < i[0]:
                    influence = self.reputation_minus[i]
        else:
            for i in self.reputation_minus:
                if i[0] <= self.score < i[1]:
                    influence = self.reputation_minus[i]
        for i in self.ach:
            fl = False
            for j in us.achievements:
                if j != "count":
                    if us.achievements[j]["text"] == i["name"]:
                        fl = True
            if not fl:
                us.add_achievements_bs_profile(i["count"], i["name"], i["time_issuing"], -5411326, i["type"])
        #print(self.score)
        self.score += us.influence * 10
        us.change_score_bs_profile(self.score)
        us.change_score_bs_profile(influence, flag=True)



    async def admin_info(self, user_id):
        if self.user_id[0] == "-":
            msg = f"⚠ Данная [club{str(user_id)[1:]}|группа] является администратором беседы"
        else:
            msg = f"⚠ Данный [id{user_id}|пользователь] является администратором беседы"
        return msg

    async def user_info(self, apis, admin_id):
        if str(self.user_id)[0] == "-":
            result = await apis.api_post("execute", code=inf(v=self.v, id=self.user_id, f=0, from_id=admin_id), v=self.v)
            name = "[club"+str(self.user_id[1:])+"|"+str(result[1]) + "]"
            im = f"[id{admin_id}|{result[2]} {result[3]}]"
        else:
            result = await apis.api_post("execute", code=inf(v=self.v, id=self.user_id, f=1, from_id=admin_id), v=self.v)
            name = "[id" + str(self.user_id) + "|" + str(result[1]) + " " + str(result[2]) + "]"
            im = f"[id{admin_id}|{result[3]} {result[4]}]"
        return name, im, result[0]


    async def check_ban_score(self, apis, score, peer_id, admin_id=-5411326, time_plus=604800, punishment="", us=None, res=None):
        # for i in self.punishments:
        #     if score < i:
        #         self.punishments[i](peer_id, start_time, end_time, admin_id, cause=-1)
        flag = False
        if score <= -50:
            await self.add_global_ban(apis, peer_id, admin_id,
                                "Рейтинг достиг отметки ниже -50", us=us, res=res)
            flag = True
        if punishment != "ban":
            if score <= -30:
                await self.add_ban(apis, peer_id, admin_id, time_plus,
                                   "Рейтинг достиг отметки ниже -30", us=us, res=res)
                flag = True
        return flag



    async def add_warn(self, apis, peer_id, admin_id, time_plus=86400, cause=-1, forward=None):
        us = user_profile(self.client, self.user_id, peer_id)
        #print(us.__dict__)
        if us.admin:
            return False, await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                              message=await self.admin_info(us.user_id), random_id=0)

        res = await self.user_info(apis, admin_id)

        start_time = res[2]
        end_time = res[2] + int(time_plus)

        us.add_warn_bs_profile(start_time, end_time, cause, admin_id)

        self.score += self.score_minus["warn"]
        #us.change_score_bs_profile(self.score_minus["warn"])

        if int(us.warn['count_old']) - 1 in self.warn_awards:
            self.ach.append({'name': '🏅 ' + self.warn_awards[int(us.warn['count_old'] - 1)],
                             "number": int(us.warn['count_old'] - 1),
                             "count": self.score_minus["warn"],
                             "type": "warn",
                             "time_issuing": start_time})
        # await self.reputation_calculation(us)

        if await self.check_ban_score(apis, us.score, peer_id, admin_id, time_plus, "warn", us, res):
            return

        await self.reputation_calculation(us)

        if int(us.warn['count']) == 0:
            await self.add_ban(apis, peer_id, admin_id, time_plus, "Достигнут лимит варнов", us, res)
            return

        ply = await self.display_time(time_plus)

        value = datetime.fromtimestamp(end_time)
        end_time_msg = value.strftime('%d.%m.%Y %H:%M')

        if self.ach:
            msg_ach = "\n\n👻 Полученные ачивки:\n" + "\n".join([i['name'] for i in self.ach])
        else:
            msg_ach = ""

        if cause != -1:
            msg = f"{res[0]}, вам выдан варн [{us.warn['count']}/3] на {ply} \n📝 Причина: {cause}\n" \
                  f"⏰ Время окончания: {end_time_msg}{msg_ach}\n\n📊 Рейтинг: {us.score}"  # от администратора" \
            # f" {im}" \
            # f"\n📝 Причина: {cause}\n⏰ Время окончания: {time}"
        else:
            msg = f"{res[0]}, вам выдан варн [{us.warn['count']}/3] на {ply}\n" \
                  f"⏰ Время окончания: {end_time_msg}{msg_ach}\n\n📊 Рейтинг: {us.score}"  # от администратора" \

        if forward:
            await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                message=msg, random_id=0, forward=forward)
        else:
            await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                message=msg, random_id=0)


        return us

    async def add_ban(self, apis, peer_id, admin_id, time_plus=86400, cause=-1, us=None, res=None):
        if not us:
            us = user_profile(self.client, self.user_id, peer_id)
        if us.admin:
            return False, await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                              message=await self.admin_info(us.user_id), random_id=0)

        if not res:
            res = await self.user_info(apis, admin_id)

        start_time = res[2]
        end_time = res[2] + int(time_plus)

        is_ban = us.add_ban_bs_profile(start_time, end_time, cause, admin_id)

        if is_ban == -1:
            if str(us.user_id)[0] == "-":
                msg = f"⚠ Данная [club{str(us.user_id)[1:]}|группа] уже находится в бане"
            else:
                msg = f"⚠ Данный [id{us.user_id}|пользователь] уже находится в бане"
            await apis.api_post("execute", code=kick(users=[us.user_id], chat_id=self.chat_id(peer_id)), v=self.v)
            return False, await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                              message=msg, random_id=0)

        #us.change_score_bs_profile(self.score_minus["punishments"])
        self.score += self.score_minus["ban"]

        if await self.check_ban_score(apis, us.score, peer_id, start_time, end_time, admin_id, "ban", us):
            return

        #await self.reputation_calculation(us)

        if int(us.ban['count']) in self.ban_awards:
            self.ach.append({'name': '🎖' + self.ban_awards[int(us.ban['count'])],
                             "number": int(us.ban['count']),
                             "count": self.score_minus["ban"],
                             "type": "ban",
                             "time_issuing": start_time})
        await self.reputation_calculation(us)

        ply = await self.display_time(time_plus)

        value = datetime.fromtimestamp(end_time)
        end_time_msg = value.strftime('%d.%m.%Y %H:%M')


        if self.ach:
            msg_ach = "\n\n👻 Полученные ачивки:\n" + "\n".join([i['name'] for i in self.ach])
        else:
            msg_ach = ""


        if cause != -1:
            msg = f"{res[0]}, бан на {ply}\n📝 Причина: {cause}\n⏰ Время окончания: {end_time_msg}\n\n" \
                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}" \
                  f"\n\n📊 Рейтинг: {us.score}"  # от администратора" \
                  #f" {im}" \
                  #f"\n📝 Причина: {cause}\n⏰ Время окончания: {time}"
        else:
            msg = f"{res[0]}, бан на {ply}\n⏰ Время окончания: {end_time_msg}\n\n" \
                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.{msg_ach}" \
                  f"\n\n📊 Рейтинг: {us.score}"  # от администратора" \
                  #  f" {im}" \
                  #  f"\n⏰ Время окончания: {time}"


        await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                            message=msg, random_id=0)

        await apis.api_post("execute", code=kick(users=[us.user_id], chat_id=self.chat_id(peer_id)), v=self.v)



        return us

    async def add_global_ban(self, apis, peer_id, admin_id, cause=-1, us=None, res=None):
        if not us:
            us = user_profile(self.client, self.user_id, peer_id, globan=True)

        if us.admin:
            return False, await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                              message=await self.admin_info(us.user_id), random_id=0)

        if not res:
            res = await self.user_info(apis, admin_id)

        start_time = res[2]

        is_globan = us.add_globan_bs_profile(start_time, cause, admin_id)

        await self.reputation_calculation(us)

        if is_globan[0] == 1:
            await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                message=f"Данный [id{us.user_id}|пользователь] добавлен в глобальный бан. "
                                f"Оттуда ещё никто не возвращался...", random_id=0)
        elif is_globan[0] == 2:
            await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                message=f"Данный [id{us.user_id}|пользователь] уже есть в глобальном бане. "
                                f"И он оттуда скорее всего не вернётся...", random_id=0)

        await apis.api_post("execute",
                            code=kick_bs(users=us.user_id, chat_id=[self.chat_id(i) for i in is_globan[1]]),
                            v=self.v)
        return us

    async def add_sms(self, apis, peer_id, type_sms, time_issuing, us=None):
        if not us:
            us = user_profile(self.client, self.user_id, peer_id)

        gl = await self.check_global_ban(apis, us)
        if gl:
            return
        # if us.__dict__.get("globan"):
        #     if us.globan[str(us.globan["count"])]["status"]:
        #         peer_ids = await us.get_globan_peer_ids()
        #         await apis.api_post("execute",
        #                             code=kick_bs(users=self.user_id, chat_id=[self.chat_id(i) for i in peer_ids]),
        #                             v=self.v)
        #         return
        self.ach = []
        us.add_sms_bs_profile(type_sms)
        kol_sms = us.__dict__[f"{type_sms}"]
        if int(kol_sms) in self.sms_awards and type_sms == "text":
            self.ach.append({'name': '🏆 ' + self.sms_awards[int(kol_sms)][0],
                             "number": int(kol_sms),
                             "count": self.sms_awards[int(kol_sms)][1],
                             "type": "sms",
                             "time_issuing": time_issuing})

            await self.reputation_calculation(us)

        if self.ach:
            msg_ach = "\n\n👻 Полученные ачивки:\n" + "\n".join([i['name'] for i in self.ach])
            msg = f"{msg_ach}" \
                  f"\n\n📊 Рейтинг: {us.score}"
        else:
            msg = ""

        return msg


    # async def score_control(self, name):
    #     if name == "user_profile":
    #         pass


    def score_control(fun):
        #@functools.wraps(fun)
        async def wrapper(self, *args, **kwargs):
            if fun.__name__ == "user_profile_info":
                uss = user_profile(self.client, kwargs['user_id'], kwargs['peer_id'])
                if uss.score > 20 or uss.admin:
                    us = user_profile(self.client, self.user_id, kwargs['peer_id'])
                    kwargs['us'] = us
                    kwargs['peer_id'] = kwargs['user_id']
                    kwargs['user_id'] = self.user_id
                else:
                    kwargs['us'] = uss
                    kwargs['peer_id'] = kwargs['user_id']


            elif fun.__name__ == "plus_rep":
                uss = user_profile(self.client, kwargs['user_id'], kwargs['peer_id'])
                fl = await self.check_ban_score(kwargs['apis'], uss.score, kwargs['peer_id'], us=uss)
                if fl:
                    return False
                if uss.admin:
                    access_amount = 100
                else:
                    access_amount = 3
                    for i in self.reputation_plus_sl:
                        if i <= uss.score:
                            access_amount = self.reputation_plus_sl[i]
                kwargs['access_amount'] = access_amount
                kwargs['us'] = uss


            elif fun.__name__ == "minus_rep":
                uss = user_profile(self.client, kwargs['user_id'], kwargs['peer_id'])
                fl = await self.check_ban_score(kwargs['apis'], uss.score, kwargs['peer_id'], us=uss)
                if fl:
                    return False
                if uss.admin:
                    access_amount = 100
                else:
                    access_amount = 0
                    for i in self.reputation_minus_sl:
                        if i <= uss.score:
                            access_amount = self.reputation_minus_sl[i]
                if access_amount == 0:
                    return f"⛔ У вас недостаточно баллов для осуждения."
                kwargs['access_amount'] = access_amount
                kwargs['us'] = uss


            elif fun.__name__ == "roulette":
                uss = user_profile(self.client, self.user_id, kwargs['peer_id'])
                if uss.score <= -15 and not uss.admin:
                    return False
                kwargs['us'] = uss
                kwargs['access_amount'] = 1

            return await fun(self, *args, **kwargs)

        return wrapper


    @score_control
    async def user_profile_info(self, apis, user_id, us=None, peer_id="d"):
        #us = user_profile(self.client, user_id, peer_id)
        # if str(user_id)[0] == "-":
        #     return "Таких не знаем🤖"
        warn = ""
        ban = ""
        #if self.is_int(peer_id):
            #info = await self.create_mongo.user_info(user_id, self.peer_id)
            # if not info:
            #     return "Такого не существует в природе👽"
        if "warn" in us.__dict__:
            if us.warn.get('count'):
                if us.warn['count'] != 0:
                    warn += f"☢ Варны: [{us.warn['count']}/3]\n"
                warn += f"🤡 Количество варнов: {us.warn['count_old'] - 1}\n\n"
        if "ban" in us.__dict__:
            if us.ban.get('count'):
                ban = f"🤡 Количество банов: {us.ban['count']}\n\n"

        result = await apis.api_post("users.get", v=self.v, user_ids=f"{user_id}", name_case="gen")
        name = f'{result[0]["first_name"]} {result[0]["last_name"]}'


        awards = ""
        #if len(us.achievements["count"]) >= 1:
        if "text" not in us.__dict__:
            kol = 0
        else:
            kol = us.text
        if "influence" not in us.__dict__:
            influence = "0.25"
        else:
            influence = us.influence
        if "achievements" in us.__dict__:
            if "count" in us.achievements:
                if us.achievements["count"] == 0:
                    awards = f"💬 Количество сообщений: {kol}\n📊 Рейтинг: {us.score}\n👻 Ачивки:\n📛 Ачивок нет"

                else:
                    achievements = []
                #for i in us.achievements:
                    #if i != "count":
                        #achievements.append(f'{us.achievements[i]["text"]}  {us.achievements[i]["score"]}')
                #awards = f"💬 Количество сообщений: {kol}\n📊 Рейтинг: {us.score}\n👻 Ачивки:\n" + "\n".join(achievements)
                    awards = f"💬 Количество сообщений: {kol}\n📊 Рейтинг: {us.score}\n" \
                             f"😎 Репутация: {influence}\n" \
                             f"👻 Количество ачивок: {us.achievements['count']}"
            else:
                awards = f"💬 Количество сообщений: {kol}\n📊 Рейтинг: {us.score}\n👻 Ачивки:\n📛 Ачивок нет"

        else:
            awards = f"💬 Количество сообщений: {kol}\n📊 Рейтинг: {us.score}\n😎 Репутация: {influence}\n📛 Ачивок нет"


        #p = requests.get('https://vk.com/foaf.php?id=' + str(self.from_id))
        s = await api_url('https://vk.com/foaf.php?id=' + str(user_id)).get_html()
        l = self.fin(s, "<ya:created dc:date=", "/>\n")
        q = l[1:-7]
        q = q[:-9]
        q = q.replace('-', '.')
        q = q.split(".")
        try:

            q = str(q[2]) + "." + str(q[1]) + "." + str(q[0])
            await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                message=f"👤 Профиль [id{user_id}|{name}]\n\n📆 Дата регистрации: {q}\n\n{warn}{ban}{awards}",
                                random_id=0)
        except:
            await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                message=f"👤 Профиль [id{user_id}|{name}]\n\n{warn}{ban}{awards}",
                                random_id=0)


        # await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
        #                     message=f"👤 Профиль [id{user_id}|{name}]\n\n{warn}{ban}{awards}",
        #                     random_id=0)

        return True#f"👤 Профиль [id{user_id}|{name}]\n\n📆 Дата регистрации: {q}\n\n{warn}{ban}{awards}"

    @score_control
    async def plus_rep(self, apis, user_id, start_time, time_plus=86400, us=None, peer_id="d", access_amount=0,
                       number_issued=0):
        if us:
            #start_time = start_time + int(time_plus)
            count = us.plus_rep(access_amount, number_issued, start_time, time_plus)
            end_time = start_time + int(time_plus)
            if count:
                if count == -1:
                    return f"⛔ Все попытки за день израсходованы"

        fl = False
        for i in self.reputation_plus_awards:
            for j in range(us.rep_plus_new["count"]-count, us.rep_plus_new["count"] + 1):
                if i == j:
                    fla = False
                    for k in us.achievements:
                        if k != "count":
                            #print(us.achievements[k]["text"], '😇 ' + self.reputation_plus_awards[j][0])
                            if us.achievements[k]["text"] == '😇 ' + self.reputation_plus_awards[j][0]:
                                fla = True
                    if not fla:
                        self.ach.append({'name': '😇 ' + self.reputation_plus_awards[j][0],
                                         "number": j,
                                         "count": self.reputation_plus_awards[j][1],
                                         "type": "plus_rep",
                                         "time_issuing": start_time})
                    fl = True
        if fl:
            self.score += int(us.rep_plus_new['count'])
            await self.reputation_calculation(us)
            self.score = 0
        # if int(us.rep_plus_new["count"]) in self.reputation_plus_awards:
        #     self.ach.append({'name': '😇 ' + self.reputation_plus_awards[int(us.rep_plus_new["count"])][0],
        #                      "number": int(us.rep_plus_new['count']),
        #                      "count": self.reputation_plus_awards[int(us.rep_plus_new["count"])][1],
        #                      "type": "plus_rep",
        #                      "time_issuing": start_time})
        #     self.score += int(us.rep_plus_new['count'])
        #     await self.reputation_calculation(us)
        #     self.score = 0

        if us.influence < 0:
            influence = 0.001
        else:
            influence = us.influence
        self.score += influence * count

        uss = user_profile(self.client, self.user_id, peer_id)
        sc = await self.reputation_calculation(uss, True)

        fl = await self.check_ban_score(apis, sc, peer_id, us=uss)
        if fl:
            return False

        #znak = "+"
        #if us.influence < 0:
            #znak = "-"
        if self.ach:
            #ach = f"\n\n👻 [id{self.from_id}|Вы] получили ачивку:\n\n
            msg_ach = f"\n\n👻 [id{user_id}|Вы] получили ачивку:\n\n" + "\n".join([i['name'] for i in self.ach])
            msg = f"✅ Уважение оказано ([id{self.user_id}|+{round(influence * count, 3)}]){msg_ach}"
        else:
            msg = f"✅ Уважение оказано ([id{self.user_id}|+{round(influence * count, 3)}])"

            # await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                # message=f"✅ Уважение оказано ([id{user_id}|+0.25])", forward=self.answer_msg(), random_id=0)


        return msg

    @score_control
    async def minus_rep(self, apis, user_id, start_time, time_plus=86400, us=None, peer_id="d", access_amount=0,
                       number_issued=0):
        if us:
            #start_time = start_time + int(time_plus)
            count = us.plus_rep(access_amount, number_issued, start_time, time_plus, "minus_rep_new")
            end_time = start_time + int(time_plus)
            if count:
                if count == -1:
                    return f"⛔ Все попытки за день израсходованы"

        #for i in
        # if int(us.minus_rep_new["count"]) in self.reputation_minus_awards:
        #     self.ach.append({'name': '😈 ' + self.reputation_minus_awards[int(us.minus_rep_new["count"])][0],
        #                      "number": int(us.minus_rep_new['count']),
        #                      "count": self.reputation_minus_awards[int(us.minus_rep_new["count"])][1],
        #                      "type": "plus_rep",
        #                      "time_issuing": start_time})
        #     self.score += int(us.minus_rep_new['count'])
        #     await self.reputation_calculation(us)
        #     self.score = 0

        fl = False
        for i in self.reputation_minus_awards:
            # print("i", i)
            for j in range(us.minus_rep_new["count"] - count, us.minus_rep_new["count"] + 1):
                # print("j", j)
                if i == j:
                    fla = False
                    for k in us.achievements:
                        if k != "count":
                            # print(us.achievements[k]["text"], '😇 ' + self.reputation_minus_awards[j][0])
                            if us.achievements[k]["text"] == '😈 ' + self.reputation_minus_awards[j][0]:
                                fla = True
                    if not fla:
                        self.ach.append({'name': '😈 ' + self.reputation_minus_awards[j][0],
                                         "number": j,
                                         "count": self.reputation_minus_awards[j][1],
                                         "type": "plus_rep",
                                         "time_issuing": start_time})
                    fl = True
        if fl:
            self.score += int(us.minus_rep_new['count'])
            await self.reputation_calculation(us)
            self.score = 0

        if us.influence < 0:
            influence = 0.001
        else:
            influence = us.influence

        self.score -= influence * count

        uss = user_profile(self.client, self.user_id, peer_id)
        sc = await self.reputation_calculation(uss, True)

        fl = await self.check_ban_score(apis, sc, peer_id, us=uss)
        if fl:
            return False

        #znak = ""
        #if us.influence < 0:
            #znak = "-"
        #print(influence * count)
        if self.ach:
            #ach = f"\n\n👻 [id{self.from_id}|Вы] получили ачивку:\n\n
            msg_ach = f"\n\n👻 [id{user_id}|Вы] получили ачивку:\n\n" + "\n".join([i['name'] for i in self.ach])
            msg = f"✅ Осуждение оказано ([id{self.user_id}|-{round(influence * count, 3)}]){msg_ach}"
        else:
            msg = f"✅ Осуждение оказано ([id{self.user_id}|-{round(influence * count, 3)}])"

            # await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                # message=f"✅ Уважение оказано ([id{user_id}|+0.25])", forward=self.answer_msg(), random_id=0)


        return msg


    @score_control
    async def roulette(self, apis, start_time, time_plus=86400, us=None, peer_id="d", access_amount=0,
                       number_issued=0, number=1):
        rul = {
            1: -9,
            2: -11,
            3: -13,
            4: -15,
            5: -17
        }
        if us:
            end_time = start_time + int(time_plus)
            if int(number) >= 1:
                if int(number) < 6:
                    ran = random.randint(1, 6)
                    if ran > int(number):
                        count = us.add_roulette(access_amount, number_issued, start_time, time_plus, True)
                    else:
                        count = us.add_roulette(access_amount, number_issued, start_time, time_plus, False)
                        ran = rul[number]

                    if int(count) != int(start_time + time_plus):
                        timestamp = count
                        value = datetime.fromtimestamp(timestamp)
                        time = value.strftime('%d.%m.%Y %H:%M')
                        return 0, f"🔌 Ваш пистолет на подзарядке, приходите после {time}"
                    # else:
                    #     ran = -4
                else:
                    return 0, f"😳 Как я столько пуль в барабан заряжу, только если солью или дробью, но так не интересно"
            elif number == 0:
                return 0, "🧐 Холостой пистолет не заряжаем"
            else:
                return 0, f"😳 Это куда ж минус то, пуля назад лететь будет??"

        if int(us.roulette["count"]) in self.roulette_awards and ran > 0:
            self.ach.append({'name': self.roulette_awards[int(us.roulette["count"])][0],
                             "number": int(us.roulette['count']),
                             "count": self.roulette_awards[int(us.roulette["count"])][1],
                             "type": "roulette",
                             "time_issuing": start_time})
            self.score += int(us.roulette['count'])
            #await self.reputation_calculation(us)
            #self.score = 0

        # if us.influence < 0:
        #     influence = 0.001
        # else:
        #     influence = us.influence
        self.score += int(ran) * 1.1

        #uss = user_profile(self.client, self.user_id, peer_id)
        sc = await self.reputation_calculation(us)
        us.user_info_update()

        fl = await self.check_ban_score(apis, us.score, peer_id, us=us)

        if fl:
            return 1, False
        #if fl:
            #return False

        #znak = ""
        #if us.influence < 0:
            #znak = "-"
        ret = f"\n\n📊 Рейтинг: {us.score}"
        if ran < 0:
            return 1, f"😭 К сожалению вы проиграли.{ret}"
        if self.ach:
            #ach = f"\n\n👻 [id{self.from_id}|Вы] получили ачивку:\n\n
            msg_ach = f"\n\n👻 [id{self.user_id}|Вы] получили ачивку:\n\n" + "\n".join([i['name'] for i in self.ach])
            msg = f"🤠 Сегодня фортуна на вашей стороне, вы победили.{msg_ach}{ret}"
        else:
            msg = f"🤠 Сегодня фортуна на вашей стороне, вы победили.{ret}"

            # await apis.api_post("messages.send", v=self.v, peer_id=peer_id,
                                # message=f"✅ Уважение оказано ([id{user_id}|+0.25])", forward=self.answer_msg(), random_id=0)


        return 1, msg


    async def transfer_points(self):
        pass

    async def conversion_points(self):
        pass
        #await get_all_profile()
