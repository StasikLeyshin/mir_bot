import asyncio
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# import asyncio
# import configparser
# from pymongo import MongoClient
# from mongodb import create_mongodb
# from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
# #import keyboards as kb

import traceback
import re


from Telegram.bot_setting import bot
from Telegram.user import users
from middlewares import SimpleHandler
from sql import pol_js
from generating_questions import questions, questions_col, loop_new, create_mongo, global_dict
from api import api_url
from edite_text import URL_REGEX
#from settings import *

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
    f2 = open(f"{file}.txt", "r+", encoding="utf8")
    s = f2.readlines()
    f2.seek(0)
    f2.close()
    #vopr = {"nom": {}, "vopr": {}, "spis_nom": [], "spis_vop": []}
    for i in s:
        pas = i[i.find(":") + 1:]
        logi = i[:i.find(":")]
        nom = pas[pas.find(":") + 1:].replace("\\v", "\n")
        vopr = pas[:pas.find(':')].replace("\x1e", "")
        questions["nom"][logi] = nom
        questions["vopr"][vopr] = nom
        questions["spis_nom"].append(str(logi))
        questions["spis_vop"].append(f"{vopr}")

def generating_col(file):
    f2 = open(f"{file}.txt", "r+", encoding="utf8")
    s = f2.readlines()
    f2.seek(0)
    f2.close()
    #vopr = {"nom": {}, "vopr": {}, "spis_nom": [], "spis_vop": []}
    for i in s:
        pas = i[i.find(":") + 1:]
        logi = i[:i.find(":")]
        nom = pas[pas.find(":") + 1:].replace("\\v", "\n")
        vopr = pas[:pas.find(':')].replace("\x1e", "")
        questions_col["nom"][logi] = nom
        questions_col["vopr"][vopr] = nom
        questions_col["spis_nom"].append(str(logi))
        questions_col["spis_vop"].append(f"{vopr}")

def add_users(message_id, user_id, chat_id, subjects="", bal=0, f=0, spis=[], perv=""):

    users[f"{user_id}&{chat_id}"] = {"message_id": message_id, "subjects": subjects, "bal": bal, "f": f, "spis": spis,
                                     "perv": perv}

def add_bal_users(user_id, chat_id, bal):
    users[f"{user_id}&{chat_id}"]["bal"] = bal

def check_users(user_id, chat_id):
    if f"{user_id}&{chat_id}" in users:
        return True,\
            users[f"{user_id}&{chat_id}"]["message_id"],\
            users[f"{user_id}&{chat_id}"]["subjects"],\
            users[f"{user_id}&{chat_id}"]["bal"],\
            users[f"{user_id}&{chat_id}"]["f"],\
            users[f"{user_id}&{chat_id}"]["spis"],\
            users[f"{user_id}&{chat_id}"]["perv"]

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


def snils_check(from_id, txt="0", snils="0", flag=0):
    try:
        if not if_int(snils.replace("-", "")) and flag != 1:
            return 0, [["Введите СНИЛС/уникальный номер в правильном формате"]]

        res = loop_new.run_until_complete(
                create_mongo["create_mongo"].users_directions_add_finish(from_id, txt, flag=flag))
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
        de = chunks(directions_list, 5)
        l = list(de)
        create_mongo["create_mongo"].add_user(from_id, 0)

        return 1, l
    except Exception as e:
        print(traceback.format_exc())


def set_create_mongo(create_mongo_new):
    create_mongo["create_mongo"] = create_mongo_new

def set_global_dict(mongo_manager, settings_info, loop, collection_bots, document_tokens, url_dj, client, tree_questions):
    global_dict["mongo_manager"] = mongo_manager
    global_dict["settings_info"] = settings_info
    global_dict["loop"] = loop
    global_dict["collection_bots"] = collection_bots
    global_dict["document_tokens"] = document_tokens
    global_dict["url_dj"] = url_dj
    global_dict["client"] = client
    global_dict["tree_questions"] = tree_questions


