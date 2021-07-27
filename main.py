# -*- coding: utf-8 -*-
import asyncio
import time
import os
from pymongo import MongoClient
import nest_asyncio
import importlib
import configparser
nest_asyncio.apply()
from flask import Flask
from aiohttp import web
import random
import threading

#app = Flask(__name__)

from api import api, api_url, tokens_setting, collecting_list_users
from mongodb import create_mongodb
from command_besed import command_list
from infinity import infinity_bots, infinity_beskon
from generating_questions import generating
from edite_text import opredel_skreen, chunks
from Telegram import test1

def load_modules(file, file_ls):

    files = os.listdir(f"c:{file}")
    file_ls = os.listdir(f"c:{file_ls}")
    modules = filter(lambda x: x.endswith('.py'), files)
    modules_ls = filter(lambda x: x.endswith('.py'), file_ls)
    for m in modules:
        importlib.import_module("commands_besed." + m[0:-3])
    for n in modules_ls:
        importlib.import_module("commands_ls." + n[0:-3])
    return


#@app.route('/')
#def hello():
    #return 'Hello, World!'



def start(name, collection_bots, document_tokens):
    with open(f'{name}.txt') as f:
        lines = f.read().splitlines()

    print(f"number tokens: {len(lines)}")
    #print(lines)

    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(api(0, i.split('&')[0]).api_get("groups.getById", v=f"{V}")) for i in lines]
    loop.run_until_complete(asyncio.wait(tasks))

    tokens = []
    tokens_new = []
    tokens_new_t = []
    ids = []
    for i in range(len(tasks)):
        result = tasks[i].result()
        if "error" not in result:
            if result[0]["id"] not in ids:
                ids.append(result[0]["id"])
                tokens.append({"id": result[0]["id"], "token": lines[i].split('&')[0], "name": result[0]["name"], "them": lines[i].split('&')[1]})
                tokens_new.append(lines[i])
                tokens_new_t.append(lines[i].split('&')[0])

            elif result[0]["id"] in ids:pass
    f = open(f'{name}.txt', 'w')
    f.write("\n".join(tokens_new))
    f.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tokens_setting(V).main(tokens_new_t, ids))
    create_mongo.create_db(collection_bots, document_tokens, tokens, ids)
    return tokens


async def selection(command_list, text):
    for c in command_list:
        #print(c.keys)
        for k in c.keys:
            if k == text or k == text[1:]:
                #print(c)
                return c
    return 0



def apis_generate(spis):
    apis = {}
    #print(spis)
    for i in spis:
        apis[i["id"]] = api(i["id"], i["token"])
    return apis


def ctf_get():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config


async def executor_post(request: web.Request):
    #print(await request.text())
    event = await request.json()
    #event = await request.text()
    #tasks.append(loop.create_task(inf.main(apis[i["id"]], i["id"], i["them"])))
    #print(event)
    if "token" in event and "soc" in event and "id" not in event:
        result = await api(0, event["token"]).api_get("groups.getById", v=f"{V}")
        if "error" not in result:
            data = {"status": 1, "id": result[0]["id"], "name": result[0]["name"]}
            apis[result[0]["id"]] = api(result[0]["id"], event["token"])
            spis.append({"id": result[0]["id"], "name": result[0]["name"], "token": event["token"], "them": event["soc"]})
            '''create_mongo.create_db(collection_bots,
                                   document_tokens,
                                   [{"id": result[0]["id"],
                                     "name": result[0]["name"],
                                     "token": event["token"],
                                     "them": event["soc"]}],
                                   [result[0]["id"]])'''
            await tokens_setting(V).main([event["token"]], [result[0]["id"]])
            loop_control[result[0]["id"]] = event["soc"]
            loop.create_task(inf.main(apis[result[0]["id"]], result[0]["id"], event["soc"], loop_control))

        else:
            data = {"status": 0}

        return web.json_response(data)

    elif "id" in event:
        result = await api(0, event["token"]).api_get("groups.getById", v=f"{V}")
        if "error" not in result:
            #print("------------------")
            data = {"status": 1, "id": result[0]["id"], "name": result[0]["name"]}
            #print(event["id"], spis)
            token = apis[event["id"]].token
            del apis[event["id"]]
            for i in spis:
                if i["id"] == event["id"]:
                    soc = i["them"]
                    spis.remove(i)
                    break
            apis[result[0]["id"]] = api(result[0]["id"], event["token"])
            spis.append({"id": result[0]["id"], "name": result[0]["name"], "token": event["token"], "them": event["soc"]})
            if token != event["token"]:
                loop_control[result[0]["id"]] = event["soc"]
                loop.create_task(inf.main(apis[result[0]["id"]], result[0]["id"], event["soc"], loop_control))
            if loop_control[result[0]["id"]] != event["soc"]:
                loop_control[result[0]["id"]] = event["soc"]
                loop.create_task(inf.main(apis[result[0]["id"]], result[0]["id"], event["soc"], loop_control))


        else:
            data = {"status": 0}

        return web.json_response(data)

    elif "token" in event and "user_link" in event:
        screen_name = await opredel_skreen(event["user_link"], event["user_link"])
        #print(screen_name)
        result = await api(0, event["token"]).api_get("users.get", v=V, user_ids=screen_name)
        if "error" not in result:
            user_id = result[0]["id"]
            data = {"status": 1, "user_id": user_id}
        else:
            data = {"status": 0}
        return web.json_response(data)

    elif "token" in event and "question" in event:
        start_time = time.time()
        users = create_mongo.users_get()
        ran = ["🌝 Вопрос дня и уже у тебя в личных сообщениях, скорее отвечай!",
               "👾 Новый день, новый вопрос, новые возможности, и это всё доступно тебе уже сейчас, можешь уже отвечать:)",
               "🌚 Утро позднее, утро раннее, а вопрос дня неизменно уже у тебя)",
               "👻 Новый вопрос! Бегом отвечать!"
               ]
        #users_new = await chunks(users, 100)
        #for i in users_new:
        result = loop.create_task(collecting_list_users(V, event['club_id']).run(users,
                                                                                 api(event['club_id'],
                                                                                     event['token']),
                                                                                 event['question'],
                                                                                 event['question_id']))
        '''result = loop.create_task(api(0, event["token"]).api_post("messages.send", v=V, peer_ids=i,
                                                                      message=f"{random.choice(ran)}\n\n"
                                                                      f"{event['question']}\n\n"
                                                                      f"⚠ Чтобы ответить на вопрос, напишите /ответ номер вопроса и ваш ответ\n\n"
                                                                      f"❗Номер текущего вопроса: {event['question_id']}",
                                                                      random_id=0))'''
        #await asyncio.sleep(1)

        '''import requests
        result = requests.post("https://api.vk.com/method/messages.send", data={
        "access_token": event["token"],
        "v": 5.103,
        "random_id": 0,
        "message": "1111",
        "peer_ids":users})'''
        result = ""
        if "error" in result:
            data = {"status": 0}
        else:
            data = {"status": 1}
        return web.json_response(data)


    return web.json_response({"status": 0})

