# -*- coding: utf-8 -*-
import asyncio
import json
import ujson

from api.api import api
from api.api_execute import api_one_run

class methods:

    def __init__(self, v, club_id):

        self.v = v
        self.club_id = club_id

    async def admin_chek(self, peer_id, from_id, apis):
        response = await apis.api_get("messages.getConversationMembers", peer_id=peer_id, v=self.v)
        if "error" not in response:
            for element in response["items"]:
                if element["is_admin"] is True and from_id == element["member_id"]:
                    return 1
            return 0
        return -1


class messages_edit:

    def __init__(self, v, club_id, apis, peer_id, text):

        self.v = v
        self.club_id = club_id
        self.apis = apis
        self.text = text
        self.peer_id = peer_id
        self.masg = 0


    async def strat_send(self):

        self.msg = await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id, message=self.text, random_id=0)

        return

    async def finish(self, new_text):

        await self.apis.api_post("messages.edit", v=self.v, peer_id=self.peer_id, message=new_text, random_id=0, message_id=self.msg)
        return

    async def del_sms(self):
        #d = await self.apis.api_post("messages.getByConversationMessageId", v=self.v, peer_id=self.peer_id, conversation_message_ids=conversation_message_id)
        #print(d["items"][0]["id"])
        #await self.apis.api_post("messages.delete", v=self.v, message_ids=f"{self.msg}, {d['items'][0]['id']}", delete_for_all=1)
        await self.apis.api_post("messages.delete", v=self.v, message_ids=self.msg, delete_for_all=1)
        return








