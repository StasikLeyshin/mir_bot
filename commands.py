# -*- coding: utf-8 -*-
import asyncio
import json
import pprint
import re
import time
from datetime import datetime
import traceback


from api.methods import methods
from api import api_url
from api.api_execute import inf_lot
from record_achievements import record_achievements
from command_ls import command_ls_dictionary, command_ls_list


class commands:

    def __init__(self, v, club_id, message, apis, them, create_mongo, collection_bots, document_tokens, url_dj,
                 client=None, tree_questions=None, mongo_manager=None, settings_info=None):

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
        self.client = client
        self.tree_questions = tree_questions
        self.mongo_manager = mongo_manager
        self.settings_info = settings_info
        self.admin_list = [15049950, 216758639, 597624554]
        #self.admin_list = [597624554, 516659275]
        #self.admin_list = [597624554, 456204202]
        self.subjects = {
            "Рус + мат(проф.) + инф": "Математика Русский Информатика и ИКТ",
            "Рус + мат(проф.) + физ": "Математика Русский Физика",
            "Рус + мат(проф.) + хим": "Математика Русский Химия",
            "Рус + мат(проф.) + общ": "Математика Русский Обществознание",
            "Рус + общ + ист": "Русский Обществознание История",
            "Рус + мат(проф.) + твор": "Математика Русский Творческий экзамен",
            "Рус + общ + твор": "Русский Обществознание Творческий экзамен"
        }

        self.subjects_opposite = {
            "Рус + мат(проф.) + инф": "math&rus&info",
            "Рус + мат(проф.) + физ": "math&rus&phys",
            "Рус + мат(проф.) + хим": "math&rus&chem",
            "Рус + мат(проф.) + общ": "math&rus&soc",
            "Рус + общ + ист": "rus&soc&hist",
            "Рус + мат(проф.) + твор": "math&rus&art",
            "Рус + общ + твор": "rus&soc&art"
        }
        self.subjects_opposite_id = {
            "Рус + мат(проф.) + инф": [1, 18, 3],
            "Рус + мат(проф.) + физ": [1, 18, 2],
            "Рус + мат(проф.) + хим": [1, 18, 7],
            "Рус + мат(проф.) + общ": [1, 18, 4],
            "Рус + мат(проф.) + гео": [1, 18, 19],
            "Рус + инф + гео": [1, 3, 19],
            "Рус + общ + ист": [1, 4, 5],
            "Рус + мат(проф.) + твор": [1, 6],
            "Рус + общ + твор": [1, 4, 6]

        }

        self.sms_awards = {
            100: ["Ууф, сотка сообщений, у нас любитель початиться", 2],
            1000: ["Ого, тысяча сообщений, еще не флудер года, но всё впереди", 6],
            2000: ["That's a lot of masseges! How abount a little more? Две тысячи сообщений пройдено!", 9],
            5000: ["ГЛАВНЫЙ ФЛУДЕР ГОДА НАЙДЕН! ПЯТЬ ТЫСЯЧ СООБЩЕНИЙ ЕСТЬ!", 12],
            10000: ["ДЕСЯТЬ ТЫСЯЧ СООБЩЕНИЙ!!! ДЕСЯЯЯЯЯТЬ! НАСПАМИЛ НА БЕЗБЕДНУЮ ЖИЗНЬ", 15],
            20000: ["ТЫ ЧЕВО ДЕЛАЕШЬ, ТЫ ЧТО, БОГАТЫРЬ ЧТО ЛИ, КУДА СТОЛЬКО, КУДА??????", 20],
            30000: ["ТЫ ЧЕГО ТУТ ДЕЛАЕШЬ? выйди траву потрогай, в злах сходи, жену погладь, сколько можно в чате сидеть.", 40],
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
            10: ["🎲 Любимчик Фортуны", 7.777]
        }

        self.direction_id = {
                                "IT и анализ данных": 1,
                                "Информационная/компьютерная безопасность": 2,
                                "Химия и биотехнология": 3,
                                "Радиоэлектроника": 4,
                                "Робототехника и автоматизация": 5,
                                "Экономика и управление": 6,
                                "Дизайн": 7,
                                "Юриспруденция": 8
        }
        self.strategic_directions_id = {
            "IT и анализ данных": 1,
            "Химия и биотехнология": 2,
            "Информационная/компьютерная безопасность": 3,
            "Радиоэлектроника": 4,
            "Робототехника и автоматизация": 5,
            "Экономика и управление": 6,
            "Дизайн": 7,
            "Юриспруденция": 8

        }

        self.event_id = {
            "Мастер-классы": 1,
            "Лекции": 2,
            "Экскурсии": 3,
            "Интеллектуальные игры": 6,
            "Университетские субботы": 7,
            "Презентации Институтов и направлений": 14,
            "День открытых дверей": 15,
            "Олимпиады": 16

        }

        self.choice_focus_open_day_id = {'Все программы': ['https://priem.mirea.ru/lk/api/events/get/295',
                                                           'https://priem.mirea.ru/lk/api/events/get/296',
                                                           'https://priem.mirea.ru/lk/api/events/get/303',
                                                           'https://priem.mirea.ru/lk/api/events/get/304',
                                                           'https://priem.mirea.ru/lk/api/events/get/306'
                                                           ],
                                         'IT и анализ данных': ['https://priem.mirea.ru/lk/api/events/get/298',
                                                                'https://priem.mirea.ru/lk/api/events/get/299',
                                                                'https://priem.mirea.ru/lk/api/events/get/302'
                                                                ],
                                         'Безопасность и приборостроение': ['https://priem.mirea.ru/lk/api/events/get/299'],
                                         'Кибернетика, робототехника': ['https://priem.mirea.ru/lk/api/events/get/299'],
                                         'Экономика и управление': ['https://priem.mirea.ru/lk/api/events/get/301'],
                                         'Юриспруденция': ['https://priem.mirea.ru/lk/api/events/get/299',
                                                           'https://priem.mirea.ru/lk/api/events/get/301'],
                                         'Химия и биотехнологии': ['https://priem.mirea.ru/lk/api/events/get/300',
                                                                   'https://priem.mirea.ru/lk/api/events/get/302'],
                                         'Радиоэлектроника': ['https://priem.mirea.ru/lk/api/events/get/302'],
                                         'Дизайн': ['https://priem.mirea.ru/lk/api/events/get/302'],
                                         'Колледж': ['https://priem.mirea.ru/lk/api/events/get/297',
                                                     'https://priem.mirea.ru/lk/api/events/get/305']
                                         }
        self.place = {'москва': '1', 'ставрополь': '2', 'фрязино': '3'}

        self.level = {'бакалавриат/специалитет': '1', 'магистратура': '3', 'аспирантура': '4'}

    def button_vk(self, label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    def menu_mirea(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                #[self.button_vk(label="Вопросы", color="positive"), self.button_vk(label="Направления", color="positive")],
                #[self.button_vk(label="Конкурс", color="primary")],
                #[self.button_vk(label="Команды", color="negative")]
                [self.button_vk(label="Частые вопросы", color="positive"),],
                [self.button_vk(label="Меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard


    def pusto(self):
        keyboard = {"buttons": [], "one_time": True}
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def menu(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                #[self.button_vk(label="Вопросы", color="positive"), self.button_vk(label="Направления", color="positive")],
                #[self.button_vk(label="Конкурс", color="primary")],
                #[self.button_vk(label="Команды", color="negative")]
                # [self.button_vk(label="Частые вопросы", color="positive"),
                #  self.button_vk(label="Подобрать направление", color="positive")],
                # [self.button_vk(label="Подобрать мероприятие", color="primary")],
                # [self.button_vk(label="Дни открытых дверей", color="primary")],
                # [self.button_vk(label="пройти опрос о мероприятиях", color="primary")],

                [self.button_vk(label="Помощь по приёму", color="positive")],
                 #self.button_vk(label="Калькулятор баллов", color="positive")],
                [self.button_vk(label="Подбор направлений", color="primary")],
                #[self.button_vk(label="Дни открытых дверей", color="primary")],
                [self.button_vk(label="Репорт", color="secondary")],
                [self.button_vk(label="Меню", color="negative")]
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

    def level_education_q(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Поступаю в бакалавриат/специалитет", color="positive")],
                 [self.button_vk(label="Поступаю в магистратуру", color="positive")],
                 [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_status(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Хочу поступать в вуз", color="positive")],
                 [self.button_vk(label="Хочу поступать в колледж", color="positive")],
                 [self.button_vk(label="Уже учусь в вузе/колледже", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def menu_incomplete(self, inline=False):
        keyboard = {
            "one_time": False,
            "inline": inline,
            "buttons": [
                 [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def menu_naked_survey(self, txt, inline=False):
        survey = [self.button_vk(label=f"{i}", color="positive") for i in txt]
        sp = [survey] + [[self.button_vk(label="Шаг назад", color="secondary")]] + [[self.button_vk(label="Меню", color="negative")]]
        keyboard = {
            "one_time": False,
            "inline": inline,
            "buttons": sp
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_where_level(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Бакалавриат/специалитет", color="positive")],
                [self.button_vk(label="Магистратура", color="positive")],
                [self.button_vk(label="Аспирантура", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_where_study(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Москва", color="positive")],
                [self.button_vk(label="Фрязино", color="positive")],
                [self.button_vk(label="Ставрополь", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_choose_direction(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Подобрать по интересам", color="positive")],
                 [self.button_vk(label="Подобрать по экзаменам", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_select_interests(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="IT и анализ данных", color="positive")],
                [self.button_vk(label="Химия и биотехнология", color="positive")],
                [self.button_vk(label="Информационная/компьютерная безопасность", color="positive")],
                [self.button_vk(label="Радиоэлектроника", color="positive")],
                [self.button_vk(label="Робототехника и автоматизация", color="positive")],
                [self.button_vk(label="Экономика и управление", color="positive")],
                [self.button_vk(label="Дизайн", color="positive")],
                [self.button_vk(label="Юриспруденция", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_type_event(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Лекции", color="positive")],
                [self.button_vk(label="Мастер-классы", color="positive")],
                [self.button_vk(label="Экскурсии", color="positive")],
                [self.button_vk(label="Интеллектуальные игры", color="positive")],
                [self.button_vk(label="Университетские субботы", color="positive")],
                [self.button_vk(label="Презентации Институтов и направлений", color="positive")],
                [self.button_vk(label="Дни открытых дверей", color="positive")],
                [self.button_vk(label="Олимпиады", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_interest_event(self, txt):
        keyboard = {
            "one_time": False,
            "inline": True,
            "buttons": [
                [self.button_vk(label="Показать ещё", color="positive", payload=txt)]
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
                [self.button_vk(label="Рус + мат(проф.) + инф", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + физ", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + общ", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + хим", color=r)],
                [self.button_vk(label="Рус + общ + ист", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + гео", color=r)],
                [self.button_vk(label="Рус + инф + гео", color=r)],
                [self.button_vk(label="Рус + мат(проф.) + твор", color=r)],
                [self.button_vk(label="Рус + общ + твор", color=r)],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_choose_event(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Подобрать по интересам", color="positive")],
                [self.button_vk(label="Онлайн мероприятия", color="positive")],
                [self.button_vk(label="Очные мероприятия", color="positive")],
                [self.button_vk(label="По виду мероприятия", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_open_day(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Хочу посмотреть все", color="positive")],
                [self.button_vk(label="Хочу выбрать направленность", color="positive")],
                [self.button_vk(label="Только онлайн", color="positive")],
                [self.button_vk(label="Только очные", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def level_focus_open_day(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="IT и анализ данных", color="positive")],
                [self.button_vk(label="Безопасность и приборостроение", color="positive")],
                [self.button_vk(label="Кибернетика, робототехника", color="positive")],
                [self.button_vk(label="Экономика и управление", color="positive")],
                [self.button_vk(label="Юриспруденция", color="positive")],
                [self.button_vk(label="Химия и биотехнологии", color="positive")],
                [self.button_vk(label="Радиоэлектроника", color="positive")],
                [self.button_vk(label="Дизайн", color="positive")],
                #[self.button_vk(label="Колледж", color="positive")],
                [self.button_vk(label="Шаг назад", color="secondary")],
                [self.button_vk(label="Вернуться в меню", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def generations_keyboard(self, list_k):

        list_n = []
        for i in list_k:
            if "шаг назад" not in i[1].lower():
                txt = i[1]
                if len(i[1]) > 40:
                    txt = str(i[1][:37]) + "..."
                list_n.append([self.button_vk(label=txt, color="positive")])
        list_n.append([self.button_vk(label="Шаг назад", color="secondary")])

        keyboard = {
            "one_time": False,
            "buttons": list_n
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def generations_keyboard_unban(self, list_k):

        list_n = []
        for i in list_k:
            if "шаг назад" not in i.lower():
                list_n.append([self.button_vk(label=i, color="positive")])
        list_n.append([self.button_vk(label="Шаг назад", color="secondary")])

        keyboard = {
            "one_time": False,
            "buttons": list_n
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def keyboard_warn(self, tex):
        r = "primary"
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Заварнить", color="positive", payload=tex+"@wr"),
                 self.button_vk(label="БАН", color="positive", payload=tex+"@bn")],
                [self.button_vk(label="Глобальный бан", color="negative", payload=tex+"@gl")]
            ],
            "inline": True
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def keyboard_unban(self, tex):
        r = "primary"
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Разбанить", color="positive", payload=tex+"@unban")],
                [self.button_vk(label="Не разбанить", color="negative", payload=tex+"@ban")]
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

    def competition(self, f):
        if f == 0:
            spis = [
                [self.button_vk(label="Добавить СНИЛС/уникальный номер", color="positive")],
                [self.button_vk(label="Посмотреть анонимно", color="positive")],
                [self.button_vk(label="Команды", color="negative")]
            ]
        elif f == 1:
            spis = [
                [self.button_vk(label="Моя ситуация", color="positive")],
                [self.button_vk(label="Посмотреть анонимно", color="positive")],
                [self.button_vk(label="Изменить СНИЛС/уникальный номер", color="positive")],
                [self.button_vk(label="Команды", color="negative")]
            ]
        keyboard = {
            "one_time": False,
            "buttons": spis
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
        return False

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
            return ''
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
                opt = re.sub(r'^\w\s', '', self.text.lower())
                text_list = opt.split(' ')
                user_id = None
                for i in text_list:
                    if "[id" in i or "[club" in i:
                        user_id = await self.opredel_skreen(i, self.text.lower())
                        if not user_id:
                            break
                #user_id = await self.opredel_skreen(i, self.text.lower())
                if self.is_int(user_id):
                    user_id = str(user_id)
                    return user_id
                else:
                    return False
        return False


    async def getting_number(self):
        try:
            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', self.text.lower())]
            for i in s:
                if i < 20:
                    return i
            return 1
        except:
            return 1

    async def getting_user_id_fwd(self):
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

    async def txt_roulette(self, txt):
        txt_list = txt.split(" ")
        if len(txt_list) > 1:
            #del txt_list[0]
            kol = txt_list[1]
            return kol
        else:
            kol = False
            return kol


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
        # s = await api_url('https://vk.com/foaf.php?id=' + str(user_id)).get_html()
        # l = self.fin(s, "<ya:created dc:date=", "/>\n")
        # q = l[1:-7]
        # q = q[:-9]
        # q = q.replace('-', '.')
        # q = q.split(".")
        # q = str(q[2]) + "." + str(q[1]) + "." + str(q[0])
        #return f"👤 Профиль [id{user_id}|{name}]\n\n📆 Дата регистрации: {q}\n\n{warn}{ban}{awards}"
        return f"👤 Профиль [id{user_id}|{name}]\n\n{warn}{ban}{awards}"

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

    async def info_rating(self, size):
        result = await self.create_mongo.rating_check()
        li = sorted(result, key=result.get, reverse=True)
        #li = list(li)
        li = li[:size]
        st = ",".join(li)
        spis = []
        resul = await self.apis.api_post("execute", code=inf_lot(from_ids=st), v=self.v)
        k = 1
        resul = list(reversed(resul))

        for i, j in zip(li, resul):
            nag = "🏐"
            if k == 1:
                nag = "🥇"
            elif k == 2:
                nag = "🥈"
            elif k == 3:
                nag = "🥉"
            elif k == 4:
                nag = "🎖"
            spis.append(f"{nag} {k}. [id{i}|{j}] ——— {result[str(i)]}")
            k += 1
        msg = "👑 ТОП 25 в рейтинге:\n\n" + "\n".join(spis)
        return msg

    '''async def bind(self):
        ad = methods(self.v, self.club_id)
        adm = await ad.admin_chek(self.message)
        if adm == 1:pass'''

    async def snils_check(self, snils="0", flag=0):
        try:
            if not self.is_int(snils.replace("-", "")):
                return 0, [["Введите СНИЛС/уникальный номер в правильном формате"]]

            res = await self.create_mongo.users_directions_add_finish(self.from_id, self.text, flag=flag)
            if res[0] == 1:
                return 0, [["Не удалось найти данные по СНИЛСУ/уникальному номеру, повторите попытку."]]
            elif res[0] == 2:

                return 0, [["Вы не привязали СНИЛС/уникальный номер."]]
            directions_list = []
            ll = 1
            vash_new = "Ваша позиция"
            if flag == 2:
                vash_new = "Позиция"
            bal = 0

            dat = ""
            vash = "Ваш "
            vash_new_new = "ваших "
            if flag == 0:
                dat = "Данные записаны\n"
            elif flag == 2:
                vash = ""
                vash_new_new = ""


            for i in range(1, res[1]["count"] + 1):
                comment = ""
                if len(res[1][str(i)]['note']) > 0:
                    comment = f"\nКомментарий: {res[1][str(i)]['note']}"
                if int(res[1][str(i)]['total_amount']) > bal:
                    bal = int(res[1][str(i)]['total_amount'])
                directions_list.append(f"{ll}. {res[2][res[1][str(i)]['code_directions']]['title']}\n"
                                       f"🐈 Код: {res[2][res[1][str(i)]['code_directions']]['code']}\n"
                                       f"👥 Количество бюджетных мест: {res[2][res[1][str(i)]['code_directions']]['plan']}\n"
                                       f"🌏 {vash_new}: {res[1][str(i)]['position']}\n"
                                       f"🌐 {vash_new} с учётом подачи согласия к зачислению: {res[1][str(i)]['position_consent']}\n"
                                       f"👨‍⚖ Согласие к зачислению: {res[1][str(i)]['consent']}\n"
                                       f"👤 Ссылка на список поступающих: "
                                       f"https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition="
                                       f"{res[1][str(i)]['code_directions']}&highlight={res[1][str(i)]['user_id']}"
                                       f"{comment}")
                ll += 1
            msg = f"{dat}⏰ {res[3]}\n💎 {vash}СНИЛС/уникальный номер: {res[1]['snils']}\n" \
                  f"💿 Сумма баллов с учётом ИД: {bal}\n" \
                  f"📝 Список {vash_new_new}направлений:\n\n"
            directions_list.insert(0, msg)
            de = self.chunks(directions_list, 5)
            l = list(de)
            # dat = ""
            # vash = "Ваш "
            # vash_new_new = "ваших "
            # if flag == 0:
            #     dat = "Данные записаны\n"
            # elif flag == 2:
            #     vash = ""
            #     vash_new_new = ""
            # msg = f"{dat}⏰ {res[3]}\n💎 {vash}СНИЛС/уникальный номер: {res[1]['snils']}\n" \
            #       f"💿 Сумма баллов с учётом ИД: {bal}\n" \
            #       f"📝 Список {vash_new_new}направлений:\n\n"\
            #       +"\n\n".join(directions_list)
            self.create_mongo.add_user(self.peer_id, 0)

            return 1, l
        except Exception as e:
            print(traceback.format_exc())



    async def ban_rating(self, user_id, from_id, bal, peer_id, cause, vrem):
        if bal <= -50:
            res_new = await self.create_mongo.globan_add(user_id, vrem, from_id, "Рейтинг достиг отметки ниже -50")
            if res_new[0] == 1:
                msg = f"Данный [id{user_id}|пользователь] добавлен в глобальный бан.\n\n" \
                      f"📝 Причина: Рейтинг достиг отметки ниже -50.\n\n" \
                      f"P.S. Оттуда ещё никто не возвращался..."
                return True, msg, res_new[1]
            elif res_new[0] == 2:
                msg = f"Данный [id{user_id}|пользователь] уже есть в глобальном бане.\n\n" \
                      f"P.S. И он оттуда скорее всего не вернётся..."
                return True, msg, res_new[1]

        elif bal <= -30:
            timestamp = 604800 + int(vrem)
            value = datetime.fromtimestamp(timestamp)
            time = value.strftime('%d.%m.%Y %H:%M')
            res_ban = await self.create_mongo.ban_check(user_id, peer_id, cause, 604800 + vrem, vrem, from_id)
            res = await record_achievements(self.create_mongo, user_id).run(kol_ban=res_ban)
            msg_n = ""
            if res[1]:
                msg_n = "\n\n👻 Полученные ачивки:\n" + "\n".join(res[1])
            ply = await self.display_time(604800)
            result = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}", name_case="gen")
            name = f'{result[0]["first_name"]} {result[0]["last_name"]}'
            msg = f"{name}, вам бан на {ply}\n📝 Причина: Рейтинг достиг отметки ниже -30\n⏰ Время окончания: {time}\n\n" \
                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.{msg_n}\n\n📊 Рейтинг: {bal}"
            return True, msg

        return False

    async def get_event_interest(self, event_id=None, count=10, offset=0):
        res = await api_url("https://priem.mirea.ru/lk/api/events/get").get_json()
        msg = []
        kk = 0
        flag = False
        if event_id:
            txt = event_id
        else:
            txt = self.direction_id[self.text]
        for i in res:
            if i["event_direction_id"] and i["event_direction_id"] != "null":
                if i["event_direction_id"] == int(txt):
                    if kk == count + offset:
                        kk += 1
                        break
                    kk += 1
                    if kk <= offset:
                        continue
                    address = ""
                    if i["is_online"] != 1:
                        address = f"🌍 Адрес: {i['address']}\n"
                        format_event = "🏤 Формат: Очно"
                    else:
                        format_event = "🏡 Формат: Дистанционно"
                    msg.append(f"🔮 {i['title']}\n⌚ Когда: {i['date_readable']} в {i['time_readable']}\n{format_event}\n"
                               f"{address}"
                               f"💡 О мероприятии: https://priem.mirea.ru/event?event_id={i['id']}")
        if kk - offset == 11:
            flag = True
        if not msg:
            msg = ["😪 Увы, пока мероприятий по этому запросу не планируется, но мы постараемся провести что-нибудь позднее.\n\n"
                   "Следи за обновлениями в календаре:\nhttps://priem.mirea.ru/events/"]
        return msg, flag, f"direction&{txt}"

    async def get_event_online_offline(self, count=10, offset=0, is_online=False):
        res = await api_url("https://priem.mirea.ru/lk/api/events/get").get_json()
        msg = []
        kk = 0
        flag = False
        sr = 0
        if is_online:
            sr = 1
        for i in res:
            if i["event_direction_id"] and i["event_direction_id"] != "null":
                if i["is_online"] == sr:
                    if kk == count + offset:
                        kk += 1
                        break
                    kk += 1
                    if kk <= offset:
                        continue
                    address = ""
                    if i["is_online"] != 1:
                        address = f"🌍 Адрес: {i['address']}\n"
                        format_event = "🏤 Формат: Очно"
                    else:
                        format_event = "🏡 Формат: Дистанционно"
                    msg.append(
                        f"🔮 {i['title']}\n⌚ Когда: {i['date_readable']} в {i['time_readable']}\n{format_event}\n"
                        f"{address}"
                        f"💡 О мероприятии: https://priem.mirea.ru/event?event_id={i['id']}")
        if kk - offset == 11:
            flag = True
        if not msg:
            msg = ["😪 Увы, пока мероприятий по этому запросу не планируется, но мы постараемся провести что-нибудь позднее.\n\n"
                   "Следи за обновлениями в календаре:\nhttps://priem.mirea.ru/events/"]
        return msg, flag, f"online&{sr}"

    async def get_open_day_online_offline(self, event_id=15, count=10, offset=0, is_online=False):
        res = await api_url("https://priem.mirea.ru/lk/api/events/get").get_json()
        msg = []
        kk = 0
        flag = False
        sr = 0
        if is_online:
            sr = 1
        if event_id:
            txt = event_id
        else:
            txt = self.event_id[self.text]
        for i in res:
            if i["type"]["id"] == int(txt) and i["is_online"] == sr:
                if kk == count + offset:
                    kk += 1
                    break
                kk += 1
                if kk <= offset:
                    continue
                address = ""
                if i["is_online"] != 1:
                    address = f"🌍 Адрес: {i['address']}\n"
                    format_event = "🏤 Формат: Очно"
                else:
                    format_event = "🏡 Формат: Дистанционно"
                msg.append(
                    f"🔮 {i['title']}\n⌚ Когда: {i['date_readable']} в {i['time_readable']}\n{format_event}\n"
                    f"{address}"
                    f"💡 О мероприятии: https://priem.mirea.ru/event?event_id={i['id']}")
        if kk - offset == 11:
            flag = True
        if not msg:
            msg = ["😪 Увы, пока мероприятий по этому запросу не планируется, но мы постараемся провести что-нибудь позднее.\n\n"
                   "Следи за обновлениями в календаре:\nhttps://priem.mirea.ru/events/"]
        return msg, flag, f"open_day_online&{sr}"

    async def get_event_type(self, event_id=None, count=10, offset=0):
        res = await api_url("https://priem.mirea.ru/lk/api/events/get").get_json()
        msg = []
        kk = 0
        flag = False
        if event_id:
            txt = event_id
        else:
            txt = self.event_id[self.text]
        for i in res:
            if i["type"]["id"] == int(txt):
                if kk == count + offset:
                    kk += 1
                    break
                kk += 1
                if kk <= offset:
                    continue
                address = ""
                if i["is_online"] != 1:
                    address = f"🌍 Адрес: {i['address']}\n"
                    format_event = "🏤 Формат: Очно"
                else:
                    format_event = "🏡 Формат: Дистанционно"
                msg.append(
                    f"🔮 {i['title']}\n⌚ Когда: {i['date_readable']} в {i['time_readable']}\n{format_event}\n"
                    f"{address}"
                    f"💡 О мероприятии: https://priem.mirea.ru/event?event_id={i['id']}")
        if kk - offset == 11:
            flag = True
        if not msg:
            msg = [
                "😪 Увы, пока мероприятий по этому запросу не планируется, но мы постараемся провести что-нибудь позднее.\n\n"
                "Следи за обновлениями в календаре:\nhttps://priem.mirea.ru/events/"]
        return msg, flag, f"event&{txt}"

    async def get_choice_focus_open_day(self):
        txt = self.choice_focus_open_day_id.get(self.text)
        msg = []
        if txt:
            msg = []
            for j in txt:
                res = await api_url(f"{j}").get_json()
                address = ""
                if res["is_online"] != 1:
                    address = f"🌍 Адрес: {res['address']}\n"
                    format_event = "🏤 Формат: Очно"
                else:
                    format_event = "🏡 Формат: Дистанционно"
                msg.append(
                    f"🔮 {res['title']}\n⌚ Когда: {res['date_readable']} в {res['time_readable']}\n{format_event}\n"
                    f"{address}"
                    f"💡 О мероприятии: https://priem.mirea.ru/event?event_id={res['id']}")
        if not msg:
            msg = [
                "😪 Увы, пока мероприятий по этому запросу не планируется, но мы постараемся провести что-нибудь позднее.\n\n"
                "Следи за обновлениями в календаре:\nhttps://priem.mirea.ru/events/"]
        return msg, False, f"event&{txt}"

    async def strategic_directions(self, place=None, strategic_id=None, level=None, count=10, offset=0):
        res = await api_url("https://priem.mirea.ru/lk/api/directions/get").get_json()
        msg = []
        kk = 0
        flag = False
        if strategic_id:
            txt = strategic_id
        else:
            txt = self.strategic_directions_id[self.text]
        for i in res:
            if i["strategic_direction_id"] == int(txt) and str(i['location_id']) == str(place) and str(i['education_level_id']) == str(level):
                if kk == count + offset:
                    kk += 1
                    break
                kk += 1
                if kk <= offset:
                    continue
                    #de = self.chunks(spis, 10)
                    #l = list(de)
                    # print(len(l))
                    # print(l)

                    #ff = 1
                perv = "🔎 Высокие шансы поступления:\n\n"
                #if pol_sql["quantity"] == -1:
                    #perv = "🔎 Гарантированное поступление на платное обучение, но на бюджет в прошлом году баллы были выше.\n\n"
                f = 1
                msg.append(
                           f"🔮 {i['program']} {i['code']}\n"
                           f"📊 Прошлогодний проходной балл на бюджет: {i['last_year_threshold']}\n"
                           f"👥 Количество бюджетных мест: {i['places_budget']}\n"
                           f"Ссылка на более подробную информацию: https://priem.mirea.ru/guide-direction?direction_id={i['id']}")
        if kk - offset == 11:
            flag = True
        if not msg:
            msg = ["😪 К сожалению таких направлений не существует."]
            return msg, False, f"strategic&{txt}&{place}&{level}"
        return msg, flag, f"strategic&{txt}&{place}&{level}"


    async def strategic_directions_exam(self, exam=None, place=None, level=None, count=10, offset=0):
        res = await api_url("https://priem.mirea.ru/lk/api/directions/get").get_json()
        msg = []
        kk = 0
        flag = False
        if exam:
            txt = [int(i) for i in exam.strip('[]').replace(' ', '').split(',')]
        else:
            txt = self.subjects_opposite_id[self.text]
        for i in res:
            if str(i['location_id']) == str(place) and str(i['education_level_id']) == str(level):
                ss = []
                for j in i["guide_exams"]:
                    ss.append(j["id"])
                if all(x in ss for x in txt):
                #if sorted(ss) == sorted(txt):

                    if kk == count + offset:
                        kk += 1
                        break
                    kk += 1
                    if kk <= offset:
                        continue
                        #de = self.chunks(spis, 10)
                        #l = list(de)
                        # print(len(l))
                        # print(l)

                        #ff = 1
                    perv = "🔎 Высокие шансы поступления:\n\n"
                    #if pol_sql["quantity"] == -1:
                        #perv = "🔎 Гарантированное поступление на платное обучение, но на бюджет в прошлом году баллы были выше.\n\n"
                    f = 1
                    msg.append(
                               f"🔮 {i['program']} {i['code']}\n"
                               f"📊 Прошлогодний проходной балл на бюджет: {i['last_year_threshold']}\n"
                               f"👥 Количество бюджетных мест: {i['places_budget']}\n"
                               f"Ссылка на более подробную информацию: https://priem.mirea.ru/guide-direction?direction_id={i['id']}")
        if kk - offset == 11:
            flag = True
        if not msg:
            msg = ["😪 К сожалению таких направлений не существует."]
            return msg, False, f"strategic_exam&{txt}&{place}&{level}"
        return msg, flag, f"strategic_exam&{txt}&{place}&{level}"


    async def step_back_bool(self):
        res = await self.create_mongo.get_users_ls_status(self.from_id)
        if res:
            if res in command_ls_dictionary:
                #print(command_ls_dictionary[f"{res}"][1].parent)
                if command_ls_dictionary[f"{res}"][1].parent:
                    await self.create_mongo.add_users_ls_status(self.from_id,
                                                                command_ls_dictionary[f"{res}"][1].parent.name)
                    return True
        return False

    async def step_back_bool_new(self, res=None, work_ls=None):
        #res = await self.create_mongo.get_users_ls_status(self.from_id)
        if res.location_tree:
            if res.location_tree in command_ls_dictionary:
                #print(command_ls_dictionary[f"{res}"][1].parent)
                if command_ls_dictionary[f"{res.location_tree}"][1].parent:
                    await work_ls.location_tree_update()
                    # await self.create_mongo.add_users_ls_status(self.from_id,
                    #                                             command_ls_dictionary[f"{res}"][1].parent.name)
                    return True
        return False


if __name__ == "__main__":


    from api import api
    # ss = {}
    # kol = 0
    # bs_list = [2000000027, 2000000036, 2000000028, 2000000029, 2000000035, 2000000037, 2000000032, 2000000033, 2000000031, 2000000030]
    # for l in bs_list:
    #     loop = asyncio.get_event_loop()
    #     s = loop.run_until_complete(api(0,
    #                                     '377cd52004220eafa956bbdbaabe9383a53820c1fa2b53cc4e14490eefa66c179d1edf2a0cb6c467fab6f').api_post(
    #         'messages.search', q='', peer_id=l, v='5.131', count=100))
    #     #pprint.pprint(s)
    #     k = 0
    #     for j in range(0, s['count'], 100):
    #         s = loop.run_until_complete(api(0,
    #                                         '377cd52004220eafa956bbdbaabe9383a53820c1fa2b53cc4e14490eefa66c179d1edf2a0cb6c467fab6f').api_post(
    #             'messages.search', q='', peer_id=l, v='5.131', count=100, offset=j))
    #         #pprint.pprint(s)
    #         for i in s['items']:
    #             if i['from_id'] == -5411326:
    #                 if i['text'] > 100:
    #                     k += 1
    #             #print(i['text'])
    #             #if 'хорошего' in i['text']:
    #                 #k += 1
    #     ss[l] = k
    #     kol += k
    # #print(k)
    # print(ss, kol)

    ss = {}
    kol = 0
    kol_all = 0
    bs_list = [2000000027, 2000000036, 2000000028, 2000000029, 2000000035, 2000000037, 2000000032, 2000000033,
               2000000031, 2000000030]

    for l in range(2000000055, 20000000100):
        loop = asyncio.get_event_loop()
        s = loop.run_until_complete(api(0,
                                        '918157cf8a3d1e91cf0d17e3f04cebacecb2b513093798b2e73d2f97c6ac978cf4d1ec456c551db5ef9b8').api_post(
            "messages.send", v='5.131', peer_id=l,
                                         message="начнём", random_id=0))
    # for l in bs_list:
    #     loop = asyncio.get_event_loop()
    #     s = loop.run_until_complete(api(0,
    #                                     '377cd52004220eafa956bbdbaabe9383a53820c1fa2b53cc4e14490eefa66c179d1edf2a0cb6c467fab6f').api_post(
    #         'messages.getHistory', peer_id=l, v='5.131', count=200))
    #     #pprint.pprint(s)
    #     #break
    #     k = 0
    #     j = 0
    #     #while len(s) != 0:
    #     kol_all += s['count']
    #     for j in range(0, s['count'], 200):
    #         s = loop.run_until_complete(api(0,
    #                                         '377cd52004220eafa956bbdbaabe9383a53820c1fa2b53cc4e14490eefa66c179d1edf2a0cb6c467fab6f').api_post(
    #             'messages.getHistory', peer_id=l, v='5.131', count=200, offset=j))
    #         # pprint.pprint(s)
    #         for i in s['items']:
    #             #print(i['from_id'])
    #             if i['from_id'] == -5411326:
    #                 if len(i['text']) > 100:
    #                     k += 1
    #             # print(i['text'])
    #             # if 'хорошего' in i['text']:
    #             # k += 1
    #         time.sleep(0.1)
    #
    #     ss[l] = k
    #     kol += k
    #     print(kol_all)
    #     print(ss, kol)
    # print(kol_all)
    # print(ss, kol)



    #text = {}
    #print(text[1:])
    # поиск по html
    # def fin(s, first, last):
    #     try:
    #         start = s.index(str(first)) + len(str(first))
    #         end = s.index(str(last), start)
    #         return s[start:end]
    #     except ValueError:
    #         return ""
    # import requests
    # #s = requests.get('https://vk.com/foaf.php?id=' + str(260671468))
    # #s = s.
    # loop = asyncio.get_event_loop()
    # s = loop.run_until_complete(api_url('https://vk.com/foaf.php?id=' + str(354930228)).get_html())
    # l = fin(s, "<ya:created dc:date=", "/>\n")
    # q = l[1:-7]
    # q = q[:-9]
    # q = q.replace('-', '.')
    # q = q.split(".")
    # q = str(q[2]) + "." + str(q[1]) + "." + str(q[0])
    # print(q)




    # def getting_number(text):
    #     try:
    #         s = [int(s) for s in re.findall(r'-?\d+\.?\d*', text.lower())]
    #         return s[0]
    #     except:
    #         return 1
    #
    #
    # print(getting_number("Осуждаю"))


    # import re
    #
    # sentence = "+rep 2"
    # #d = re.findall('\d', '25BNKLOPY5T')
    # s = [int(s) for s in re.findall(r'-?\d+\.?\d*', sentence)]
    # print(s)
    # def opredel_skreen(g, text):
    #     if "vk.com/" in str(text):
    #         r = re.findall(r'/\w+.\w+', g)
    #         t = r[-1]
    #         t = t[1:]
    #         return t
    #
    #     elif "[id" in str(text) or "[club" in str(text):
    #         l = g.find('|')
    #         l2 = g.find('id')
    #         k = g[:l]
    #         k2 = k[l2 + 2:]
    #         k = k[1:]
    #         k = k.replace("club", "")
    #         k = k.replace("id", "")
    #         if "[club" in str(text):
    #             k = "-" + str(k)
    #     return k
    #
    #
    # def getting_user_id(text):
    #     if "[id" in str(text.lower()) or "[club" in str(text.lower()):
    #         opt = re.sub(r'^\w\s', '', text.lower())
    #         text_list = opt.split(' ')
    #         user_id = None
    #         for i in text_list:
    #             #print(i)
    #             if "[id" in i or "[club" in i:
    #                 user_id = opredel_skreen(i, text.lower())
    #                 print(user_id)
    #                 if not user_id:
    #                     break
    #         # user_id = await self.opredel_skreen(i, self.text.lower())
    #         # if self.is_int(user_id):
    #         #     user_id = str(user_id)
    #         #     return user_id
    #         # else:
    #         #     return False
    #         return user_id
    #     return False

    #print(getting_user_id("+реп [id24434334|batteb])"))