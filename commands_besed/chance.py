import traceback
import random
import numpy as np
import asyncio

import command_besed
from commands import commands
from api.methods import messages_edit

class chance(commands):

    async def run(self):
        try:
            res = await self.create_mongo.profile_users_add(self.from_id)
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if res[1] > 35 or adm:
                ran = ["рандом", "бот", "к", "вашим", "услугам", "."]
                ran_1 = ["что", "здесь", "происходит", "я", "не", "знаю", "но", "зато", "это", "рандомный", "рандом"]
                ran_2 = ["рандомим", "по", "полной", "программе", "настоящий", "надеюсь", "вы", "что-то", "понимаете"]
                ran_3 = ["устал", "я", "радомить"]
                np.random.shuffle(ran)
                np.random.shuffle(ran_1)
                np.random.shuffle(ran_2)
                np.random.shuffle(ran_3)
                ran[0] = ran[0].capitalize()
                ran_1[0] = ran_1[0].capitalize()
                ran_2[0] = ran_2[0].capitalize()
                ran_3[0] = ran_3[0].capitalize()
                perv = ["Вы попали к нужному мастеру рандома, давайте зарандомим.",
                        "Вам повезло, я опытный таролог. Воспольземся картами таро.",  # Начинаю расскладывать карты таро",
                        "Начинаю расчитывать вероятность на основе сложных формул.",
                        "🔮 Давайте погадаем с помощью магического шара.",  # Снимаю покрывало с гадального шара",
                        "Кто как не ушедшие из мира сего могут нам помочь.",  # Достаю доску Уиджи"
                        "Пожалуйста подождите, совершаю запрос на госуслуги. Время ожидания 30 минут.",
                        "Ваш шанс равен 100 процентам, даже гадать не буду.",
                        "Начинаю игру в нарды на ваш шанс, ожидайте.",
                        " ".join(ran)]
                slov = {
                    perv[0]: {
                        "is_random": False,
                        "range": 2,
                        1: ["🎲 Рандомлю. Первое значение получено.", 5],
                        2: ["🎲 Рандомлю. Второе значение получено.", 5],
                        "chance": {
                            "🎰 Ваш запрос обработан и зарандомлен.": random.randint(55, 99)
                        },
                        "sms": "🎰 Ваш запрос обработан и зарандомлен."
                    },
                    perv[1]: {
                        "is_random": False,
                        "range": 3,
                        1: ["🎟 Раскладываю карты на столе.", 5],
                        2: ["👁 Очищаю все свои чакры для лучшего результата.", 5],
                        3: ["🔥💦🌪 Задаю вопрос, мысленно обращаясь ко всем стихиям и к аватару Аангу.", 5],
                        "chance": {
                            "🎯 Карты таро дали ответ на ваш вопрос. Да прибудет свами таро.": random.randint(70, 99)
                        },
                        "sms": "🎯 Карты таро дали ответ на ваш вопрос. Да прибудет свами таро."
                    },
                    perv[2]: {
                        "is_random": False,
                        "range": 4,
                        1: ["✊🏻 Гуглю сложные формулы по теории вероятности.", 5],
                        2: ["✊🏻 Гуглю калькуляторы интеграллов.", 5],
                        3: ["💪🏻 Соединяю два запроса в один.", 5],
                        4: ["👨🏻‍🎓 Делаю умное лицо.", 5],
                        "chance": {
                            "🤖 Получил ваш ответ с использованием предобученной модели машинного обучения.": random.randint(70, 99)
                        },
                        "sms": "🤖 Получил ваш ответ с использованием предобученной модели машинного обучения."
                    },
                    perv[3]: {
                        "is_random": False,
                        "range": 4,
                        1: ["🛌 Снимаю покрывало с гадального шара.", 5],
                        2: ["🌚 Подключаюсь к спутнику.", 5],
                        3: ["👽 Получаю сигнал из космоса.", 5],
                        4: ["🎥 Преобразовываю полученные данные и вывожу их на шар.", 5],
                        "chance": {
                            "📀 Данные преобразованы, магическое число получено.": random.choice([55, 66, 77, 88, 99])
                        },
                        "sms": "📀 Данные преобразованы, магическое число получено."
                    },
                    perv[4]: {
                        "is_random": False,
                        "range": 4,
                        1: ["🏄‍♂ Достаю доску Уиджи.", 5],
                        2: [f"🧟‍♂ Вызываю чьего-то {''.join(['пра' for i in range(random.randint(1, 9))])}дедушку.", 5],
                        3: [f"🧟‍♀ Прадедушка оказался буйным, вызываю чью-то {''.join(['пра' for i in range(random.randint(1, 9))])}бабушку", 5],
                        4: ["⚰ Узнаю шансы у неё.", 5],
                        "chance": {
                            "🔥 Доску спалила. Пришлось прогнать её. Успела сообщить только первую половину числа.": random.randint(1, 9),
                            "🕯 Она сообщила число. Я смог распознать его.": random.randint(55, 99)
                        },
                        "sms": random.choice(["🔥 Доску спалила. Пришлось прогнать её. Успела сообщить только первую половину числа.",
                                              "🕯 Она сообщила число. Я смог распознать его."])
                    },
                    perv[5]: {
                        "is_random": False,
                        "range": 4,
                        1: ["‼ Пожалуйста подождите. Время ожидания 29 минут 55 секунд.", 5],
                        2: [f"‼ Пожалуйста подождите. Время ожидания 29 минут 50 секунд.", 5],
                        3: [f"💚 Устали небось ждать. Открываю исходный код.", 5],
                        4: ["🔇 Ставлю 00:00 в время ожидания.", 5],
                        "chance": {
                            "🆘 Получил ошибку 404. Запучкаю рандомайзер на основе ошибки": random.choice([54, 64, 74, 84, 94]),
                            "✅ Шанс получен, сайт не упал, я счастлив.": random.randint(55, 99),
                        },
                        "sms": random.choice(
                            ["🆘 Получил ошибку 404. Запучкаю рандомайзер на основе ошибки",
                             "✅ Шанс получен, сайт не упал, я счастлив."])
                    },
                    perv[6]: {
                        "is_random": False,
                        "range": 0,
                        "chance": {
                            "💥 Ваш шанс сто процентов.": 100
                        },
                        "sms": "💥 Ваш шанс сто процентов."
                    },
                    perv[7]: {
                        "is_random": False,
                        "range": 4,
                        1: ["👨‍✈ Играю в нарды.", 5],
                        2: [f"🍖 Бросили нарды, шанс проигран, играем в шашлык.", 5],
                        3: [f"🌭 Шашлык вкусный, но сосики жаренные вуснее.", 5],
                        4: ["🍼 Кажется вы ждёте шанс, сейчас разобью бутылку и по её звуку определю число.", 5],
                        "chance": {
                            "💦 Бутылка разбилась, шанс получен, кто-то радуется.":
                                random.randint(55, 99),
                            "🌊 Бутылка оказалась сделана из ударопрочного материала, пришлось её разбивать о Титаник...":
                                random.randint(55, 99),
                        },
                        "sms": random.choice(
                            ["💦 Бутылка разбилась, шанс получен, кто-то радуется.",
                             "🌊 Бутылка оказалась сделана из ударопрочного материала, пришлось её разбивать о Титаник..."])
                    },
                    perv[8]: {
                        "is_random": False,
                        "range": 3,
                        1: ["🤖" + " ".join(ran_1), 5],
                        2: ["🤖" + " ".join(ran_2), 5],
                        3: ["🤖" + " ".join(ran_3), 5],
                        "chance": {
                            "👾 На самом делеле я гробатрон и я украл ваши шансы.":
                                0,
                            "🤖 Рандом бот устать, держите ваши шансы.":
                                random.randint(55, 99),
                        },
                        "sms": random.choice(
                            ["👾 На самом делеле я гробатрон и я украл ваши шансы.",
                             "🤖 Рандом бот устать, держите ваши шансы."])
                    },
                }
                ran = random.choice(perv)
                msg = messages_edit(self.v, self.club_id, self.apis, self.peer_id, ran)
                await msg.start_send()
                await asyncio.sleep(5)
                for i in range(1, slov[ran]["range"] + 1):
                    await msg.finish(slov[ran][i][0])
                    await asyncio.sleep(slov[ran][i][1])
                await msg.finish(f"{slov[ran]['sms']}\n\nВаш шанс: {slov[ran]['chance'][slov[ran]['sms']]}")
                await asyncio.sleep(5)
                #await msg.del_sms()

        except Exception as e:
            print(traceback.format_exc())




chances = command_besed.Command()

chances.keys = ['/шанс', '/chance']
chances.description = 'Шанс поступления'
chances.process = chance
chances.topics_blocks = []
chances.topics_resolution = ["tema1"]