def gen_menu(f):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Вопросы", callback_data="questions"))
    if f:
        markup.add(InlineKeyboardButton("Выбор направления", callback_data="choice"))
        #markup.add(InlineKeyboardButton("Конкурс", callback_data="competition"))
    return markup

# def gen_menu_only_one():
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Меню", callback_data="menu"))
#     return markup


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

def gen_competition(f):
    markup = InlineKeyboardMarkup()
    if f == 0:
        markup.add(InlineKeyboardButton("Добавить СНИЛС/уникальный номер", callback_data="competition_add"))
        markup.add(InlineKeyboardButton("Посмотреть анонимно", callback_data="competition_anonymous"))
    elif f == 1:
        markup.add(InlineKeyboardButton("Моя ситуация", callback_data="my_situation"))
        markup.add(InlineKeyboardButton("Посмотреть анонимно", callback_data="competition_anonymous"))
        markup.add(InlineKeyboardButton("Изменить СНИЛС/уникальный номер", callback_data="competition_add"))

    markup.add(InlineKeyboardButton("Меню", callback_data="menu"))
    return markup

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

#@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # if call.data == "cb_yes":
    #     print(call.data)
    #     bot.edit_message_text("test", call.message.chat.id, call.message.message_id, reply_markup=gen_markup())
    #     bot.answer_callback_query(call.id, "Answer is Yes")
    # elif call.data == "cb_no":
    #     bot.answer_callback_query(call.id, "Answer is No")
    if call.data == "questions":
        if call.message.chat.id != -1001290867279:
            markup = ReplyKeyboardMarkup()
            for i in questions["spis_vop"]:
                markup.add(KeyboardButton(i))
            markup.add(KeyboardButton("Меню"))
            bot.send_message(call.message.chat.id, "🗳 Выберите интересующий вас вопрос",
                             reply_markup=markup)
        else:
            markup = ReplyKeyboardMarkup()
            for i in questions_col["spis_vop"]:
                markup.add(KeyboardButton(i))
            markup.add(KeyboardButton("Меню"))
            bot.send_message(call.message.chat.id, "🗳 Выберите интересующий вас вопрос",
                             reply_markup=markup)
        # de = chunks(questions["spis_vop"], 15)
        # l = list(de)
        # ff = 1
        # for i in l:
        #     #if ff == 1:
        #         #bot.send_message(call.message.chat.id, "Выберете номер интересуещего вас вопроса\n\n" + str('\n\n'.join(i)))
        #     #elif ff == len(l):
        #         #bot.send_message(call.message.chat.id, '\n\n'.join(i), reply_markup=gen_markup(0, len(questions["spis_nom"])))
        #     #else:
        #     bot.send_message(call.message.chat.id, '\n\n'.join(i))
        #     ff += 1
        # bot.send_message(call.message.chat.id, "🗳 Выберете номер интересуещего вас вопроса",
        #                  reply_markup=gen_markup(0, len(questions["spis_nom"])))
        # bot.edit_message_text("Выберете номер интересуещего вас вопроса", call.message.chat.id, call.message.message_id,
        #                       reply_markup=gen_markup(0, len(questions["spis_nom"])))

    elif call.data == "competition":
        if call.message.chat.type == "private":
            create_mongo["create_mongo"].add_user(call.message.chat.id, 0)
            res = loop_new.run_until_complete(create_mongo["create_mongo"].users_directions_add_start(call.message.chat.id))
            f = 0
            if res:
                f = 1
            bot.edit_message_text("🧩 Выберите нужную функцию",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_competition(f))
    elif call.data == "competition_add":
        if call.message.chat.type == "private":
            create_mongo["create_mongo"].add_user(call.message.chat.id, 5)
            res = loop_new.run_until_complete(
                create_mongo["create_mongo"].users_directions_add_start(call.message.chat.id))
            f = 0
            if res:
                f = 1
            bot.edit_message_text("Введите ваш СНИЛС/уникальный номер",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_competition(f))

    elif call.data == "competition_anonymous":
        if call.message.chat.type == "private":
            create_mongo["create_mongo"].add_user(call.message.chat.id, 6)
            res = loop_new.run_until_complete(
                create_mongo["create_mongo"].users_directions_add_start(call.message.chat.id))
            f = 0
            if res:
                f = 1
            bot.edit_message_text("Введите СНИЛС/уникальный номер",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=gen_competition(f))

    elif call.data == "my_situation":
        if call.message.chat.type == "private":
            loop_new.run_until_complete(
                create_mongo["create_mongo"].users_directions_add_start(call.message.chat.id))
            msg = snils_check(call.message.chat.id, flag=1)
            g = 1
            for i in msg[1]:
                if g == len(msg[1]):
                    bot.send_message(call.message.chat.id, "\n\n".join(i), reply_markup=gen_competition(msg[0]))
                else:
                    bot.send_message(call.message.chat.id, "\n\n".join(i))
                g += 1


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
                    bot.edit_message_text(check[6] + "\n\n".join(check[5][check[4] + 1]),
                                          call.message.chat.id, call.message.message_id,
                                          parse_mode='HTML',
                                          reply_markup=gen_menu_one(f)
                                          )
                    add_users(call.message.message_id, call.from_user.id, call.message.chat.id,
                              subjects=check[2],
                              spis=check[5],
                              f=check[4] + 1,
                              perv=check[6])

    elif call.data == "back":
        if call.message.chat.type == "private":
            check = check_users(call.from_user.id, call.message.chat.id)
            if check:
                if int(check[4] - 1) != -1:
                    f = 0
                    if check[4] - 1 == 0:
                        f = 1
                    bot.edit_message_text(check[6] + "\n\n".join(check[5][check[4] - 1]),
                                          call.message.chat.id, call.message.message_id,
                                          parse_mode='HTML',
                                          reply_markup=gen_menu_one(f)
                                          )
                    add_users(call.message.message_id, call.from_user.id, call.message.chat.id,
                              subjects=check[2],
                              spis=check[5],
                              f=check[4] - 1,
                              perv=check[6])

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
               spis.append(f"🔮 <a href='{i['link']}'>{i['name']} {i['code']}</a>\n📊 Прошлогодний проходной балл на бюджет:{i['bal']}\n"
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

#@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    #bot.send_photo(message.chat.id, open('C:/Users/Zett/Desktop/mir_bot/generating_questions/img/test1.png', 'rb'))
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "🌐 Команды бота:\n\n"
                                          "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n"
                                          "📈 Направления — подберёт перспективные направления по проходным баллам\n\n",
                                          #"📊 Конкурс — покажет текущее положение в списке",
                         reply_markup=gen_menu(True))
    else:
        # markup = ReplyKeyboardMarkup()
        # markup.add(KeyboardButton({}))
        # bot.send_message(message.chat.id, message.chat.id, reply_markup=markup)
        bot.send_message(message.chat.id, '_', reply_markup=ReplyKeyboardRemove())
                         #reply_markup=gen_menu(False))
        # bot.send_message(message.chat.id, "🌐 Команды бота:\n\n"
        #                                   "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n",
        #                  reply_markup=gen_menu(False))

    #bot.send_message(message.chat.id, "Выберете номер интересуещего вас вопроса", reply_markup=gen_markup(0))

