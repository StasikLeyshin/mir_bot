# -*- coding: utf-8 -*-

import asyncio

class infinity_beskon:

    def __init__(self, V, create_mongo, apps, collection_django, apis, st):

        self.V = V
        self.create_mongo = create_mongo
        self.apps = apps
        self.apis = apis
        self.st = st
        self.collection_django = collection_django

    async def generate(self, st):
        thems = {}
        for i in st:
            if i["them"] in thems:
                thems[i["them"]] = thems[i["them"]].append(i["id"])
            elif i["them"] not in thems:
                thems[i["them"]] = [i["id"]]
        return thems


    async def beskon(self):
        gen = await self.generate(self.st)
        #print(gen)
        loop = asyncio.get_running_loop()
        while True:
            loop.create_task(self.create_mongo.get(self.collection_django, self.apps))
            await asyncio.sleep(60)