async def executor_get(request: web.Request):
    #event = await request.json()
    event = await request.text()
    print(event)
    return web.Response(text="Hello, wor ld")


async def test():
    app = web.Application()
    app.router.add_route(
        path='/',
        method='POST',
        handler=executor_post
    )
    app.router.add_route(
        path='/',
        method='GET',
        handler=executor_get
    )
    #import nest_asyncio
    #nest_asyncio.apply()
    web.run_app(app=app, host="127.0.0.1", port=5000)

async def te():
    try:
        await asyncio.sleep(10)
        loop_control[5411326] = "e"
    except Exception as e:
        print(e)

async def add_group(spis_new):
    ap_url = api_url(f"{url_dj}?")
    for i in spis_new:
        if "peer_id" in i:
            await ap_url.post_json(create=1, token=i["token"], id_group=i["id"], name=i["name"], them=i["them"], peer_id=i["peer_id"])
        else:
            await ap_url.post_json(create=1, token=i["token"], id_group=i["id"], name=i["name"], them=i["them"])
    return





if __name__ == "__main__":
    #import requests
    #import datetime
    #result = requests.post("https://api.vk.com/method/groups.getById", data={"access_token": "c18533e0a343cf748c1c1f167f11876a32082494b463155109fe18f5e52cc9e39f931a8eaaa367d7c4313", "v": 5.103})
    #result = requests.post("http://127.0.0.1:8000/api/", data={"spec": 1})
    #print(result.json())
    #import threading
    #x = threading.Thread(target=app.run())
    #x.start()
    #print(1)

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

    tok = config["Txt"]["tokens"]

    url_dj = config["Django"]["url_dj"]

    questions_file = config["Questions"]["file"]
    questions_file_abitur = config["Questions"]["file_abitur"]
    questions_file_col = config["Questions"]["file_col"]

    load_modules(f"{bs}", f"{ls}")

    client = MongoClient(localhost, int(port))
    create_mongo = create_mongodb(client, collection_django, apps)

    loop.run_until_complete(generating(questions_file, create_mongo).sp_vopr(encoding=1, f=1))

    loop.run_until_complete(generating(questions_file_abitur, create_mongo).sp_vopr(encoding=1, f=1))

    loop.run_until_complete(generating(questions_file_col, create_mongo).sp_vopr(encoding=1, f=1, nap="col"))

    #files = os.listdir("generating_questions/img")
    #print(files)
    #print(filter(lambda x: x.endswith('.png'), files))

    #start(tok, collection_bots, document_tokens)
    #toke = create_mongo.get_tokens(collection_bots, document_tokens)
    #loop1 = asyncio.get_event_loop()
    toke = loop.run_until_complete(api_url(f"{url_dj}?").post_json(get=1))
    #toke = await api_url(f"{url_dj}?").post_json(get=1)
    #spis = toke["list"]
    spis = toke["list"]
    #spis_new = toke[1]
    #print(spis)
    apis = apis_generate(spis)
    print(f"number of working tokens: {len(apis)}")

    inf = infinity_bots(V, create_mongo, collection_bots, document_tokens, url_dj)
    inf_b = infinity_beskon(V, create_mongo, collection_django, apps, collection_bots, document_tokens, apis, spis, url_dj)
    #tasks = []
    #loop1 = asyncio.get_running_loop()
    #loop.close()
    #loop = asyncio.get_running_loop()
    tasks = []
    loop_control = {}
    for i in spis:
        loop_control[i["id"]] = i["them"]
        #loop_control[spis[i]["id"]] = 0

    tasks = [loop.create_task(inf.main(apis[i["id"]], i["id"], i["them"], loop_control, loop)) for i in spis]

    tasks.append(loop.create_task(inf_b.beskon()))
    #print(tasks)
    tasks.append(loop.create_task(test()))

    tasks.append(loop.create_task(inf.main_user(api(1 ,"8eeeba5ca7ebdaed6fa6163a6053722bbfe9eaca70be274d024dcac817010305e267eb749b28d6f0bd54d"), 1)))

    #tasks.append(test1())
    x = threading.Thread(target=test1)
    x.start()

    #tasks.append(loop.create_task(add_group(spis_new)))
    #tasks.append(loop.create_task(te()))
    #print(111111111111)
    results = loop.run_until_complete(asyncio.wait(tasks))
    #print(1)"""