# @bot.message_handler(commands=['id'])
# def message_handler(message):
#     bot.send_message(message.chat.id, f"{message.chat.id}") #-1001290867279



@bot.callback_query_handler(func=lambda call: True)
def callback_query_new(call):
    #print(call.message.chat)
    if call.message.chat.type == "private":
        message_dict = {
            "peer_id": call.from_user.id,
            "from_id": call.from_user.id,
            "message": call.message,
            "date": call.message.date,
            "text": call.data,
            # "conversation_message_id": 0,
            "id": call.message.message_id,
            # "fwd_messages": [],
        }
        #print(message_dict)
        global_dict["loop"].create_task(
            SimpleHandler("105", 1768876438, message_dict, bot,
                          "tema1",
                          create_mongo["create_mongo"], global_dict["collection_bots"],
                          global_dict["document_tokens"], global_dict["url_dj"],
                          global_dict["loop"], global_dict["client"],
                          mongo_manager=global_dict["mongo_manager"],
                          settings_info=global_dict["settings_info"],
                          tree_questions=global_dict["tree_questions"],
                          is_telegram=True).middleware_ls())



@bot.message_handler()
def message_handler_empty(message):
    #print(message)
    if int(message.from_user.id) == 447019454:pass
        #print(message)

        #print(bot.get_chat_member(message.chat.id))
        #print(bot.get_chat_member())
        # print(bot.get_chat_administrators(message.chat.id))
        # for i in bot.get_chat_administrators(message.chat.id):
        #     print(i)
    if message.text.lower() == "/привязать" and int(message.from_user.id) == 447019454:
        print(message.chat.id, message.chat.title)
        # post = await api_url(f"http://45.155.207.247/api/").post_json(club_id=message.chat.title,
        #                                                               Conver=message.chat.id, create_bs=2)
        # loop = asyncio.get_event_loop()
        # post = loop.run_until_complete(api_url(f"http://45.155.207.247/api/").post_json(club_id=message.chat.title,
        #                                                               Conver=message.chat.id, create_bs=2))

        import requests

        post = requests.post("http://45.155.207.247/api/", data={"name": message.chat.title,
                                                                 "Conver": message.chat.id,
                                                                 "create_bs": 2})
        #print(post.json())
        if "error" in post.json():
            bot.send_message(message.chat.id, "☢ Беседа уже была привязана")
        else:
            bot.send_message(message.chat.id, "✅ Беседа успешно привязана")


    if message.chat.type == "supergroup":

        message_dict = {
            "peer_id": message.chat.id,
            "from_id": message.from_user.id,
            "message": message,
            "date": message.date,
            "text": message.text,
            # "conversation_message_id": 0,
            "id": message.message_id,
            # "fwd_messages": [],
        }
        #print("TEST")
        #print(bot.resol)
        #print(message.entities[0])
        #print(bot.get_chat_administrators(message.chat.id)[0])

        global_dict["loop"].create_task(
            SimpleHandler("105", 1768876438, message_dict, bot,
                          "tema1",
                          create_mongo["create_mongo"], global_dict["collection_bots"],
                          global_dict["document_tokens"], global_dict["url_dj"],
                          global_dict["loop"], global_dict["client"],
                          mongo_manager=global_dict["mongo_manager"],
                          settings_info=global_dict["settings_info"], is_telegram=True).middleware_ls(True))

    if message.chat.type == "private":
        # if message.text.lower() == "/start" and int(message.from_user.id) == 447019454:
        #     bot.send_message(message.chat.id, "Привет, я — бот приёмной комиссии."
        #                                       "Я попробую ответить на ваши вопросы."
        #                                       "Если что-то пойдёт не так, переведу на сотрудника."
        #                                       "Если вы хотите сразу поговорить с сотрудником напишите слово «оператор»."
        #                                       "Укажите, о чём вы хотели бы узнать (цифрой).",
        #                              reply_markup=gen_menu_new(True))

            # ter = bot.send_message(message.chat.id, "Test")
            # print(ter)
            message_dict = {
                "peer_id": message.chat.id,
                "from_id": message.from_user.id,
                "message": message,
                "date": message.date,
                "text": message.text,
                # "conversation_message_id": 0,
                "id": message.message_id,
                # "fwd_messages": [],
            }
            #print("TEST")
            #print(bot.resol)
            #print(message.entities[0])
            #print(bot.get_chat_administrators(message.chat.id)[0])

            global_dict["loop"].create_task(
                SimpleHandler("105", 1768876438, message_dict, bot,
                              "tema1",
                              create_mongo["create_mongo"], global_dict["collection_bots"],
                              global_dict["document_tokens"], global_dict["url_dj"],
                              global_dict["loop"], global_dict["client"],
                              mongo_manager=global_dict["mongo_manager"],
                              settings_info=global_dict["settings_info"],
                              tree_questions=global_dict["tree_questions"],
                              is_telegram=True).middleware_ls())




    # if message.text.lower() == "/start":
    #     text = '<div>На какие мероприятия от РТУ МИРЭА сходить в ближайшую неделю.</div><div><br></div><div>Регистрация на все мероприятия доступна в личном кабинете школьника на сайте приёмной комиссии https://vk.cc/cds2zi.</div><div><br></div><div>Дни открытых дверей</div><div><br></div><div>25 марта, суббота, 11:00 — День открытых дверей всех образовательных программ, онлайн. Регистрация https://vk.cc/cluy5V</div><div><br></div><div>26 марта, воскресенье, 11:00 — День открытых дверей Колледжа программирования и кибербезопасности, проспект Вернадского, 78. Регистрация https://vk.cc/cluyjc</div><div><br></div><div>2 апреля, воскресенье — День открытых дверей всех образовательных программ, проспект Вернадского, 78.&nbsp;</div><div><br></div><div>Регистрация 11:00 https://vk.cc/cluyrZ</div><div><br></div><div>Регистрация 13:00 https://vk.cc/cluyy7</div><div><br></div><div>(Программы для Дня открытых дверей с началом в 11:00 и с началом в 13:00 идентичны).</div><div><br></div><div>Важное&nbsp;</div><div><br></div><div>Московский конкурс межпредметных навыков и знаний «Интеллектуальный мегаполис. Потенциал». Участвовать https://vk.cc/cluwtq</div><div><br></div><div>Другие олимпиады и конкурсы, которые могут помочь в поступлении https://vk.cc/cjmsgx</div><div><br></div><div>Онлайн отборочный тур «Кибербиатлон-2023». Участвовать https://vk.cc/clZ5pP</div><div><br></div><div>29 марта, среда, 13:00-18:00 — День абитуриента Роскосмоса. Адрес:пр-т Мира, 119, ВДНХ, павильон №34</div><div><br></div><div>Лучшие мероприятия</div><div><br></div><div>Меганаправление «Информационные технологии и анализ данных»</div><div><br></div><div>23 марта, четверг, 17:00 — очная экскурсия в локацию Института информационных технологий. Адрес: проспект Вернадского, 78. Регистрация https://vk.cc/cm9GBg</div><div><br></div><div>28 марта, вторник, 16:20 — онлайн лекция «Цифровая трансформация процессов и организаций». Регистрация https://vk.cc/cmmzR7</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/cjmskK</div><div><br></div><div>Меганаправление «Химия и биотехнологиях»</div><div><br></div><div>23 марта, четверг, 17:00 — онлайн встреча «100 вопросов представителю Института тонких химических технологий им. М.В. Ломоносова». Регистрация https://vk.cc/clZ6a9</div><div>27 марта, понедельник, 16:00 — один день с Институтом перспективных технологий и индустриального программирования. Знакомство с направлением подготовки «Материаловедение и технологии материалов». Адрес: улица Стромынка, 20. Регистрация https://vk.cc/cmmA7t</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/cjmsoh</div><div><br></div><div>Меганаправление «Радиоэлектроника»</div><div><br></div><div>23 марта, четверг, 16:30 — онлайн лекция «Структура и принцип работы радиолокатора». Регистрация https://vk.cc/cm9GZw</div><div><br></div><div>24 марта, пятница, 16:30 — очная экскурсия по учебно-научным лабораториям кафедры радиоволновых процессов и технологий. Адрес: проспект Вернадского, 78. Регистрация https://vk.cc/cmmAA5</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/ciAL8K</div><div><br></div><div>Меганаправление «Робототехника и автоматизация производств»</div><div><br></div><div>23 марта, четверг, 16:30 — очный мастер-класс «Сквозной монтаж компонентов на печатные платы». Адрес: проспект Вернадского, 78. Регистрация https://vk.cc/clZ7xb</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/ciALTZ</div><div><br></div><div>Меганаправление «Экономика и управление»</div><div><br></div><div>21 марта, вторник, 16:30 — онлайн встреча с представителем направления Управление персоналом. Регистрация https://vk.cc/cm9HjI</div><div><br></div><div>27 марта, понедельник, 18:00 — онлайн мастер-класс «Урок финансовой грамотности: триггеры маркетинга или как управляют покупателями». Регистрация https://vk.cc/cmmAVy</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/ciAMcy</div><div><br></div><div>Меганаправление «Юриспруденция»</div><div><br></div><div>22 марта, среда, 16:00 — очная лекция «Проблемы защиты государства от промышленного шпионажа». Адрес: улица Стромынка, 20. Регистрация https://vk.cc/cm9HRo</div><div><br></div><div>27 марта, понедельник, 16:00 — очная экскурсия на кафедру Правовое обеспечение национальной безопасности. Адрес: улица Стромынка, 20. Регистрация https://vk.cc/cmmB4E</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/cjmsLe</div><div><br></div><div>Меганаправление «Дизайн»</div><div><br></div><div>23 марта, четверг, 16:30 — очный мастер-класс «Изготовление небольшого керамического изделия». Адрес: улица Стромынка, 20. Регистрация https://vk.cc/cm9I6v</div><div><br></div><div>27 марта, понедельник, 17:10 — очная экскурсия по лабораториям кафедры компьютерного дизайна. Адрес: 5-я улица Соколиной Горы, 22. Регистрация https://vk.cc/cmmBkt</div><div><br></div><div>Все мероприятия меганаправления https://vk.cc/cm9HZ3</div>'
    #     text = text.replace("<div>", "").replace("</div>", "").replace("<br>", "\n\n").replace("&nbsp;", "")
    #     #bot.send_message(message.chat.id, '[inline URL](http://www.example.com/)', parse_mode='Markdown')
    #     bot.send_message(message.chat.id, text,
    #                      parse_mode='HTML')
    # if message.from_user.id != 777000 and message.from_user.id != 57923444 and message.from_user.id != 447019454\
    #         and message.from_user.id != 1087968824:
    #     if message.chat.type != "private":
    #         res = re.findall(URL_REGEX, f'{message.text}')
    #         if res:
    #             bot.delete_message(message.chat.id, message.message_id)
    # if message.text == "Меню":
    #     if message.chat.type == "private":
    #         bot.send_message(message.chat.id, "🌐 Команды бота:\n\n"
    #                                           "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n"
    #                                           "📈 Направления — подберёт перспективные направления по проходным баллам",
    #                          reply_markup=gen_menu(True))
    #     else:
    #         bot.send_message(message.chat.id, "🌐 Команды бота:\n\n"
    #                                           "📝 Вопросы — покажет список часто задаваемых вопросов.\n\n",
    #                          reply_markup=gen_menu(False))
    #
    # if message.chat.id != -1001290867279:
    #     if message.text in questions["spis_vop"]:
    #         bot.send_message(message.chat.id, questions["vopr"][message.text])
    # else:
    #     if message.text in questions_col["spis_vop"]:
    #         bot.send_message(message.chat.id, questions_col["vopr"][message.text])
    #
    # if message.chat.type == "private":
    #     chek = create_mongo["create_mongo"].check_user(message.chat.id)
    #     if chek == 5 or chek == 6:
    #         bot.delete_message(message.chat.id, message.message_id)
    #         flag = 0
    #         if chek == 6:
    #             flag = 2
    #         loop_new.run_until_complete(
    #             create_mongo["create_mongo"].users_directions_add_start(message.chat.id))
    #         msg = snils_check(message.chat.id, message.text, snils=message.text, flag=flag)
    #         g = 1
    #         for i in msg[1]:
    #             if flag != 2:
    #                 if g == len(msg[1]):
    #                     res = loop_new.run_until_complete(
    #                         create_mongo["create_mongo"].users_directions_add_start(message.chat.id))
    #                     f = 0
    #                     if res:
    #                         f = 1
    #                     bot.send_message(message.chat.id, "\n\n".join(i), reply_markup=gen_competition(f))
    #             else:
    #                 if flag == 2:
    #                     if g == len(msg[1]):
    #                         res = loop_new.run_until_complete(
    #                             create_mongo["create_mongo"].users_directions_add_start(message.chat.id))
    #                         f = 0
    #                         if res:
    #                             f = 1
    #                         bot.send_message(message.chat.id, "\n\n".join(i), reply_markup=gen_competition(f))
    #                         continue
    #                 bot.send_message(message.chat.id, "\n\n".join(i))
    #             g += 1
    #         return
    #
    #     number = if_int(message.text)
    #     if number:
    #         if 310 >= number >= 0:
    #             number = number - 10
    #             subjects = {"math&rus&info": "Математика Русский Информатика и ИКТ",
    #                         "math&rus&phys": "Математика Русский Физика",
    #                         "math&rus&chem": "Математика Русский Химия",
    #                         "math&rus&soc": "Математика Русский Обществознание",
    #                         "rus&soc&hist": "Русский Обществознание История",
    #                         "math&rus&art": "Математика Русский Творческий экзамен",
    #                         "rus&soc&art": "Русский Обществознание Творческий экзамен", "reduction": "rus&soc&art"}
    #             check = check_users(message.from_user.id, message.chat.id)
    #             if check:
    #                 predmets = check[2].split("&")
    #                 #print(check, predmets)
    #                 pol_sql = pol_js(predmets[0], predmets[1], predmets[2], str(number), 1)
    #                 if pol_sql["quantity"] != 0:
    #                     spis = []
    #                     for i in pol_sql["programs"]:
    #                         spis.append(
    #                             f"🔮 <a href='{i['link']}'>{i['name']} {i['code']}</a>\n📊 Прошлогодний проходной балл на бюджет: {i['bal']}\n"
    #                             f"👥 Количество бюджетных мест: {i['places']}")
    #                     de = chunks(spis, 10)
    #                     l = list(de)
    #                     #print(len(l))
    #                     #print(l)
    #
    #                     ff = 1
    #                     bot.delete_message(message.chat.id, message.message_id)
    #                     perv = "🔎 Высокие шансы поступления:\n\n"
    #                     if pol_sql["quantity"] == -1:
    #                         perv = "🔎 Гарантированное поступление на платное обучение, но на бюджет в прошлом году баллы были выше.\n\n"
    #
    #                     add_users(message.message_id, message.from_user.id, message.chat.id, subjects=check[2], f=0, spis=l,
    #                               perv=perv)
    #
    #                     if len(l) > 1:
    #                     #for i in l:
    #                         #if ff == 1:
    #                         # m = bot.send_message(message.chat.id, "🔎 Высокие шансы поступления:\n\n" + "\n\n".join(l[0]),
    #                         #                      parse_mode='HTML',
    #                         #                      reply_markup=gen_menu_one())
    #                         bot.edit_message_text(perv + "\n\n".join(l[0]),
    #                                               message.chat.id, check[1],
    #                                               parse_mode='HTML',
    #                                               reply_markup=gen_menu_one(1)
    #                                               )
    #                     elif len(l) == 1:
    #
    #                         bot.edit_message_text(perv + "\n\n".join(l[0]),
    #                                               message.chat.id, check[1],
    #                                               parse_mode='HTML',
    #                                               reply_markup=gen_menu_one(3)
    #                                               )
    #                 else:
    #                     bot.edit_message_text("🏤 В РТУ МИРЭА много разных программ и не всегда стоит ориентироваться на проходные баллы прошлого года. Со всеми программами можно ознакомиться на сайте: https://priem.mirea.ru/guide/?level=bach-spec\n\n"
    #                                           "📖 А ещё у нас очень доступное платное образование, а при оплате до 18 августа можно получить скидку на обучение: ссылка.\n\n"
    #                                           "💰Кстати, если вы поступите на бюджет мы вам вернём всю сумму.",
    #                                           message.chat.id, check[1],
    #                                           parse_mode='HTML',
    #                                           reply_markup=gen_menu_one(3)
    #                                           )
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


def test1(create_mongo_new, mongo_manager, settings_info, loop, collection_bots, document_tokens, url_dj, client,
          tree_questions):
    #generating_q("FAQ_T")
    #generating_col("FAQ_T_col")
    set_create_mongo(create_mongo_new)
    set_global_dict(mongo_manager, settings_info, loop, collection_bots, document_tokens, url_dj, client,
                    tree_questions)
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