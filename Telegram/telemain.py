import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButton
# import asyncio
# import configparser
# from pymongo import MongoClient
# from mongodb import create_mongodb
# from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
# #import keyboards as kb


from Telegram.bot_setting import bot
from Telegram.user import users
from sql import pol_js
from generating_questions import questions

# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
#
#
# from log.log import logger
#
# #from config import TOKEN
#
# from Telegram.bot_setting import dp, bot
#
#
# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     await message.reply("Привет!\nНапиши мне что-нибудь!")
#
#
# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")
#
#
# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)
#
#
# #if __name__ == '__main__':
# async def test1():
#     executor.start_polling(dp)



# bot = telebot.TeleBot('1768876438:AAG_nv70s_eTKJfqccJS7NOQ0zPKJNvCQRE')

# def ctf_get():
#     config = configparser.ConfigParser()
#     config.read("settings.ini")
#     return config
#
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     print(message.chat.type)
#     if message.chat.type == "private":
#         bot.reply_to(message, "Howdy, how are you doing?")
#     elif message.chat.type == "supergroup" or message.chat.type == "group":
#         bot.reply_to(message, "supergroup")

def generating_q(file):
    f2 = open(f"{file}.txt", "r+", encoding="cp1251")
    s = f2.readlines()
    f2.seek(0)
    f2.close()
    #vopr = {"nom": {}, "vopr": {}, "spis_nom": [], "spis_vop": []}
    for i in s:
        pas = i[i.find(":") + 1:]
        logi = i[:i.find(":")]
        nom = pas[pas.find(":") + 1:].replace("\\v", "\n")
        questions["nom"][logi] = nom
        questions["vopr"][logi] = pas[:pas.find(":")]
        questions["spis_nom"].append(str(logi))
        questions["spis_vop"].append(f"{logi}. {pas[:pas.find(':')]}")

def add_users(message_id, user_id, chat_id, subjects="", bal=0, f=0, spis=[]):

    users[f"{user_id}&{chat_id}"] = {"message_id": message_id, "subjects": subjects, "bal": bal, "f": f, "spis": spis}

def add_bal_users(user_id, chat_id, bal):
    users[f"{user_id}&{chat_id}"]["bal"] = bal

def check_users(user_id, chat_id):
    if f"{user_id}&{chat_id}" in users:
        return True,\
               users[f"{user_id}&{chat_id}"]["message_id"],\
               users[f"{user_id}&{chat_id}"]["subjects"],\
               users[f"{user_id}&{chat_id}"]["bal"],\
               users[f"{user_id}&{chat_id}"]["f"],\
               users[f"{user_id}&{chat_id}"]["spis"]
    return False

def del_users(user_id, chat_id):
    del users[f"{user_id}&{chat_id}"]
    return True



def if_int(number):
    try:
        return int(number)
    except:
        return False

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def gen_menu(f):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Вопросы", callback_data="questions"))
    if f:
        markup.add(InlineKeyboardButton("Выбор направления", callback_data="choice"))
    return markup

def gen_menu_one(f):
    markup = InlineKeyboardMarkup()
    if f == 0:
        markup.add(InlineKeyboardButton("<", callback_data="back"), InlineKeyboardButton(">", callback_data="forward"))
    elif f == 1:
        markup.add(InlineKeyboardButton(">", callback_data="forward"))
    elif f == 2:
        markup.add(InlineKeyboardButton("<", callback_data="back"))
    #markup.add(InlineKeyboardButton("Посмотреть ещё", callback_data="view_more"))
    markup.add(InlineKeyboardButton("Меню", callback_data="menu"))
    return markup

def gen_choice(pred, nap=-1):
    subjects = [{"name": "Математика Русский Информатика и ИКТ", "reduction": "math&rus&info"},
                {"name": "Математика Русский Физика", "reduction": "math&rus&phys"},
                {"name": "Математика Русский Химия", "reduction": "math&rus&chem"},
                {"name": "Математика Русский Обществознание", "reduction": "math&rus&soc"},
                {"name": "Русский Обществознание История", "reduction": "rus&soc&hist"},
                {"name": "Математика Русский Творческий экзамен", "reduction": "math&rus&art"},
                {"name": "Русский Обществознание Творческий экзамен", "reduction": "rus&soc&art"}]
    markup = InlineKeyboardMarkup()
    if nap != -1:
        markup.add(InlineKeyboardButton(f"Показать направления ({nap})", callback_data="nap"))
    for i in subjects:
        if pred == i["reduction"]:
            markup.add(InlineKeyboardButton(f"{i['name']} (Выбрано)", callback_data=i["reduction"]))
        else:
            markup.add(InlineKeyboardButton(i["name"], callback_data=i["reduction"]))

    markup.add(InlineKeyboardButton("Меню", callback_data="menu"))
    return markup

