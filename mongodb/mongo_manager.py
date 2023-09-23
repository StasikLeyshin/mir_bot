import json
import os
from typing import List

from bson.json_util import dumps
import ujson
#from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

# from api.db import DatabaseManager
# from api.models.generic import User
# from api.utils.logger import logger_config
#
# logger = logger_config(__name__)


class MongoManager:


    # client: AsyncIOMotorClient = None
    # db: AsyncIOMotorDatabase = None



    def __init__(self, client):
        self.client = client
        #self.user_id = user_id
        self.db = self.client["bots"]
        self.logs = self.client["logs"]


    # to be used from /api/public endpoints
    async def user_get_total(self, documents):
        total = await self.db[str(documents)].count_documents({})
        return total

    async def user_get_actives(self, user_id, db):
        users = db.users.find({"user_id": user_id})
        # users_list = []
        # async for user in users:
        #     users_list.append(json.loads(dumps(user)))

        return users

    async def user_get_all(self, documents):
        users_list = []
        users = self.db[str(documents)].find({})

        async for user in users:
            del user["_id"]
            # users_list.append(ujson.loads(dumps(user)))
            users_list.append(user)

        return users_list

    async def user_get_one(self, user_id, documents, is_telegram=False):
        if is_telegram:

            users = self.db[str(documents)].find({"telegram_user_id": user_id})
        else:
            users = self.db[str(documents)].find({"user_id": user_id})


        async for user in users:
            del user["_id"]
            return user  # ujson.loads(dumps(user))

    async def user_insert_one(self, user, documents, is_telegram=False):
        #print(user)
        if is_telegram:
            user_id = user["telegram_user_id"]
        else:
            user_id = user["user_id"]
        _user = await self.user_get_one(user_id=user_id, documents=documents, is_telegram=is_telegram)
        #print(_user)
        if not _user:
            # print("Error")
        #else:
            await self.db[str(documents)].insert_one(user)

            _user = await self.user_get_one(user_id=user_id, documents=documents, is_telegram=is_telegram)

        return _user


    async def user_insert_update_all(self, users, users_all, user_admins, documents):
        operations_ist = []
        #operations_admin_ist = []
        users_all_copy = users_all.copy()
        users_old_list = await self.user_get_all(documents)
        for i in users_old_list:
            #print(i["user_id"])
            if i["user_id"] in user_admins:
                i["admin"] = True
            else:
                i["admin"] = False
            if i["user_id"] in users_all:
                i["output"] = False
                # for j in users:
                #     if i["user_id"] == j["user_id"]:
                #         j["output"] = False
                #         #j["admin"] = j["admin"]
                #         #j["kicked"] = j["kicked"]
                #         break
                users_all_copy.remove(i['user_id'])
            else:
                i["output"] = True

        #print(users_all_copy, users_all)
        for i in users_all_copy:
            for j in users:
                if i == j["user_id"]:
                    operations_ist.append(InsertOne(j))

            # if i["user_id"] not in users_all:
            #     i["output"] = True
            #     # if "kicked" in i:
            #     #     if not i["kicked"]:
            #     #         i["kicked"] = False
            # else:
            #     i["output"] = False


        # for i in users:
        #     operations_admin_ist.append(UpdateOne({'user_id': i['user_id']},
        #                                     {'$set': {
        #                                         'status': i['admin'],
        #                                     }}, upsert=True))
        # result = await self.db[str(documents_admins)].bulk_write(operations_ist)
        #print(users)

        for i in users_old_list:
            operations_ist.append(UpdateOne({'user_id': i['user_id']},
                                            {'$set': {
                                                'admin': i['admin'],
                                                'kicked': i['kicked'],
                                                'output': i['output']
                                            }}))

        #  for i in users:
            # flag = False
            # for j in users_old_list:
            #     if i["user_id"] == j["user_id"]:
            #         flag = True
            #         break
            #if flag:
            # operations_ist.append(UpdateOne({'user_id': i['user_id']},
            #                                 {'$set': {
            #                                     'admin': i['admin'],
            #                                     'kicked': i['kicked'],
            #                                     'output': i['output']
            #                                 }}))
            # else:
            #     operations_ist.append(InsertOne(i))
        await self.db[str(documents)].bulk_write(operations_ist)
        return True




    async def user_update_one(self, user, documents, is_telegram=False):
        #_user = user
        if is_telegram:
            await self.db[str(documents)].update_one({"telegram_user_id": user["telegram_user_id"]}, {"$set": user})
            user_updated = await self.user_get_one(user_id=user["user_id"], documents=documents)
        else:
            await self.db[str(documents)].update_one({"user_id": user["user_id"]}, {"$set": user})
            user_updated = await self.user_get_one(user_id=user["user_id"], documents=documents)

        return user_updated

    async def users_update_influence(self, users_list, documents):
        operations_ist = []
        for i in users_list:
            if i.get('influence'):
                operations_ist.append(UpdateOne({'user_id': i['user_id']},
                                                {'$set': {
                                                    'influence': i['influence']
                                                }}))
        if operations_ist:
            await self.db[str(documents)].bulk_write(operations_ist)
        return True


    async def users_update_ban_warn(self, users_list, documents):
        operations_ist = []
        for i in users_list:
            #if i['punishments']['warn'].get('warn_list'):
            if i['punishments']['warn']:
                #print(i['punishments']['warn'])
                operations_ist.append(UpdateOne({'user_id': i['user_id']},
                                                {'$set': {
                                                    'punishments': {
                                                        'ban': i['punishments']['ban'],
                                                        'warn': {
                                                            'warn_list': i['punishments']['warn']['warn_list']
                                                        }
                                                    },
                                                }}))
        if operations_ist:
            await self.db[str(documents)].bulk_write(operations_ist)
        return True

    async def user_ban_peer_ids_check(self, user, documents_peer_ids):
        #_user = user

        peer_ids = self.db[str(documents_peer_ids)].find({})

        peer_ids_list = []

        async for peer_id in peer_ids:
            #print(peer_id, user)
            user_info = await self.user_get_one(user_id=user["user_id"], documents=str(peer_id["peer_id"]))
            try:
                if user_info:
                    if user_info["punishments"]["ban"].get("status") and not user_info["punishments"]["ban"].get("unban"):
                        peer_ids_list.append(peer_id["peer_id"])
            except:
                continue

        #await self.db[str(documents)].update_one({"user_id": user["user_id"]}, {"$set": user})
        #user_updated = await self.user_get_one(user_id=user["user_id"], documents=documents)

        return peer_ids_list


    async def settings_get_one(self, documents, settings_id=1):

        settings = self.db[str(documents)].find({"id": settings_id})
        async for user in settings:
            del user["_id"]
            return user

    async def settings_insert_one(self, settings, documents):
        _settings = await self.settings_get_one(documents=documents)
        if not _settings:

            await self.db[str(documents)].insert_one(settings)

            _settings = await self.settings_get_one(documents=documents)

        return _settings

    async def settings_update_one(self, settings, documents, settings_id=1):
        #_user = user
        await self.db[str(documents)].update_one({"id": settings_id}, {"$set": settings})
        user_updated = await self.settings_get_one(documents=documents)

        return user_updated

    async def conversation_zl_get_one(self, peer_id_zl, documents):
        conversation_zls = self.db[str(documents)].find({"peer_id_zl": peer_id_zl})


        async for user in conversation_zls:
            del user["_id"]
            return user  # ujson.loads(dumps(user))

    async def conversation_zl_insert_one(self, conversation_zl, documents):

        _conversation_zl = await self.conversation_zl_get_one(peer_id_zl=conversation_zl["peer_id_zl"],
                                                              documents=documents)
        if not _conversation_zl:
            await self.db[str(documents)].insert_one(conversation_zl)

            _conversation_zl = await self.conversation_zl_get_one(peer_id_zl=conversation_zl["peer_id_zl"],
                                                                  documents=documents)

        return _conversation_zl

    async def conversation_zl_update_one(self, conversation_zl, documents):
        await self.db[str(documents)].update_one({"peer_id_zl": conversation_zl["peer_id_zl"]},
                                                 {"$set": conversation_zl})
        user_updated = await self.conversation_zl_get_one(peer_id_zl=conversation_zl["peer_id_zl"],
                                                          documents=documents)

        return user_updated


    async def peer_ids_get_all(self, documents):
        peer_ids = self.db[str(documents)].find({})

        peer_ids_list = []

        async for peer_id in peer_ids:
            peer_ids_list.append(peer_id["peer_id"])
        return peer_ids_list


    async def peer_ids_get_one(self, peer_id, documents):
        peer_ids = self.db[str(documents)].find({"peer_id": peer_id})


        async for user in peer_ids:
            del user["_id"]
            return user  # ujson.loads(dumps(user))

    async def peer_ids_insert_one(self, peer_ids, documents):

        _peer_ids = await self.peer_ids_get_one(peer_id=peer_ids["peer_id"],
                                                documents=documents)
        if not _peer_ids:
            await self.db[str(documents)].insert_one(peer_ids)

            _peer_ids = await self.peer_ids_get_one(peer_id=peer_ids["peer_id"],
                                                    documents=documents)

        return _peer_ids

    async def peer_ids_update_one(self, peer_ids, documents):
        await self.db[str(documents)].update_one({"peer_id": peer_ids["peer_id"]},
                                                 {"$set": peer_ids})
        user_updated = await self.peer_ids_get_one(peer_id=peer_ids["peer_id"],
                                                   documents=documents)

        return user_updated

    async def log_insert_one(self, log, documents):

        #_log = await self.settings_get_one(documents=documents)

        #if not _settings:

        await self.db[str(documents)].insert_one(log)

            #_settings = await self.settings_get_one(documents=documents)

        return True

    async def log_sms_count(self, user_id, current_time, time_interval, documents, type_sms=None):

        if type_sms:
            result = await self.db[str(documents)].count_documents({"user_id": user_id, "type_sms": type_sms,
                                                                    "current_time": {"$gt": current_time - time_interval}})
        else:
            result = await self.db[str(documents)].count_documents({"user_id": user_id,
                                                                    "current_time": {
                                                                        "$gt": current_time - time_interval}})

        #_log = await self.settings_get_one(documents=documents)

        #if not _settings:

        #await self.db[str(documents)].insert_one(log)

            #_settings = await self.settings_get_one(documents=documents)

        return result

    async def zawarn_get_one(self, from_id, conversation_message_id_forward, current_time, documents):
        zawarns = self.db[str(documents)].find({"from_id": from_id,
                                                "conversation_message_id_forward": conversation_message_id_forward,
                                                "current_time": current_time})

        async for zawarn in zawarns:
            del zawarn["_id"]
            return zawarn  # ujson.loads(dumps(user))

    async def zawarn_insert_one(self, zawarn, documents):
        #print(user)
        _zawarn = await self.zawarn_get_one(from_id=zawarn["from_id"],
                                            conversation_message_id_forward=zawarn["conversation_message_id_forward"],
                                            current_time=zawarn["current_time"],
                                            documents=documents)
        #print(user)
        if not _zawarn:
            # print("Error")
        #else:
            await self.db[str(documents)].insert_one(zawarn)

            _zawarn = await self.zawarn_get_one(from_id=zawarn["from_id"],
                                                conversation_message_id_forward=zawarn[
                                                    "conversation_message_id_forward"],
                                                current_time=zawarn["current_time"],
                                                documents=documents)

        return _zawarn

    async def zawarn_update_one(self, zawarn, documents):
        #_user = user
        await self.db[str(documents)].update_one(
            {
                "user_id": zawarn["user_id"],
                "conversation_message_id_forward": zawarn["conversation_message_id_forward"],
                "current_time": zawarn["current_time"]
            },
            {"$set": zawarn})
        user_updated = await self.zawarn_get_one(from_id=zawarn["from_id"],
                                                 conversation_message_id_forward=zawarn[
                                                    "conversation_message_id_forward"],
                                                 current_time=zawarn["current_time"],
                                                 documents=documents)

        return user_updated

    async def tribe_get_all(self, documents):
        users_list = []
        tribes = self.db[str(documents)].find({})

        async for tribe in tribes:
            del tribe["_id"]
            # users_list.append(ujson.loads(dumps(user)))
            users_list.append(tribe)

        return users_list

    async def tribe_get_one(self, cut, documents):
        tribes = self.db[str(documents)].find({"cut": cut})


        async for tribe in tribes:
            del tribe["_id"]
            return tribe  # ujson.loads(dumps(user))

    async def tribe_insert_one(self, tribe, documents):
        #print(user)
        _tribe = await self.tribe_get_one(cut=tribe["cut"], documents=documents)
        #print(user)
        if not _tribe:
            # print("Error")
        #else:
            await self.db[str(documents)].insert_one(tribe)

            _tribe = await self.tribe_get_one(cut=tribe["cut"], documents=documents)

        return _tribe

    async def tribe_users_count(self, cut, documents):
        result = await self.db[str(documents)].count_documents({"tribe": cut})
        return result

    async def tribe_users_get(self, cut, documents):
        users_list = []
        tribes = self.db[str(documents)].find({"tribe": cut})

        async for tribe in tribes:
            del tribe["_id"]
            # users_list.append(ujson.loads(dumps(user)))
            users_list.append(tribe)

        return users_list

    async def questions_unban_get_all(self, dj_db, documents):
        questions = self.client[dj_db][str(documents)].find({})

        questions_list = []

        async for question in questions:
            del question["_id"]
            questions_list.append(question)
        return questions_list

    async def get_log_add_leave(self, time_start, time_finish, peer_id, documents):
        chat_returned_user = await self.db[str(documents)].count_documents({"type": "chat_returned_user",
                                                                            "peer_id": peer_id,
                                                                "$and": [
                                                                    {"current_time": {"$gte": time_start}},
                                                                    {"current_time": {"$lte": time_finish}}
                                                                ]})
        chat_exit_user = await self.db[str(documents)].count_documents({"type": "chat_exit_user", "peer_id": peer_id,
                                                                "$and": [
                                                                    {"current_time": {"$gte": time_start}},
                                                                    {"current_time": {"$lte": time_finish}}
                                                                ]})
        return chat_returned_user, chat_exit_user

    async def get_log_sms_active(self, time_start, time_finish, documents):
        sms_active = await self.db[str(documents)].count_documents({"type": "sms",
                                                                "$and": [
                                                                    {"current_time": {"$gte": time_start}},
                                                                    {"current_time": {"$lte": time_finish}}
                                                                ]})
        return sms_active


    async def get_log_cmd(self, time_start, time_finish, tupe_cmd):
        sms_active = await self.db["logs"].count_documents({"type": tupe_cmd,
                                                                "$and": [
                                                                    {"current_time": {"$gte": time_start}},
                                                                    {"current_time": {"$lte": time_finish}}
                                                                ]})
        return sms_active

    #
    # async def user_delete_one(self, user: User) -> List[User]:
    #     await self.db.users.delete_one(user.dict())
    #
    #     user_deleted = await self.user_get_one(user_id=user.dict()["user_id"])
    #
    #     return user_deleted

class User:

    def __init__(self):
        self.user_id = 1
        self.name = "ХЗ"
        self.cmd = ["+rep", "-rep", "/profile"]

    @property
    def user_dict(self):
        #print(self.__dict__)
        return self.__dict__

if __name__ == "__main__":

    from motor import MotorClient
    import asyncio
    uri = 'mongodb://localhost:27017'
    client = MotorClient(uri)
    me = MongoManager(client, 123)
    loop = asyncio.get_event_loop()
    #toke = loop.run_until_complete(me.user_get_all("users"))
    us = User()
    #toke = loop.run_until_complete(me.user_insert_one(us.user_dict))
    #toke = loop.run_until_complete(me.user_get_one(1))
    toke = loop.run_until_complete(me.user_update_one(us.user_dict))
    print(toke)
