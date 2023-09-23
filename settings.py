import asyncio
import configparser
import os
import importlib
from pymongo import MongoClient
import pprint

from Tree import tree_distribution_root
from generating_questions.generating_questions import GeneratingCardTaro
from mongodb import create_mongodb, MongoManager
from api import api, api_url, tokens_setting, collecting_list_users
from infinity import infinity_bots, infinity_beskon
from generating_questions import generating, generating_answers

from motor import MotorClient
import yaml




def apis_generate(spis):
    apis = {}
    #print(spis)
    for i in spis:
        apis[i["id"]] = api(i["id"], i["token"])
    return apis



def get_files(folder):
    files_list = os.listdir(path=folder)
    for i in files_list.copy():
        if "." in i or "__" in i:
            files_list.remove(i)
    return files_list


def load_modules(file, file_ls, file_ls_chain):

    files = os.listdir(f"{file}")
    file_ls = os.listdir(f"{file_ls}") #c:{file_ls}
    modules = filter(lambda x: x.endswith('.py'), files)
    modules_ls = filter(lambda x: x.endswith('.py'), file_ls)
    for m in modules:
        importlib.import_module("commands_besed." + m[0:-3])
    for n in modules_ls:
        importlib.import_module("commands_ls." + n[0:-3])

    files_list = get_files(f"{file_ls_chain}")
    modules = []
    # for i in files_list:
    #     #print(i)
    #     files = os.listdir(f"{file_ls_chain}/{i}")
    #     #print(files)
    #     modules = filter(lambda x: x.endswith('.py'), files)
    #     for m in modules:
    #         importlib.import_module(f"{file_ls_chain}.{i}." + m[0:-3])
    import re
    for root, dirs, files in os.walk(f"{file_ls_chain}"):
        for file in files:
            if (file.endswith(".py")):
                root = rf"{root}"
                #na = root.replace(r'\\', '.')
                na = re.sub(r'\\', '.', root)
                na = re.sub('/', '.', na)
                #print(f"{na}." + file[0:-3])
                #print(root, "  ", dirs, "   ", file)
                importlib.import_module(f"{na}." + file[0:-3])
                #print(root, "  ", dirs, "   ", files)
                #print(os.path.join(root, file))
    return


def ctf_get():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config

loop = asyncio.get_event_loop()

config = ctf_get()

mon = config["MongoDb"]
localhost = mon["localhost"]
port = mon["port"]
collection_bots = mon["collection_bots"]
document_tokens = mon["document_tokens"]
collection_django = mon["collection_django"]
apps = mon["apps"]

vk = config["VK"]
V = vk["v"]

mod = config["Modules"]
bs = mod["bs"]
ls = mod["ls"]
ls_chain = mod["ls_chain"]

tok = config["Txt"]["tokens"]

url_dj = config["Django"]["url_dj"]

questions_file = config["Questions"]["file"]
questions_file_abitur = config["Questions"]["file_abitur"]
questions_file_col = config["Questions"]["file_col"]

user_bot = config["Userbot"]
user_bot_id = user_bot["user_id"]
user_bot_token = user_bot["token"]

telegram_bot = config["Telegram"]
from_bot_id_tg = telegram_bot["from_id"]
token_bot_tg = telegram_bot["token"]

load_modules(f"{bs}", f"{ls}", f"{ls_chain}")
tree_distribution_root()

client = MongoClient(localhost, int(port))
create_mongo = create_mongodb(client, collection_django, apps)

uri = 'mongodb://localhost:27017'
client = MotorClient(uri)
mongo_manager = MongoManager(client)

with open('description_commands.yaml', encoding="utf-8") as fh:
    read_data = yaml.load(fh, Loader=yaml.FullLoader)

generating_card_taro = GeneratingCardTaro("Таро/ТАРО").start("Для бота")
read_data["taro"] = generating_card_taro

loop.run_until_complete(mongo_manager.settings_update_one(read_data, "settings"))
settings_info = loop.run_until_complete(mongo_manager.settings_insert_one(read_data, "settings"))


# gen = generating(questions_file, create_mongo)
#
# loop.run_until_complete(gen.sp_vopr(sheet="Бакалавриатспециалитет", f=1, nap="bachelors"))
#
# loop.run_until_complete(gen.sp_vopr(sheet="Магистратура", f=1, nap="magistracy"))
#
# loop.run_until_complete(gen.sp_vopr(sheet="Колледж", f=1, nap="college"))
#
# loop.run_until_complete(gen.sp_vopr(sheet="Студентам", f=1, nap="student"))


toke = loop.run_until_complete(api_url(f"{url_dj}?").post_json(get=1))
#toke = await api_url(f"{url_dj}?").post_json(get=1)
#spis = toke["list"]
spis = toke["list"]
# for i in spis:
#     i['token'] = "ffjgbtu9rgfiewie3r48fgrjeori44i5jrtboirtkgj89gt4gio"
#spis_new = toke[1]
#print(spis)
apis = apis_generate(spis)

apis[int(user_bot_id)] = api(int(user_bot_id), user_bot_token)

apis[int(from_bot_id_tg)] = api(int(from_bot_id_tg), token_bot_tg, True)

print(f"number of working tokens: {len(apis)}")

inf = infinity_bots(V, create_mongo, collection_bots, document_tokens, url_dj)
inf_b = infinity_beskon(V, create_mongo, collection_django, apps, collection_bots, document_tokens, apis, spis, url_dj,
                        mongo_manager=mongo_manager, settings_info=read_data)
#tasks = []
#loop1 = asyncio.get_running_loop()
#loop.close()
#loop = asyncio.get_running_loop()
tasks = []
loop_control = {}
#callback_apis = {}
for i in spis:
    loop_control[i["id"]] = i["them"]


tree_questions = generating_answers('test').start('Вопросы JS НОЯБРЬ')

# pprint.pprint(spis)
# pprint.pprint(loop_control)
