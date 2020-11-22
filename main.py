# -*- coding: utf-8 -*-
import asyncio
import time
import os
from pymongo import MongoClient
#import nest_asyncio
import importlib
import configparser
#nest_asyncio.apply()

from api import api, api_url, tokens_setting
from mongodb import create_mongodb
from command_besed import command_list
from infinity import infinity_bots, infinity_beskon


def load_modules(file):
   files = os.listdir(f"c:{file}")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("commands_besed." + m[0:-3])



def start(name, collection_bots, document_tokens):
    with open(f'{name}.txt') as f:
        lines = f.read().splitlines()

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
    for i in spis:
        apis[i["id"]] = api(i["id"], i["token"])
    return apis


def ctf_get():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config


if __name__ == "__main__":
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

    load_modules(f"{bs}")

    client = MongoClient(localhost, int(port))
    create_mongo = create_mongodb(client)

    start(tok, collection_bots, document_tokens)

    spis = create_mongo.get_tokens(collection_bots, document_tokens)
    apis = apis_generate(spis)

    inf = infinity_bots(V, create_mongo, collection_bots, document_tokens)
    inf_b = infinity_beskon(V, create_mongo,collection_django, apps, apis, spis)

    tasks = [loop.create_task(inf.main(apis[i["id"]], i["id"], i["them"])) for i in spis]
    tasks.append(loop.create_task(inf_b.beskon()))
    results = loop.run_until_complete(asyncio.wait(tasks))

