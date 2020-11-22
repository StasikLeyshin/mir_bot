# -*- coding: utf-8 -*-

import asyncio

class infinity_beskon:

    def __init__(self, V, create_mongo, apis, st):

        self.V = V
        self.create_mongo = create_mongo
        self.apis = apis
        self.st = st

    async def generate(self, st):
        thems = {}
        for i in st:
            if i["them"] in thems:
                thems[i["them"]] = thems[i["them"]].append(i["id"])
            elif i["them"] not in thems:
                thems[i["them"]] = [i["id"]]
        return thems


    async def beskon(self):
        await self.generate(self.st)
        while True:
            await asyncio.sleep(60)