def gen_choice_pod(slov):
    markup = InlineKeyboardMarkup()
    for i in slov["programs"]:
        markup.add(InlineKeyboardButton(i["name"], callback_data="1"))


def gen_markup(vopr, n):
    markup = InlineKeyboardMarkup()
    markup.row_width = 7
    #markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"), InlineKeyboardButton("No", callback_data="cb_no"))
    #print(InlineKeyboardButton("Yes", callback_data="cb_yes"))
    #g = [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(2)]
    #print(g[0])
    #gg = [{'text': str(i+1), 'url': None, 'callback_data': str(i+1), 'switch_inline_query': None, 'switch_inline_query_current_chat': None, 'callback_game': None, 'pay': None, 'login_url': None} for i in range(2)]
    #markup.add(gg)
    #n = 23
    for i in range(0, n, 5):
        g = []

        #name =
        if n - i <= 5:
            for j in range(i, n):
                if vopr == j + 1:
                    nom = f"{j + 1} (Выбрано)"
                else:
                    nom = str(j + 1)
                g.append(InlineKeyboardButton(nom, callback_data=nom))
        else:
            for j in range(i, i + 5):
                if vopr == j + 1:
                    nom = f"{j + 1} (Выбрано)"
                else:
                    nom = str(j + 1)
                g.append(InlineKeyboardButton(nom, callback_data=nom))
        markup.add(*g)
        #markup.row(InlineKeyboardButton(str(i+1)))
        # markup.add(InlineKeyboardButton(str(i+1), callback_data=str(i+1)),
        #            InlineKeyboardButton(str(i+2), callback_data=str(i+2)),
        #            InlineKeyboardButton(str(i+3), callback_data=str(i+3)),
        #            InlineKeyboardButton(str(i+4), callback_data=str(i+4)),
        #            InlineKeyboardButton(str(i+5), callback_data=str(i+5)))
    #markup.add(InlineKeyboardButton("<", callback_data="<"), InlineKeyboardButton(">", callback_data=">"))
    markup.add(InlineKeyboardButton("Меню", callback_data="menu"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # if call.data == "cb_yes":
    #     print(call.data)
    #     bot.edit_message_text("test", call.message.chat.id, call.message.message_id, reply_markup=gen_markup())
    #     bot.answer_callback_query(call.id, "Answer is Yes")
    # elif call.data == "cb_no":
    #     bot.answer_callback_query(call.id, "Answer is No")
    if call.data == "questions":

        de = chunks(questions["spis_vop"], 15)
        l = list(de)
        ff = 1
        for i in l:
            #if ff == 1:
                #bot.send_message(call.message.chat.id, "Выберете номер интересуещего вас вопроса\n\n" + str('\n\n'.join(i)))
            #elif ff == len(l):
                #bot.send_message(call.message.chat.id, '\n\n'.join(i), reply_markup=gen_markup(0, len(questions["spis_nom"])))
            #else:
            bot.send_message(call.message.chat.id, '\n\n'.join(i))
            ff += 1
        bot.send_message(call.message.chat.id, "🗳 Выберете номер интересуещего вас вопроса",
                         reply_markup=gen_markup(0, len(questions["spis_nom"])))
        # bot.edit_message_text("Выберете номер интересуещего вас вопроса", call.message.chat.id, call.message.message_id,
        #                       reply_markup=gen_markup(0, len(questions["spis_nom"])))
    elif call.data == "menu":
        if call.message.chat.type == "private":
            check = check_users(call.from_user.id, call.message.chat.id)
            if check:
                del_users(call.from_user.id, call.message.chat.id)
            bot.edit_message_text("🌐 Команды бота:\n\n"
                                  "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n"
                                  "📃 Направления — подберёт перспективные направления по проходным баллам",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_menu(True))
        else:
            bot.edit_message_text("🌐 Команды бота:\n\n"
                                  "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_menu(False))
    elif call.data == "choice":
        if call.message.chat.type == "private":
            bot.edit_message_text("💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n"
                                  "🧮 Для ввода суммы баллов отправьте сумму баллов.\n\n"
                                  "📃 Для получения списка программ необходимо выбрать набор сданных предметов "
                                  "и ввести сумму баллов.",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_choice("0"))

    elif call.data == "forward":
        if call.message.chat.type == "private":
            check = check_users(call.from_user.id, call.message.chat.id)
            if check:
                if int(check[4] + 1) < len(check[5]):
                    f = 0
                    if check[4] + 1 == len(check[5]) - 1:
                        f = 2
                    bot.edit_message_text("🔎 Высокие шансы поступления:\n\n" + "\n\n".join(check[5][check[4] + 1]),
                                          call.message.chat.id, call.message.message_id,
                                          parse_mode='HTML',
                                          reply_markup=gen_menu_one(f)
                                          )
                    add_users(call.message.message_id, call.from_user.id, call.message.chat.id,
                              subjects=check[2],
                              spis=check[5],
                              f=check[4] + 1)

    elif call.data == "back":
        if call.message.chat.type == "private":
            check = check_users(call.from_user.id, call.message.chat.id)
            if check:
                if int(check[4] - 1) != -1:
                    f = 0
                    if check[4] - 1 == 0:
                        f = 1
                    bot.edit_message_text("🔎 Высокие шансы поступления:\n\n" + "\n\n".join(check[5][check[4] - 1]),
                                          call.message.chat.id, call.message.message_id,
                                          parse_mode='HTML',
                                          reply_markup=gen_menu_one(f)
                                          )
                    add_users(call.message.message_id, call.from_user.id, call.message.chat.id,
                              subjects=check[2],
                              spis=check[5],
                              f=check[4] - 1
                              )

    elif call.data == "nap1":
        if call.message.chat.type == "private":
            subjects = {"math&rus&info": "Математика Русский Информатика и ИКТ",
                        "math&rus&phys": "Математика Русский Физика",
                        "math&rus&chem": "Математика Русский Химия",
                        "math&rus&soc": "Математика Русский Обществознание",
                        "rus&soc&hist": "Русский Обществознание История",
                        "math&rus&art": "Математика Русский Творческий экзамен",
                        "rus&soc&art": "Русский Обществознание Творческий экзамен", "reduction": "rus&soc&art"
                        }
            check = check_users(call.from_user.id, call.message.chat.id)
            add_users(call.message.message_id, call.from_user.id, call.message.chat.id, subjects=check[2], f=1)
            predmets = check[2].split("&")
            #print(check, predmets)
            pol_sql = pol_js(predmets[0], predmets[1], predmets[2], str(check[3]), 1)
            spis = []
            for i in pol_sql["programs"]:
               spis.append(f"🔮 <a href='{i['link']}'>{i['name']} {i['code']}</a>\n📊 Прошлогодний проходной балл: {i['bal']}\n"
                           f"👥 Количество бюджетных мест: {i['places']}")
            de = chunks(spis, 10)
            l = list(de)
            #print(len(l))

            ff = 1
            for i in l:
                if ff == 1:
                    bot.send_message(call.message.chat.id, "🔎 Высокие шансы поступления:\n\n" + "\n\n".join(i),
                                     parse_mode='HTML')
                # elif ff == len(l):
                #     bot.send_message(call.message.chat.id, "\n\n".join(i),
                #                      reply_markup=gen_choice(call.data),
                #                      parse_mode='HTML')
                else:
                    bot.send_message(call.message.chat.id, "\n\n".join(i),
                                     parse_mode='HTML')
                ff += 1

            m = bot.send_message(call.message.chat.id,
                                 "💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n"
                                 "🧮 Для ввода суммы баллов отправьте сумму баллов.\n\n"
                                 "📃 Для получения списка программ необходимо выбрать набор сданных предметов "
                                 "и ввести сумму баллов.\n\n"
                                 f"📚 Выбранные предметы: {subjects[check[2]]}\n\n"
                                 f"💿 Введённые баллы: {check[3]}",
                                 reply_markup=gen_choice(check[2], int(pol_sql["quantity"])))
            #print(m)
            add_users(m.message_id, call.from_user.id, call.message.chat.id, subjects=check[2], bal=check[3], f=1)
            # bot.edit_message_text("💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n"
            #                       "🧮 Для ввода суммы баллов отправьте сумму баллов.\n\n"
            #                       "📃 Для получения списка программ необходимо выбрать набор сданных предметов "
            #                       "и ввести сумму баллов.\n\n"
            #                       f"📚 Выбранные предметы: {subjects[check[2]]}\n\n"
            #                       f"💿 Введённые баллы: {check[3]}",
            #                       call.message.chat.id, call.message.message_id,
            #                       reply_markup=gen_choice(check[2]))

    elif call.data in [i for i in ["math&rus&info", "math&rus&phys", "math&rus&chem", "math&rus&soc", "rus&soc&hist", "math&rus&art", "rus&soc&art"]]:
        if call.message.chat.type == "private":
            subjects = {"math&rus&info": "Математика Русский Информатика и ИКТ",
                        "math&rus&phys": "Математика Русский Физика",
                        "math&rus&chem": "Математика Русский Химия",
                        "math&rus&soc": "Математика Русский Обществознание",
                        "rus&soc&hist": "Русский Обществознание История",
                        "math&rus&art": "Математика Русский Творческий экзамен",
                        "rus&soc&art": "Русский Обществознание Творческий экзамен", "reduction": "rus&soc&art"}
            check = check_users(call.from_user.id, call.message.chat.id)
            pl = ""
            if check:
                if check[3] != 0:
                    pl = f"\n\n💿 Введённые баллы: {check[3]}"
                add_users(call.message.message_id, call.from_user.id, call.message.chat.id, call.data, check[3])
            else:
                add_users(call.message.message_id, call.from_user.id, call.message.chat.id, call.data)

            bot.edit_message_text("💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n"
                                  "🧮 Для ввода суммы баллов отправьте сумму баллов.\n\n"
                                  "📃 Для получения списка программ необходимо выбрать набор сданных предметов "
                                  "и ввести сумму баллов.\n\n"
                                  f"📚 Выбранные предметы: {subjects[call.data]}{pl}",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_choice(call.data))
    elif call.data in questions["spis_nom"]:#[str(i) for i in range(24)]:

        bot.edit_message_text(f"💡 Выбран вопрос с номером {call.data}\n\n"
                              f"❓ {questions['vopr'][str(call.data)]}\n\n"
                              f"ℹ️ {questions['nom'][str(call.data)]}",
                              call.message.chat.id, call.message.message_id,
                              reply_markup=gen_markup(int(call.data), len(questions["spis_nom"])))

@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    #bot.send_photo(message.chat.id, open('C:/Users/Zett/Desktop/mir_bot/generating_questions/img/test1.png', 'rb'))
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "🌐 Команды бота:\n\n"
                     "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n"
                     "📈 Направления — подберёт перспективные направления по проходным баллам",
                     reply_markup=gen_menu(True))
    else:
        bot.send_message(message.chat.id, "🌐 Команды бота:\n\n"
                                          "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n",
                         reply_markup=gen_menu(False))

    #bot.send_message(message.chat.id, "Выберете номер интересуещего вас вопроса", reply_markup=gen_markup(0))

@bot.message_handler()
def message_handler_empty(message):
    if message.chat.type == "private":
        number = if_int(message.text)
        if number:
            if 310 >= number >= 0:
                subjects = {"math&rus&info": "Математика Русский Информатика и ИКТ",
                            "math&rus&phys": "Математика Русский Физика",
                            "math&rus&chem": "Математика Русский Химия",
                            "math&rus&soc": "Математика Русский Обществознание",
                            "rus&soc&hist": "Русский Обществознание История",
                            "math&rus&art": "Математика Русский Творческий экзамен",
                            "rus&soc&art": "Русский Обществознание Творческий экзамен", "reduction": "rus&soc&art"}
                check = check_users(message.from_user.id, message.chat.id)
                predmets = check[2].split("&")
                #print(check, predmets)
                pol_sql = pol_js(predmets[0], predmets[1], predmets[2], str(number), 1)
                if pol_sql["quantity"] != 0:
                    spis = []
                    for i in pol_sql["programs"]:
                        spis.append(
                            f"🔮 <a href='{i['link']}'>{i['name']} {i['code']}</a>\n📊 Прошлогодний проходной балл: {i['bal']}\n"
                            f"👥 Количество бюджетных мест: {i['places']}")
                    de = chunks(spis, 10)
                    l = list(de)
                    #print(len(l))
                    #print(l)
                    add_users(message.message_id, message.from_user.id, message.chat.id, subjects=check[2], f=0, spis=l)

                    ff = 1
                    bot.delete_message(message.chat.id, message.message_id)
                    if len(l) > 1:
                    #for i in l:
                        #if ff == 1:
                        # m = bot.send_message(message.chat.id, "🔎 Высокие шансы поступления:\n\n" + "\n\n".join(l[0]),
                        #                      parse_mode='HTML',
                        #                      reply_markup=gen_menu_one())
                        bot.edit_message_text("🔎 Высокие шансы поступления:\n\n" + "\n\n".join(l[0]),
                                              message.chat.id, check[1],
                                              parse_mode='HTML',
                                              reply_markup=gen_menu_one(1)
                                              )
                    elif len(l) == 1:
                        bot.edit_message_text("🔎 Высокие шансы поступления:\n\n" + "\n\n".join(l[0]),
                                              message.chat.id, check[1],
                                              parse_mode='HTML',
                                              reply_markup=gen_menu_one(3)
                                              )
                    #del l[0]
                    # add_users(m.message_id, message.from_user.id, message.chat.id, subjects=check[2], bal=check[3],
                    #           f=1,
                    #           spis=l)

                    # elif ff == len(l):
                    #     bot.send_message(call.message.chat.id, "\n\n".join(i),
                    #                      reply_markup=gen_choice(call.data),
                    #                      parse_mode='HTML')
                    #else:
                        #bot.send_message(message.chat.id, "\n\n".join(i),
                                         #parse_mode='HTML')
                    #ff += 1

                # m = bot.send_message(message.chat.id,
                #                      "💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n"
                #                      "🧮 Для ввода суммы баллов отправьте сумму баллов.\n\n"
                #                      "📃 Для получения списка программ необходимо выбрать набор сданных предметов "
                #                      "и ввести сумму баллов.\n\n"
                #                      f"📚 Выбранные предметы: {subjects[check[2]]}\n\n"
                #                      f"💿 Введённые баллы: {number}",
                #                      reply_markup=gen_choice(check[2], int(pol_sql["quantity"])))
                # print(m)
                #add_users(m.message_id, message.from_user.id, message.chat.id, subjects=check[2], bal=check[3], f=1)
                # check = check_users(message.from_user.id, message.chat.id)
                # if check:
                #     if check[4] != 1:
                #         add_bal_users(message.from_user.id, message.chat.id, number)
                #         subjects = {"math&rus&info": "Математика Русский Информатика и ИКТ",
                #                     "math&rus&phys": "Математика Русский Физика",
                #                     "math&rus&chem": "Математика Русский Химия",
                #                     "math&rus&soc": "Математика Русский Обществознание",
                #                     "rus&soc&hist": "Русский Обществознание История",
                #                     "math&rus&art": "Математика Русский Творческий экзамен",
                #                     "rus&soc&art": "Русский Обществознание Творческий экзамен", "reduction": "rus&soc&art"}
                #         predmets = check[2].split("&")
                #         pol_sql = pol_js(predmets[0], predmets[1], predmets[2], number)
                #         bot.edit_message_text("💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n"
                #                               "🧮 Для ввода суммы баллов отправьте сумму баллов.\n\n"
                #                               "📃 Для получения списка программ необходимо выбрать набор сданных предметов "
                #                               "и ввести сумму баллов.\n\n"
                #                               f"📚 Выбранные предметы: {subjects[check[2]]}\n\n"
                #                               f"💿 Введённые баллы: {number}",
                #                               message.chat.id, check[1],
                #                               reply_markup=gen_choice(check[2], pol_sql["quantity"]))


def test1():
    generating_q("FAQ_T")

    bot.polling(none_stop=True)

# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     #button_hi = KeyboardButton('Привет! 👋')
#     print(1111111111111111111)
#     #greet_kb = ReplyKeyboardMarkup()
#     #greet_kb.add(button_hi)
#     await message.reply("Привет!")#, reply_markup=greet_kb)
#
# @dp.message_handler()
# async def echo(message: types.Message):
#     print(23233232)
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await message.answer(message.text)
#
# def test1():
#     print("START", dp)
#     try:
#         executor.start_polling(dp)#, skip_updates=True)
#     except:
#         print("ERRROR")


# if __name__ == "__main__":

    # config = ctf_get()
    #
    # mon = config["MongoDb"]
    # localhost = mon["localhost"]
    # port = mon["port"]
    # collection_bots = mon["collection_bots"]
    # document_tokens = mon["document_tokens"]
    # collection_django = mon["collection_django"]
    # apps = mon["apps"]
    #
    # vk = config["VK"]
    # V = vk["v"]
    #
    # mod = config["Modules"]
    # bs = mod["bs"]
    # ls = mod["ls"]
    #
    # tok = config["Txt"]["tokens"]
    #
    # url_dj = config["Django"]["url_dj"]
    #
    # questions_file = config["Questions"]["file"]
    #
    # client = MongoClient(localhost, int(port))
    # create_mongo = create_mongodb(client, collection_django, apps)

    # bot.polling()