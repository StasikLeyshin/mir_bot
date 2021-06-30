# -*- coding: utf-8 -*-
import asyncio
import json
import re

from api.methods import methods
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
                user_id = self.fwd_messages["from_id"]
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



    '''async def bind(self):
        ad = methods(self.v, self.club_id)
        adm = await ad.admin_chek(self.message)
        if adm == 1:pass'''


