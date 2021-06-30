# -*- coding: utf-8 -*-

import asyncio
import datetime as DT

from date_compare import date_compare
from api import api_url, api, photo_upload
from help_text import opredel_screen
from Telegram.bot_setting import bot

class infinity_beskon:

    def __init__(self, V, create_mongo, collection_django, apps, collection_bots, document_tokens, apis, st, url_dj):

        self.V = V
        self.create_mongo = create_mongo
        self.apps = apps
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.apis = apis
        self.st = st
        self.collection_django = collection_django
        self.url_dj = url_dj

    async def current_time(self):
        tek = DT.datetime.now()
        dt = DT.datetime.fromisoformat(tek.strftime('%Y-%m-%d %H:%M:%S'))
        return str(dt.timestamp())[:-2]


    async def generate(self, st):
        thems = {}
        for i in st:
            if i["them"] in thems:
                thems[i["them"]].append(i["id"])
            elif i["them"] not in thems:
                thems[i["them"]] = [i["id"]]
        return thems


    async def send(self, kwargs, club_id, peer_id, text, post):
        for i in range(9):
            print(kwargs)
            image = kwargs[f"image_{i+1}"]
            if image != "0":
                res = await photo_upload(self.apis[int(club_id)], self.V, peer_id, kwargs[f"image_{i+1}"],
                                         '/home/stas/mir_bot/media/').upload()
                #res = await photo_upload(self.apis[int(club_id)], self.V, peer_id, "2021/06/29/28ae1abb0bcacd6e81ad2de947ba86da.jpg",
                                         #"/home/stas/mir_bot/media/").upload()
                if res != None:
                    if len(post) > 1:
                        post += f",{res}"
                    else:
                        post += f"{res}"
        #print(post)
        await self.apis[int(club_id)].api_post("messages.send", v=self.V, peer_id=peer_id, random_id=0, message=text, attachment=post)

    async def send_telegram(self, chat_id, text):
        bot.send_message(chat_id, f"{text}")

    async def dispatch(self, kwargs, spis_ras, gen, id_ras):
        loop = asyncio.get_running_loop()
        post = kwargs["post"]
        if len(post) > 1:
            post = await opredel_screen(post)
        text = kwargs["text"]
        for i in spis_ras:
            if i in gen:
                for j in gen[i]:
                    #peer_id = self.create_mongo.get_peer_id(self.collection_bots, self.document_tokens, j)
                    peer_id = self.create_mongo.get_peer_id_new(self.collection_django, self.apps, j, id_ras)
                    print(peer_id)
                    if peer_id[0] != "0":
                        for i in peer_id:
                            if int(i) > 0:
                                loop.create_task(self.send(kwargs, j, int(i), text, post))
                            else:
                                loop.create_task(self.send_telegram(i, text))




    async def get_rass(self, gen):
        results = self.create_mongo.get(self.collection_django, self.apps)
        for i in results:
            #print(i["text"])
            date_chek = date_compare(i["date_start"], i["period"]).compare_date()
            #print(date_chek)
            if date_chek == "1":
                #await api_url(f"{self.url_dj}").post_json(id=i["id"], delete="1")
                spis_ras = self.create_mongo.get_them(self.collection_django, self.apps, i["id"])
                await self.dispatch(i, spis_ras, gen, i["id"])
                await api_url(f"{self.url_dj}").post_json(id=i["id"], delete="1")

            elif date_chek != "0":
                await api_url(f"{self.url_dj}").post_json(id=i["id"], date_start=date_chek)
                spis_ras = self.create_mongo.get_them(self.collection_django, self.apps, i["id"])
                await self.dispatch(i, spis_ras, gen, i["id"])

    async def peer_ids_add(self, apis_new, club_id):
        #for i in self.apis:
        p = await self.apis[int(club_id)].api_post("messages.getConversations", v=self.V, count=200)
        for i in p["items"]:
            #print(i)
            if int(i["conversation"]["peer"]["id"]) > 2000000000:
                print(i["conversation"]["peer"]["id"], club_id)
        return
            #self.create_mongo.update(self.collection_bots, self.document_tokens, i, self.peer_id)

    async def withdrawal_warn_ban(self):
        tek = await self.current_time()
        await self.create_mongo.remove_ban_warn(tek)



    async def beskon(self):
        #[await self.peer_ids_add(self.apis[i], i) for i in self.apis]
        #loop = asyncio.get_running_loop()
        #tasks = [loop.create_task(self.peer_ids_add(self.apis[i], i)) for i in self.apis]
        #loop.run_until_complete(asyncio.wait(tasks))
        #await self.peer_ids_add()
        #gen = await self.generate(self.st)
        loop = asyncio.get_running_loop()
        while True:
            gen = await self.generate(self.st)
            loop.create_task(self.get_rass(gen))
            loop.create_task(self.withdrawal_warn_ban())
            await asyncio.sleep(60)
