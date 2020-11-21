# -*- coding: utf-8 -*-
import asyncio
import time
import os
from pymongo import MongoClient
#import nest_asyncio
import importlib
#nest_asyncio.apply()

from api.api import api, api_url
from api.tokens_setting import tokens_setting
from mongodb.create_mongodb import create_mongodb
from command_besed import command_list

V = 5.103
#club_id = 5411326
club_id = 194180799
start_time = time.time()
#apis = api()
client = MongoClient('localhost', 27017)

create_mongo = create_mongodb(client, "bots", "tokens")
#create_mongo.get_tokens()

def load_modules(file):
   files = os.listdir(file)
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("commands_besed." + m[0:-3])
       #print(m)
load_modules("commands_besed")

#create_mongo.get_tokens(empty = "ar")
#client = MongoClient()
#client = MongoClient('localhost', 27017)
#db = client['bots']
#collection = db['tokens']
#posts = db.posts
#if posts == None:
def start(name):
    with open(f'{name}.txt') as f:
        lines = f.read().splitlines()
    #print(lines)
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(api(0, i.split('&')[0]).api_get("groups.getById", v=f"{V}")) for i in lines]
    results = loop.run_until_complete(asyncio.wait(tasks))

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
    #print(tokens_new_t)
    loop.run_until_complete(tokens_setting(V).main(tokens_new_t, ids))
    create_mongo.create_db(tokens, ids)
    return tokens

start("tokens")

async def selection(command_list, text):
    for c in command_list:
        #print(c.keys)
        for k in c.keys:
            if k == text or k == text[1:]:
                #print(c)
                return c
    return 0
                #await c.process(V, club_id, message, apis).run()


async def main(token, club_id, them):
    apis = api(club_id, token)
    asd = await apis.api_get("groups.getLongPollServer", v=V, group_id=club_id)
    print(asd)
    if "error" not in asd:
        server = asd['server']
        key = asd['key']
        ts = asd['ts']

        while True:
            otvet = await api_url(f"{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2").get_json()
            if "failed" in otvet:
                if otvet["failed"] == 2 or otvet["failed"] == 3:
                    asd = await apis.api_get("groups.getLongPollServer", v=V, group_id=club_id)
                    if "error" not in asd:
                        server = asd['server']
                        key = asd['key']
                        ts = asd['ts']
                        continue

                else:
                    continue

            #print(otvet)
            updates = otvet["updates"]
            #print(updates)
            if "ts" in otvet:
                ts = otvet['ts']
            if len(updates) > 0:
                slovar = updates[0]
                if "type" in slovar and slovar["type"] == "message_new":
                    message = slovar["object"]["message"]
                    from_id = message["from_id"]
                    peer_id = message["peer_id"]
                    #print(message)

                    #ls
                    if from_id == peer_id:pass
                        #print(message)

                    #besed
                    if from_id != peer_id:
                        print(message)
                        text = message["text"].lower()
                        sel = await selection(command_list, text)

                        if sel != 0:
                            await sel.process(V, club_id, message, apis, them, create_mongo).run()
                            continue
                        '''for c in command_list:
                            print(c.keys)
                            for k in c.keys:
                                if k == text or k == text[1:]:
                                    print(c)
                                    await c.process(V, club_id, message, apis).run()'''

                        #print(message)



            #for i in range(0, len(otvet["updates"])):pass
                #print(otvet["updates"])
    #await api().get_http()

st = create_mongo.get_tokens()
#print(st)
async def beskon(st):
    bots = {}
    thems = {}
    for i in st:
        bots[i["id"]] = api(i["id"], token)
        if i["them"] in thems:
            thems[i["them"]] = thems[i["them"]].append(i["id"])
        elif "" not in thems:
            thems[i["them"]] = [i["id"]]
    #print(thems)
    #print(bots)

    while True:
        await asyncio.sleep(60)





loop = asyncio.get_event_loop()
loop.run_until_complete(beskon(st))
#loop.run_until_complete(main(token, club_id, "them1"))



#tokens["club_id"] = i

#create_mongodb('localhost', 27017, tokens, ids).create_db()

#print(lines)


#asyncio.ensure_future(tokens_setting(V).main("tokens"))

#async def main(token):pass 
    



#loop = asyncio.get_event_loop()
#print(loop.run_until_complete(fet_get(f"https://api.vk.com/method/utils.getServerTime?v=5.103&access_token={token}")))
#a = api(club_id, "utils.getServerTime", v = f"{V}", access_token = f"{token}")
#print(loop.run_until_complete(a.api_get()))
#print(loop.run_until_complete(api().api_get("utils.getServerTime", v = f"{V}", access_token = f"{token}")))
print("1) --- %s seconds ---" % (time.time() - start_time))

#response = requests.get(f"https://api.vk.com/method/utils.getServerTime?v=5.103&access_token={token}")
#print(response.json())
#print("2) --- %s seconds ---" % (time.time() - start_time))
#def start(token):