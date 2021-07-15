# -*- coding: utf-8 -*-
import asyncio
import json
import re
from datetime import datetime


from api.methods import methods
from api import api_url

class commands:

    def __init__(self, v, club_id, message, apis, them, create_mongo, collection_bots, document_tokens, url_dj):

        self.v = v
        self.club_id = club_id
        self.message = message
        self.peer_id = self.message["peer_id"]
        self.from_id = self.message["from_id"]
        self.date = self.message["date"]
        self.id_sms = self.message["id"]
        self.text = self.message["text"]
        self.conversation_message_id = self.message["conversation_message_id"]
        self.message_id = self.message["id"]
        self.fwd_messages = self.message["fwd_messages"]
        self.attachments = self.message["attachments"]
        self.methods = methods(self.v, self.club_id)
        self.apis = apis
        self.them = them
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.url_dj = url_dj
        self.admin_list = [15049950, 216758639, 597624554]
        #self.admin_list = [597624554, 456204202]
        self.subjects = {"Рус + мат(проф.) + инф": "Математика Русский Информатика и ИКТ",
                         "Рус + мат(проф.) + физ": "Математика Русский Физика",
                         "Рус + мат(проф.) + хим": "Математика Русский Химия",
                         "Рус + мат(проф.) + общ": "Математика Русский Обществознание",
                         "Рус + общ + ист": "Русский Обществознание История",
                         "Рус + мат(проф.) + твор": "Математика Русский Творческий экзамен",
                         "Рус + общ + твор": "Русский Обществознание Творческий экзамен"}

        self.subjects_opposite = {"Рус + мат(проф.) + инф": "math&rus&info",
                         "Рус + мат(проф.) + физ": "math&rus&phys",
                         "Рус + мат(проф.) + хим": "math&rus&chem",
                         "Рус + мат(проф.) + общ": "math&rus&soc",
                         "Рус + общ + ист": "rus&soc&hist",
                         "Рус + мат(проф.) + твор": "math&rus&art",
                         "Рус + общ + твор": "rus&soc&art"}

        self.sms_awards = {
            100: ["Ууф, сотка сообщений, у нас любитель початиться", 2],
            1000: ["Ого, тысяча сообщений, еще не флудер года, но всё впереди", 6],
            2000: ["That's a lot of masseges! How abount a little more? Две тысячи сообщений пройдено!", 9],
            5000: ["ГЛАВНЫЙ ФЛУДЕР ГОДА НАЙДЕН! ПЯТЬ ТЫСЯЧ СООБЩЕНИЙ ЕСТЬ!", 12]
        }
        self.reputation_plus_awards = {
            1: ["А вы, я погляжу, хороший малый", 1],
            5: ["Добрый чел, позитивный", 3],
            10: ["Поднял репутацию уже десяти Си-Джеям!", 6]
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
            20: ["Партия недовольна вами, минус тарелка рис", -0.1]
        }

    def button_vk(self, label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    def menu(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Вопросы", color="positive"), self.button_vk(label="Направления", color="positive")],
                [self.button_vk(label="Команды", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_education(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Бакалавриат / Специалитет", color="positive"),
                 self.button_vk(label="Магистратура", color="positive"),
                 self.button_vk(label="Колледж", color="positive")],
                [self.button_vk(label="Команды", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def direction(self):
        r = "primary"
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Команды", color="negative")],
                [self.button_vk(label="Рус + мат(проф.) + инф", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + физ", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + общ", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + хим", color=r)],
                [self.button_vk(label="Рус + общ + ист", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + твор", color=r)],
                [self.button_vk(label="Рус + общ + твор", color=r)]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def keyboard_warn(self, tex):
        r = "primary"
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Заварнить", color="positive", payload=tex)]
            ],
            "inline": True
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def keyboard_answer_admin(self, tex):
        r = "primary"
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Ответить", color="positive", payload=tex)]
            ],
            "inline": True
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard


    def keyboard_empty(self):
        r = "primary"
        keyboard = {
            "one_time": False,
            "buttons": []
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def answer_msg(self):
        msg = {
            "conversation_message_ids": [self.conversation_message_id],
            "peer_id": self.peer_id,
            "is_reply": True
        }
        msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
        msg = str(msg.decode('utf-8'))
        return msg

    def answer_msg_other(self):
        msg = {
            "conversation_message_ids": [self.conversation_message_id],
            "peer_id": self.peer_id,
        }
        msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
        msg = str(msg.decode('utf-8'))
        return msg

    def answer_msg_other_parameters(self, peer_id, conversation_message_id):
        msg = {
            "conversation_message_ids": [conversation_message_id],
            "peer_id": peer_id,
        }
        msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
        msg = str(msg.decode('utf-8'))
        return msg

    def answer_msg_parameters(self, peer_id, conversation_message_id):
        msg = {
            "conversation_message_ids": [conversation_message_id],
            "peer_id": peer_id,
            "is_reply": True
        }
        msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
        msg = str(msg.decode('utf-8'))
        return msg

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # ищем фото в высоком разрешении json
    async def photo_r_json(self, data):
        photo = max(data, key=lambda x: x['width'] * x['height'])
        return photo

    # определение скрин имени
    async def opredel_skreen(self, g, text):
        if "vk.com/" in str(text):
            r = re.findall(r'/\w+.\w+', g)
            t = r[-1]
            t = t[1:]
            return t

        elif "[id" in str(text) or "[club" in str(text):
            l = g.find('|')
            l2 = g.find('id')
            k = g[:l]
            k2 = k[l2 + 2:]
            k = k[1:]
            k = k.replace("club", "")
            k = k.replace("id", "")
            if "[club" in str(text):
                k = "-" + str(k)
        return k

    def chat_id(self):
        return str(int(self.peer_id) - 2000000000)


    def chat_id_param(self, per_id):
        return str(int(per_id) - 2000000000)

    def is_int(self, s):
        try:
            int(s)
            return True
        except:
            return False


    # получения текста после \n
    async def txt_warn(self, g):
        l = g.find('\n')
        if l == -1:
            return -1
        k = g[l:]
        k = k.replace(".", " ")
        k = k.replace("\n", "")
        k = k.lstrip()
        return k

    # преобразование часов/минут в секунды
    async def preobrz(self, vre):
        g = vre.lower().split(" ")
        # print(g)
        for i, item in enumerate(g):
            if "мин" or "час" or "день" or "год" or "лет" or "дне" or "дн" in item:
                if self.is_int(g[i - 1]):
                    if "мин" in item:
                        sek = int(g[i - 1]) * 60
                        return sek
                    elif "час" in item:
                        sek = int(g[i - 1]) * 3600
                        return sek
                    elif "ден" in vre or "дне" in item or "дн" in item:
                        sek = int(g[i - 1]) * 86400
                        return sek
                    elif "год" in item or "лет" in item:
                        sek = int(g[i - 1]) * 31536000
                        return sek
        return 86400


    # отображение времени по секундам
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

    async def getting_user_id(self):

        if "reply_message" in self.message or self.fwd_messages != []:
            if "reply_message" in self.message:
                user_id = self.message["reply_message"]["from_id"]
            else:
                user_id = self.fwd_messages[0]["from_id"]
            if self.is_int(user_id):
                user_id = str(user_id)
                return user_id
            else:
                return False
        elif len(self.text.lower().split(' ')) > 1:
            if "vk.com/" in self.text.lower():
                t = await self.opredel_skreen(self.text.lower().split(' ')[1], self.text.lower())
                # test = await vk.api.utils.resolve_screen_name(screen_name=t)
                test = await self.apis.api_post("utils.resolveScreenName", v=self.v, screen_name=t)
                if test["type"] == "group":
                    user_id = "-" + str(test["object_id"])
                else:
                    user_id = test["object_id"]
                if self.is_int(user_id):
                    user_id = str(user_id)
                    return user_id
                else:
                    return False
            elif "[id" in str(self.text.lower()) or "[club" in str(self.text.lower()):
                i = self.text.lower().split(' ')[1]
                user_id = await self.opredel_skreen(i, self.text.lower())
                if self.is_int(user_id):
                    user_id = str(user_id)
                    return user_id
                else:
                    return False
        return False

    # получение текста ачивки и количества баллов
    async def txt_achievement(self, txt):
        txt_list = txt.split(" ")
        if "[id" in str(txt.lower()) or "[club" in str(txt.lower()) or "vk.com/" in txt.lower():
            del txt_list[0]
            del txt_list[0]
            l = len(txt_list) - 1
            kol = txt_list[l]
            del txt_list[l]
            return " ".join(txt_list), kol
        else:
            del txt_list[0]
            l = len(txt_list) - 1
            kol = txt_list[l]
            del txt_list[l]
            return " ".join(txt_list), kol


    async def ls_open_check(self, fr_id):
        res = await self.apis.api_post("messages.isMessagesFromGroupAllowed", v=self.v, group_id=self.club_id,
                                       user_id=fr_id)
        if res["is_allowed"] == 1:
            return True
        else:
            return False


    # поиск по html
    def fin(self, s, first, last):
        try:
            start = s.index(str(first)) + len(str(first))
            end = s.index(str(last), start)
            return s[start:end]
        except ValueError:
            return ""

    async def info_user(self, user_id, res=0, f=0):
        if str(user_id)[0] == "-":
            return "Таких не знаем🤖"

        warn = ""
        ban = ""
        if f == 0:
            info = await self.create_mongo.user_info(user_id, self.peer_id)
            if not info:
                return "Такого не существует в природе👽"

            if "count_old" in info["warn"]:
                warn = f"☢ Варны: [{info['warn']['count']}/3]\n🤡 Количество варнов: {info['warn']['count_old'] - 1}\n\n"
            if "count" in info["ban"]:
                ban = f"🤡 Количество банов: {info['ban']['count']}\n\n"

        result = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}", name_case="gen")
        name = f'{result[0]["first_name"]} {result[0]["last_name"]}'

        if res == 0:
            res = await self.create_mongo.profile_users_add(user_id)


        awards = ""
        if len(res[0]) >= 1:
            if res[0][0] == "0":
                awards = f"💬 Количество сообщений: {res[2]}\n📊 Рейтинг: {res[1]}\n👻 Ачивки:\n📛 Ачивок нет"
            else:
                awards = f"💬 Количество сообщений: {res[2]}\n📊 Рейтинг: {res[1]}\n👻 Ачивки:\n" + "\n".join(res[0])

        # p = requests.get('https://vk.com/foaf.php?id=' + str(self.from_id))
        s = await api_url('https://vk.com/foaf.php?id=' + str(user_id)).get_html()
        l = self.fin(s, "<ya:created dc:date=", "/>\n")
        q = l[1:-7]
        q = q[:-9]
        q = q.replace('-', '.')
        q = q.split(".")
        q = str(q[2]) + "." + str(q[1]) + "." + str(q[0])
        return f"👤 Профиль [id{user_id}|{name}]\n\n📆 Дата регистрации: {q}\n\n{warn}{ban}{awards}"

    async def time_transformation(self, vrem):
        timestamp = int(vrem)
        value = datetime.fromtimestamp(timestamp)
        tim = value.strftime('%d.%m.%Y %H:%M')
        return tim

    async def info_reputation(self, user_id):
        await self.create_mongo.profile_users_add(user_id, reputation_minus=self.date, f=2)
        await self.create_mongo.profile_users_add(user_id, reputation_plus=self.date, f=2)
        result = await self.create_mongo.profile_users_check(user_id, self.date)
        plus = []
        j = 1
        for i in result["plus"]:
            res = await self.time_transformation(result["plus"][i])
            plus.append(f"{j}. +реп станет доступен после {res}")
            j += 1
        minus = []
        j = 1
        for i in result["minus"]:
            res = await self.time_transformation(result["minus"][i])
            minus.append(f"{j}. -реп станет доступен после {res}")
            j += 1
        resul = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}", name_case="gen")
        name = f'{resul[0]["first_name"]} {resul[0]["last_name"]}'
        minu = ""
        if result["count_minus"] != 0:
            minu = f"\n\n😈 Количество доступных -реп: [{result['count_minus_available']}/{result['count_minus']}]\n" \
                   + "\n".join(minus)
        msg = f"👤 Доступная репутация [id{user_id}|{name}]\n\n" \
              f"😇 Количество доступных +реп: [{result['count_plus_available']}/{result['count_plus']}]\n" \
              + "\n".join(plus) + \
              f"{minu}"
        return msg
    '''async def bind(self):
        ad = methods(self.v, self.club_id)
        adm = await ad.admin_chek(self.message)
        if adm == 1:pass'''


