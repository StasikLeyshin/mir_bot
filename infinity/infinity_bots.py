# -*- coding: utf-8 -*-

import asyncio

from api import api_url
from command_besed import command_list
from command_ls import command_ls_list

class infinity_bots:

    def __init__(self, V, create_mongo, collection_bots, document_tokens, url_dj):

        self.V = V
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.url_dj = url_dj

    async def selection(self, command_list, text, them):
        flag = False
        for c in command_list:
            #print(c.keys)
            for k in c.keys:
                if k == text or k == text[1:]:
                    # print(c)
                    flag = True
                    break
                elif k == text.split(" ")[0] or k == text.split(" ")[0][1:]:
                    flag = True
                    break
                #print(text.split(" ")[0])
            #print(flag)
            if flag:
                for m in c.topics_blocks:
                    if m == them or m == them[1:]:
                        return 0
                if len(c.topics_resolution) == 0:
                    return c
                for n in c.topics_resolution:
                    if n == them or n == them[1:]:
                        return c
                return 0
        return 0


    async def main(self, apis, club_id, them, control):
        #apis = api(club_id, token)
        print("-" * 40)
        print(f"Start group ID: [{club_id}] Them: [{them}]")
        loop = asyncio.get_running_loop()
        asd = await apis.api_get("groups.getLongPollServer", v=self.V, group_id=club_id)
        #print(asd)
        if "error" not in asd:
            #print(asd)
            server = asd['server']
            key = asd['key']
            ts = asd['ts']

            while True:
                try:
                    if control[club_id] != them:
                        print(f"Close {club_id}")
                        return
                    otvet = await api_url(f"{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2").get_json(club_id)
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
                            if from_id == peer_id:
                                print(message)
                                text = message["text"].lower()
                                sel = await self.selection(command_ls_list, text, them)
                                #print(sel, text, command_ls_list)
                                blocs = ["target", "consultants"]
                                print(sel)
                                if sel != 0:
                                    loop.create_task(sel.process(self.V, club_id, message, apis, them,
                                                                 self.create_mongo,
                                                                 self.collection_bots,
                                                                 self.document_tokens,
                                                                 self.url_dj).run())
                                    continue
                                else:
                                    if them not in blocs:
                                        otvet = self.create_mongo.questions_get_one(text)
                                        if otvet != "":
                                            await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                                                message=otvet, random_id=0)
                                            continue
                            # bs
                            if from_id != peer_id:
                                print(message)
                                text = message["text"].lower()
                                sel = await self.selection(command_list, text, them)

                                if sel != 0:
                                    loop.create_task(sel.process(self.V, club_id, message, apis, them,
                                                                 self.create_mongo,
                                                                 self.collection_bots,
                                                                 self.document_tokens,
                                                                 self.url_dj).run())
                                    #await sel.process(self.V, club_id, message, apis, them, self.create_mongo).run()
                                    continue


                except Exception as e:
                    print(e)
                    continue
        #print(asd["code"])
        elif "error" in asd and asd["errcode"] in [5, 38]:
            #print(111111111111111111111)
            await api_url(f"{self.url_dj}").post_json(club_id=club_id, status=1)
            return
        #print(asd)
