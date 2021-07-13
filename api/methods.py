# -*- coding: utf-8 -*-
import asyncio
import json
import ujson
import random

from api.api import api
from api.api_execute import mailing
from edite_text import opredel_skreen, chunks

class methods:

    def __init__(self, v, club_id):

        self.v = v
        self.club_id = club_id

    async def admin_chek(self, peer_id, from_id, apis):
        response = await apis.api_get("messages.getConversationMembers", peer_id=peer_id, v=self.v)
        if "error" not in response:
            for element in response["items"]:
                if "is_admin" in element:
                    if element["is_admin"] is True and from_id == element["member_id"]:
                        return 1
            return 0
        return -1

    async def users_chek(self, peer_id, apis):
        response = await apis.api_get("messages.getConversationMembers", peer_id=peer_id, v=self.v)
        if "error" not in response:
            users = {}
            users_vse = []
            users_adm = []
            for element in response["items"]:
                if "is_admin" in element:
                    if element["is_admin"] is True:
                        users[element["member_id"]] = {"admin": True}
                        users_adm.append(element["member_id"])
                        #users.append({"user_id": element["member_id"], "admin": True})
                        users_vse.append(element["member_id"])
                else:
                    users[element["member_id"]] = {"admin": False}
                    #users.append({"user_id": element["member_id"], "admin": False})
                    users_vse.append(element["member_id"])

            return users, users_vse, users_adm
        return False



class messages_edit:

    def __init__(self, v, club_id, apis, peer_id, text):

        self.v = v
        self.club_id = club_id
        self.apis = apis
        self.text = text
        self.peer_id = peer_id
        self.masg = 0


    async def start_send(self):

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



class collecting_list_users:

    def __init__(self, v, club_id):

        self.v = v
        self.club_id = club_id


    async def run(self, users_old, apis, question, question_id):

        ran = ["🌝 Вопрос дня и уже у тебя в личных сообщениях, скорее отвечай!",
               "👾 Новый день, новый вопрос, новые возможности, и это всё доступно тебе уже сейчас, можешь уже отвечать:)",
               "🌚 Утро позднее, утро раннее, а вопрос дня неизменно уже у тебя)",
               "👻 Новый вопрос! Бегом отвечать!"
               ]
        users = await chunks(users_old, 100)
        for i in users:
            users_25 = await chunks(i, 25)
            new_users = []
            for j in users_25:
                #j_int = [int(i) for i in j]
                new_use = await apis.api_post("execute", code=mailing(v=self.v, users=j, group_id=int(self.club_id)), v=self.v)
                print(555, new_use)
                new_users = new_users + new_use
            print(new_users)
            await apis.api_post("messages.send", v=self.v, peer_ids=",".join(new_users),
                                message=f"{random.choice(ran)}\n\n"
                                f"{question}\n\n"
                                f"⚠ Чтобы ответить на вопрос, напишите /ответ номер вопроса и ваш ответ\n\n"
                                f"❗Номер текущего вопроса: {question_id}",
                                random_id=0)

