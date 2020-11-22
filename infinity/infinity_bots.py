# -*- coding: utf-8 -*-

import asyncio

from api import api_url
from command_besed import command_list

class infinity_bots:

    def __init__(self, V, create_mongo, collection_bots, document_tokens):

        self.V = V
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens

    async def selection(self, command_list, text):
        for c in command_list:
            # print(c.keys)
            for k in c.keys:
                if k == text or k == text[1:]:
                    # print(c)
                    return c
        return 0


    async def main(self, apis, club_id, them):
        #apis = api(club_id, token)
        loop = asyncio.get_running_loop()
        asd = await apis.api_get("groups.getLongPollServer", v=self.V, group_id=club_id)
        print(asd)
        if "error" not in asd:
            server = asd['server']
            key = asd['key']
            ts = asd['ts']

            while True:
                otvet = await api_url(f"{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2").get_json()
                if "failed" in otvet:
                    if otvet["failed"] == 2 or otvet["failed"] == 3:
                        asd = await apis.api_get("groups.getLongPollServer", v=self.V, group_id=club_id)
                        if "error" not in asd:
                            server = asd['server']
                            key = asd['key']
                            ts = asd['ts']
                            continue

                    else:
                        continue

                updates = otvet["updates"]
                if "ts" in otvet:
                    ts = otvet['ts']
                if len(updates) > 0:
                    slovar = updates[0]
                    if "type" in slovar and slovar["type"] == "message_new":
                        message = slovar["object"]["message"]
                        from_id = message["from_id"]
                        peer_id = message["peer_id"]
                        # print(message)

                        # ls
                        if from_id == peer_id: pass
                        # print(message)

                        # bs
                        if from_id != peer_id:
                            print(message)
                            text = message["text"].lower()
                            sel = await self.selection(command_list, text)

                            if sel != 0:
                                loop.create_task(sel.process(self.V, club_id, message, apis, them, self.create_mongo, self.collection_bots, self.document_tokens).run())
                                #await sel.process(self.V, club_id, message, apis, them, self.create_mongo).run()
                                continue

