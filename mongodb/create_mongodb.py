# -*- coding: utf-8 -*-
import asyncio
from pymongo import MongoClient
import os
import traceback
import numpy as np

from api import api_url, api, photo_upload

var = "code.py"


class create_mongodb:

    def __init__(self, client, collections_django, apps_django):

        self.client = client
        self.collections_django = collections_django
        self.apps_django = apps_django
        # self.collections = collections
        # self.documents = documents
        # self.tokens = tokens
        # self.ids = ids

    def create_db(self, collections, documents, tokens, ids):
        db = self.client[f"{collections}"]
        # collection = db['tokens']
        posts = db[f"{documents}"]
        one_doc = posts.find_one()
        if one_doc != None:
            for post in posts.find():
                if post["id"] in ids:
                    # print(tokens)
                    del tokens[ids.index(post["id"])]
                    del ids[ids.index(post["id"])]

            if len(tokens) > 0:
                posts.insert_many(tokens)

        elif one_doc == None:
            result = posts.insert_many(tokens)
            # print(result)

    def get_tokens(self, collections, documents, **kwargs):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        # print(posts.find)
        if "empty" in kwargs:
            kwargs = {}
        tokens = []
        ids = []
        tokens_new = []
        for post in posts.find(kwargs):
            # print(post)
            tokens.append({"id": post["id"], "token": post["token"], "them": post["them"]})
            if "peer_id" in post:
                tokens_new.append({"id": post["id"], "token": post["token"], "them": post["them"], "name": post["name"],
                                   "peer_id": post["peer_id"]})
            else:
                tokens_new.append(
                    {"id": post["id"], "token": post["token"], "them": post["them"], "name": post["name"]})
            # tokens[post["id"]] = post["token"]
        # print(tokens)
        return tokens, tokens_new

    def update(self, collections, documents, club_id, peer_id):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po = posts.find_one({'id': club_id, 'peer_id': peer_id})
        print(po)
        if po is None:
            post = posts.find_one({'id': club_id})
            if post is not None:
                post['peer_id'] = peer_id
                posts.save(post)
                return 1
        return 0

    def get_them(self, collections, apps, id_ras):
        db = self.client[f"{collections}"]
        posts = db[f"{apps}_rassilka_them"]
        thems_id = []
        thems = []
        for post in posts.find({"rassilka_id": id_ras}):
            thems_id.append(post["topics_id"])
        posts = db[f"{apps}_topics"]
        for i in thems_id:
            thems.append(posts.find_one({'id': i})["soc"])
        # post = posts.find_one({'id':them_id})
        return thems

    def get(self, collections, apps):
        db = self.client[f"{collections}"]
        kwargs = {}
        # if "empty" in kwargs:
        # kwargs = {}
        # self.get_them(db, apps, kwargs["them"])
        posts = db[f"{apps}_rassilka"]
        # if "empty" in kwargs:
        # kwargs = {}
        thems = []
        for post in posts.find(kwargs):
            thems.append(post)

        return thems

    def get_peer_id(self, collections, documents, club_id):
        peer_id = 0
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po = posts.find_one({'id': club_id})
        if "peer_id" in po:
            peer_id = po["peer_id"]
        return peer_id

    def get_peer_id_new(self, collections, apps, club_id, id_ras):
        peer_id = 0
        f = 0
        peer_id_news = []
        db = self.client[f"{collections}"]
        posts = db[f"{apps}_rassilka_them_peer_id"]
        res_ids = posts.find({"rassilka_id": id_ras})
        posts = db[f"{apps}_conversations_ab"]
        # res_ids_ab = posts.find({})
        for i in res_ids:
            po = posts.find_one({'id': i["conversations_ab_id"]})
            peer_id_news.append(po["Conver"])
            f = 1
        if f == 0:
            posts = db[f"{apps}_groups"]
            po = posts.find_one({'id_group': club_id})
            if "peer_id_new" in po:
                peer_id = po["peer_id_new"]
                peer_id_news = peer_id.split(', ')
        return peer_id_news

    def questions_update(self, collections, documents, vopr):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        posts.remove({})
        posts.insert_many(vopr)
        posts_ab = db["questions_abitur_photo"]
        posts_ab.remove({})
        posts_ab = db["users"]
        posts_ab.remove({})
        return

    def questions_get(self, collections="bots", documents="questions"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        vopr = ""
        for post in posts.find({}):
            if len(vopr) > 1:
                vopr += f"\n{post['nom']}. {post['vopr']}"
            else:
                vopr += f"{post['nom']}. {post['vopr']}"
        return vopr

    def questions_get_one(self, number, collections="bots", documents="questions"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]

        # posts_ab = db["questions_abitur_photo"]
        #
        # posts_ab.remove({})

        po = posts.find_one({'nom': number})
        if po is not None:
            return po["otvet"]
        else:
            return ""

    async def questions_get_abitur(self, apis, v, peer_id, nap, collections="bots", documents="questions_abitur_photo"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po = posts.find_one({"nap": nap})
        if po is not None:
            return po["att"]
        else:
            files = os.listdir("generating_questions/img")
            post = ""
            # loop = asyncio.get_running_loop()
            for i in files:
                if "png" in i:
                    if nap in i:
                        res = await photo_upload(apis, v, peer_id, f"{i}", "generating_questions/img/").upload()
                        # print(res)
                        """res = await photo_upload(self.apis,
                                             self.v, self.peer_id,
                                             f"{i}",
                                             "generating_questions/img/").upload()"""
                        # print(res)
                        if len(post) > 1:
                            # post = f"{res}," + post
                            post = post + f",{res}"
                        else:
                            post += f"{res}"

            posts.insert_one({"nap": nap, "att": post})
            # posts.insert_many([{"att": post}])

            return post

    def rating(self, user_id):
        # try:
        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_users"]
        po = posts.find_one({'user_id': str(user_id)})
        if po is not None:
            return po
        return -1
        # except Exception as e:
        # print(e)

    def answer(self, number):

        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_questions"]
        po = posts.find_one({'id': int(number)})
        if po is None:
            return 0
        else:
            po_new = posts.find_one({'id': int(number) + 1})
            # print(po_new)
            if po_new is None:
                return 1
            else:
                return 2

    def users_get(self):

        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_users"]
        users = ""
        repeat = []
        for post in posts.find({}):
            if len(users) > 1:
                if post['user_id'] not in repeat and post['user_id'] != '':
                    # print(post)
                    users += f",{post['user_id']}"
                    repeat.append(post['user_id'])
            else:
                users += f"{post['user_id']}"
                repeat.append(post['user_id'])
        # print(repeat)
        return repeat

    def users_get_chek(self, user_id):
        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_users"]
        po = posts.find_one({'user_id': str(user_id)})
        if po is None:
            return 0
        else:
            return 1

    def answer_chek(self, user_id, number):

        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_users"]
        po = posts.find_one({'user_id': str(user_id)})
        user_id_mongo = po["id"]
        post = db[f"{self.apps_django}_answers"]
        ans = post.find_one({'user_id': user_id_mongo, 'question_id': int(number)})
        if ans is None:
            return (1, user_id_mongo, number)
        else:
            return (0)

    def add_user(self, user_id, f=0, flag=1, vrem=0, slov={}, collections="bots", documents="users", nap="0"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is not None:
            # posts.remove({'user_id': user_id})
            # posts.insert_one({"user_id": user_id, "flag": 0})
            po_new['flag'] = f
            if nap != "0":
                po_new['nap'] = nap
            if flag == 1:
                po_new['time'] = vrem
                po_new['slov'] = slov
            elif flag == 2:
                po_new['time'] = vrem

            posts.save(po_new)
            # posts.update({"user_id": user_id}, {"flag": 0})
            return 1
        else:
            if flag == 1:
                posts.insert_one({"user_id": user_id, "flag": f, "predm": "", "bal": 0, "time": vrem, "slov": slov,
                                  "slov_questions": {}, "slych": 0, "nap": nap})
            else:
                posts.insert_one({"user_id": user_id, "flag": f, "predm": "", "bal": 0, "nap": nap})
            return 1

    def check_user(self, user_id, collections="bots", documents="users"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is None:
            return 0
        else:
            return po_new["flag"]

    def check_user_nap(self, user_id, collections="bots", documents="users"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is None:
            return "0"
        else:
            return po_new["nap"]

    def generation_questions(self, user_id, number, collections="bots", documents="users"):
        try:
            db = self.client[f"{collections}"]
            posts = db[f"{documents}"]
            po_new = posts.find_one({'user_id': user_id})
            if po_new is not None:
                if po_new["flag"] == 4:
                    if len(po_new["slov_questions"]) == 0:
                        db_new = self.client[f"{self.collections_django}"]
                        posts_new = db_new[f"{self.apps_django}_answers_unban_new1"]
                        questions_list = list(posts_new.find({}))
                        np.random.shuffle(questions_list)
                        k = 1
                        slov_questions = {"count": 1, "count_answer": 0, "count_correct_answers": 0,
                                          "peer_id": po_new["slov"][f"{number}"]}
                        for i in questions_list:
                            question = i["question"].split('\n')
                            question_new = question[0]
                            question.pop(0)
                            np.random.shuffle(question)
                            answer = i["answer"]
                            kk = 1
                            answer_new = []
                            for j in question:
                                l = j.split(" ")
                                if answer in l[0]:
                                    slov_questions[f"{k}"] = {"answer": str(kk)}
                                l.pop(0)
                                answer_new.append(f"{kk}) {' '.join(l)}")
                                kk += 1
                            slov_questions[f"{k}"]["question"] = str(question_new) + "\n" + "\n".join(answer_new)
                            k += 1
                            if k == 9:
                                break
                        po_new["slov_questions"] = slov_questions
                        posts.save(po_new)
                        print(slov_questions)
                        return 3, slov_questions["1"]["question"]
                    else:
                        if number == po_new["slov_questions"][f"{po_new['slov_questions']['count']}"]["answer"]:
                            if int(int(po_new['slov_questions']['count']) + 1) == 8:
                                if int(int(po_new['slov_questions']["count_correct_answers"]) + 1) == 5:
                                    peer_id = po_new['slov_questions']["peer_id"]
                                    po_new["slov_questions"] = {}
                                    posts.save(po_new)
                                    return 1, peer_id
                                else:
                                    # po_new["slov_questions"] = {}
                                    posts.save(po_new)
                                    return -1, ""
                            elif int(int(po_new['slov_questions']["count_correct_answers"]) + 1) == 5:
                                peer_id = po_new['slov_questions']["peer_id"]
                                po_new["slov_questions"] = {}
                                posts.save(po_new)
                                return 1, peer_id
                            po_new['slov_questions']['count'] = str(int(int(po_new['slov_questions']['count']) + 1))
                            po_new['slov_questions']['count_correct_answers'] = str(
                                int(int(po_new['slov_questions']['count_correct_answers']) + 1))
                            posts.save(po_new)
                            return 2, po_new["slov_questions"][f"{po_new['slov_questions']['count']}"]["question"]
                        else:
                            if int(int(po_new['slov_questions']['count']) + 1) == 8:
                                # po_new["slov_questions"] = {}
                                posts.save(po_new)
                                return -1, ""
                            po_new['slov_questions']['count'] = str(int(int(po_new['slov_questions']['count']) + 1))
                            posts.save(po_new)
                            return 2, po_new["slov_questions"][f"{po_new['slov_questions']['count']}"]["question"]
        except Exception as e:
            print(traceback.format_exc())

    def unban(self, user_id, peer_id, collections="bots", documents="users"):
        try:
            db = self.client[f"{collections}"]
            posts = db[f"{peer_id}"]
            po_new = posts.find_one({'user_id': int(user_id)})
            if po_new is not None:
                if "count" in po_new["ban"]:
                    print("BAN EST")
                    po_new["ban"][str(po_new["ban"]["count"])]["status"] = False
                    print(po_new)
                    posts.save(po_new)

                post = db[f"{documents}"]
                pos_new = post.find_one({'user_id': user_id})
                pos_new['slych'] = 0
                post.save(pos_new)
                return
        except Exception as e:
            print(traceback.format_exc())

    def null_attempt(self, user_id, collections="bots", documents="users"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is not None:
            peer_id = po_new["slov_questions"]["peer_id"]
            po_new["slov_questions"] = {}
            posts.save(po_new)
            pos = db[f"{peer_id}"]
            pos_new = pos.find_one({"user_id": int(user_id)})
            if pos_new is not None:
                if "count" in pos_new["ban"]:
                    pos_new["ban"][str(pos_new["ban"]["count"])]["chance"] = 0
                    pos.save(pos_new)
        return

    def check_user_unban(self, user_id, vrem, slych, flag, collections="bots", documents="users"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is not None:
            if flag:
                po_new['time'] = vrem
                po_new['slych'] = slych
                posts.save(po_new)
                return 1
            return po_new['time'], po_new['slych']

    def edit_user(self, user_id, predm, collections="bots", documents="users"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is not None:
            po_new['predm'] = predm
            posts.save(po_new)
        return 1

    def check_predmet(self, user_id, collections="bots", documents="users"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': user_id})
        if po_new is not None:
            return po_new['predm']
        return 0

    def start_bs(self, peer_id, users, users_vse, users_adm, collections="bots"):
        try:
            db = self.client[f"{collections}"]
            posts = db[f"{peer_id}"]
            # users_new = users.copy()
            users_vse_new = users_vse.copy()
            pos = posts.find({})
            pos_d = list(pos)

            for i in pos_d:
                if i["user_id"] not in users_vse:
                    i["output"] = True
                    if "kicked" in i:
                        if not i["kicked"]:
                            i["kicked"] = False
                else:
                    i["output"] = False
                    if "kicked" in i:
                        if not i["kicked"]:
                            i["kicked"] = False
                    # del users[i["user_id"]]
                    users_vse_new.remove(i["user_id"])
                if i["user_id"] in users_adm:
                    i["admin"] = True
                else:
                    i["admin"] = False
            for i in users_vse_new:
                pos_d.append(
                    {"user_id": i, "admin": users[i]["admin"], "output": False, "kicked": False, "moder": {}, "ban": {},
                     "warn": {}, "mute": {}})

            posts.remove({})
            posts.insert_many(pos_d)
            posts = db[f"settings"]
            po = posts.find_one({"perv": 1})
            if po is None:
                posts.insert_one({"perv": 1, "peer_ids": f"{peer_id}"})
            else:
                sp = str(po["peer_ids"]).split(", ")
                if str(peer_id) not in sp:
                    sp.append(str(peer_id))
                    po["peer_ids"] = ", ".join(sp)
                    posts.save(po)
            # db = self.client[f"{collections}"]
            # posts = db[f"{peer_id}"]
            # users_new = users.copy()
            # for i in users:
            #     po = posts.find_one({'user_id': i["user_id"]})
            #     if po is not None:
            #         if "output" in po:
            #             if po["output"]:
            #                 po["output"] = False
            #                 po.save(po)
            #         users_new.remove(i)
            #     else:
            #         i["ban"] = {}
            #         i["warn"] = {"count": 0}
            #         i["mute"] = {}
            #         i["output"] = False
            # pos = posts.find({})
            # for i in pos:
            #     if i["user_id"] not in users_vse:
            #         po = posts.find_one({'user_id': i["user_id"]})
            #         po["output"] = True
            #         po.save(po)
            # #pos.save(pos)
            # posts.insert_many(users_new)
        except Exception as e:
            print(traceback.format_exc())

    async def admin_check(self, user_id, peer_id, f=0, collections="bots"):
        try:
            db = self.client[f"{collections}"]
            if f == 1:
                posts_ab = db[f"conversations"]
                pos_new = posts_ab.find_one({"peer_id_zl": int(peer_id)})
                if pos_new is not None:
                    peer_id_ab = pos_new["peer_id_ab"]
                    posts = db[f"{peer_id_ab}"]
            elif f == 0:
                posts = db[f"{peer_id}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is not None:
                return pos["admin"]
            else:
                return False
        except Exception as e:
            print(traceback.format_exc())

    async def ban_check(self, user_id, peer_id, cause, vrem, start_time, user_admin, collections="bots"):
        try:
            db = self.client[f"{collections}"]
            posts = db[f"{peer_id}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is not None:
                if not pos["ban"]:
                    pos["ban"]["1"] = {}
                    pos["ban"]["1"]["status"] = True
                    pos["ban"]["1"]["time"] = vrem
                    pos["ban"]["1"]["cause"] = cause
                    pos["ban"]["1"]["start_time"] = start_time
                    pos["ban"]["1"]["user_admin"] = user_admin
                    pos["ban"]["1"]["chance"] = 1
                    pos["ban"]["count"] = 1
                    posts.save(pos)
                    return 1
                else:
                    if pos["ban"][str(pos["ban"]["count"])]["status"] == True:
                        return 0
                    else:
                        pos["ban"][str(pos["ban"]["count"] + 1)] = {}
                        pos["ban"][str(pos["ban"]["count"] + 1)]["status"] = True
                        pos["ban"][str(pos["ban"]["count"] + 1)]["time"] = vrem
                        pos["ban"][str(pos["ban"]["count"] + 1)]["cause"] = cause
                        pos["ban"][str(pos["ban"]["count"] + 1)]["start_time"] = start_time
                        pos["ban"][str(pos["ban"]["count"] + 1)]["user_admin"] = user_admin
                        pos["ban"][str(pos["ban"]["count"] + 1)]["chance"] = 1
                        pos["ban"]["count"] += 1
                        posts.save(pos)
                        return pos["ban"]["count"]
            else:
                posts.insert_one(
                    {"user_id": int(user_id), "admin": False, "output": False, "kicked": False, "moder": {},
                     "ban": {
                         "1": {
                             "status": True,
                             "time": vrem,
                             "cause": cause,
                             "start_time": start_time,
                             "user_admin": user_admin,
                             "chance": 1
                         },
                         "count": 1},
                     "warn": {},
                     "mute": {}})
                return 1
        except Exception as e:
            print(traceback.format_exc())

    async def add_warn(self, user_id, peer_id, cause, vrem, start_time, user_admin, collections="bots"):
        try:
            db = self.client[f"{collections}"]
            posts = db[f"{peer_id}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is not None:
                if not pos["warn"]:
                    pos["warn"]["count"] = 1
                    pos["warn"]["count_old"] = 2
                    pos["warn"]["1"] = {}
                    pos["warn"]["1"]["status"] = True
                    pos["warn"]["1"]["time"] = vrem
                    pos["warn"]["1"]["cause"] = cause
                    pos["warn"]["1"]["start_time"] = start_time
                    pos["warn"]["1"]["user_admin"] = user_admin
                    posts.save(pos)
                    return 1, 1
                else:
                    if pos["warn"]["count"] == 2:
                        pos["warn"][str(pos["warn"]["count_old"])] = {}
                        pos["warn"][str(pos["warn"]["count_old"])]["time"] = vrem
                        pos["warn"][str(pos["warn"]["count_old"])]["cause"] = cause
                        pos["warn"][str(pos["warn"]["count_old"])]["status"] = True
                        pos["warn"][str(pos["warn"]["count_old"])]["start_time"] = start_time
                        pos["warn"][str(pos["warn"]["count_old"])]["user_admin"] = user_admin
                        pos["warn"]["count_old"] += 1
                        pos["warn"]["count"] = 0
                        ban = 1
                        if "count" in pos["ban"]:
                            ban = pos["ban"]["count"]
                        # pos["ban"]["status"] = True
                        # pos["ban"]["time"] = vrem
                        # pos["ban"]["cause"] = cause
                        posts.save(pos)
                        #res = await self.ban_check(user_id, peer_id, cause, vrem, start_time, user_admin)
                        return 3, pos["warn"]["count_old"] - 1, ban
                    else:
                        pos["warn"][str(pos["warn"]["count_old"])] = {}
                        pos["warn"][str(pos["warn"]["count_old"])]["time"] = vrem
                        pos["warn"][str(pos["warn"]["count_old"])]["cause"] = cause
                        pos["warn"][str(pos["warn"]["count_old"])]["status"] = True
                        pos["warn"][str(pos["warn"]["count_old"])]["start_time"] = start_time
                        pos["warn"][str(pos["warn"]["count_old"])]["user_admin"] = user_admin
                        pos["warn"]["count"] += 1
                        pos["warn"]["count_old"] += 1
                        posts.save(pos)
                        return pos["warn"]["count"], pos["warn"]["count_old"] - 1

            return -1
        except Exception as e:
            print(traceback.format_exc())

    async def ban_remove(self, user_id, peer_id, collections="bots"):
        db = self.client[f"{collections}"]
        posts_ab = db[f"conversations"]
        pos_new = posts_ab.find_one({"peer_id_zl": int(peer_id)})
        if pos_new is not None:
            peer_id_ab = pos_new["peer_id_ab"]
            posts = db[f"{peer_id_ab}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is not None:
                pos["ban"][str(pos["ban"]["count"])]["status"] = False
                pos["output"] = False
                pos["kicked"] = False
                posts.save(pos)

    async def add_user_bs(self, user_id, peer_id, f=0, collections="bots"):
        """
        Добавляет нового пользователя в бд при переходе по ссылке или по добавлении в беседу
        :param user_id: Id пользователя, которого необходимо добавить
        :param peer_id: Id беседы Злюки
        :param collections:
        :return:
        """
        db = self.client[f"{collections}"]
        posts_ab = db[f"conversations"]
        pos_new = posts_ab.find_one({"peer_id_zl": int(peer_id)})
        if pos_new is not None:
            peer_id_ab = pos_new["peer_id_ab"]
            posts = db[f"{peer_id_ab}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is None:
                posts.insert_one(
                    {"user_id": int(user_id), "admin": False, "output": False, "kicked": False, "moder": {}, "ban": {},
                     "warn": {},
                     "mute": {}})
            else:
                if f == 1:
                    if "count" in pos["ban"]:
                        # print(pos["ban"][str(pos["ban"]["count"])])
                        if pos["ban"][str(pos["ban"]["count"])]["status"]:
                            return 2
                else:
                    pos["output"] = False
                    pos["kicked"] = False
                    posts.save(pos)
            return 1

    async def remove_user_bs(self, user_id, peer_id, f=0, collections="bots"):

        try:
            db = self.client[f"{collections}"]
            posts_ab = db[f"conversations"]
            pos_new = posts_ab.find_one({"peer_id_zl": int(peer_id)})
            if pos_new is not None:
                peer_id_ab = pos_new["peer_id_ab"]
                posts = db[f"{peer_id_ab}"]
                pos = posts.find_one({"user_id": int(user_id)})
                if pos is None:
                    if f == 0:
                        posts.insert_one(
                            {"user_id": int(user_id), "admin": False, "output": True, "kicked": False, "moder": {},
                             "ban": {},
                             "warn": {}, "mute": {}})
                    else:
                        posts.insert_one(
                            {"user_id": int(user_id), "admin": False, "output": False, "kicked": True, "moder": {},
                             "ban": {},
                             "warn": {}, "mute": {}})
                else:
                    if f == 0:
                        pos["output"] = True
                    else:
                        pos["kicked"] = True
                    posts.save(pos)
                return 1
        except Exception as e:
            print(traceback.format_exc())

    async def remove_ban_warn(self, vrem, collections="bots"):
        try:
            print(vrem)
            db = self.client[f"{collections}"]
            posts_peer_ids = db[f"settings"]
            pos_new = posts_peer_ids.find_one({"perv": 1})
            peer_ids = pos_new["peer_ids"].split(", ")
            # print(peer_ids)
            for i in peer_ids:
                posts = db[f"{i}"]
                pos = posts.find({})
                for j in pos:
                    if "count" in j["ban"]:
                        if j["ban"][str(j["ban"]["count"])]["status"]:
                            if int(j["ban"][str(j["ban"]["count"])]["time"]) <= int(vrem):
                                j["ban"][str(j["ban"]["count"])]["status"] = False
                                posts.save(j)
                    if "count" in j["warn"]:
                        if j['warn']['count'] > 0:
                            for g in range(1, 3):
                                if f'{j["warn"]["count_old"] - g}' in j['warn']:
                                    if j['warn'][f'{j["warn"]["count_old"] - g}']["status"]:
                                        if int(j['warn'][f'{j["warn"]["count_old"] - g}']["time"]) <= int(vrem):
                                            j["warn"][str(j["warn"]["count_old"] - g)]["status"] = False
                                            j["warn"]["count"] = j["warn"]["count"] - 1
                                            # j["warn"]["count_old"] = j["warn"]["count_old"] - 1
                                            posts.save(j)
            return 1
        except Exception as e:
            print(traceback.format_exc())

    async def add_besed_zl(self, peer_id_ab, peer_id_zl, collections="bots", documents="conversations"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        pos = posts.find_one({"peer_id_ab": int(peer_id_ab)})
        if pos is None:
            posts.insert_one({"peer_id_ab": int(peer_id_ab), "peer_id_zl": int(peer_id_zl)})
            return 1
        else:
            return 0

    async def get_settings(self, collections="bots", documents="settings"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        pos = posts.find_one({"perv": 1})
        if pos is not None:
            return pos["peer_ids"].split(", ")

    async def ban_chek(self, user_id, collections="bots"):
        try:
            slov = {"peer_ids": []}
            db = self.client[f"{collections}"]
            posts_peer_ids = db[f"settings"]
            pos_new = posts_peer_ids.find_one({"perv": 1})
            peer_ids = pos_new["peer_ids"].split(", ")
            # print(peer_ids)
            k = 1
            for i in peer_ids:
                posts = db[f"{i}"]
                pos = posts.find_one({"user_id": int(user_id)})
                if pos is not None:
                    if "count" in pos["ban"]:
                        if pos["ban"][str(pos["ban"]["count"])]["status"] and pos["ban"][str(pos["ban"]["count"])]["chance"] > 0:
                            slov["peer_ids"].append(i)
                            slov[f"{i}"] = {"count": pos["ban"]["count"], "user_id": int(user_id)}
                            slov[f"{k}"] = f"{i}"
                            k += 1
            return slov

        except Exception as e:
            print(traceback.format_exc())
            return slov

    async def add_users_zawarn(self, user_id, vrem, peer_id, collections="bots"):
        """
        Добавляет пользователя при подозрении на мат
        :param user_id: ID пользователя
        :param vrem: время отпрвки сообщения с матом
        :param peer_id: ID беседы
        :param collections:
        :return: 1
        """
        db = self.client[f"{collections}"]
        posts = db[f"users_warn"]
        posts.insert_one({"user_id": user_id, "peer_id": peer_id, "vrem": vrem, "status": False})
        return 1

    async def chek_zawarn(self, user_id, vrem, collections="bots"):
        """
        Добавляет пользователя при подозрении на мат
        :param user_id: ID пользователя
        :param vrem: время отпрвки сообщения с матом
        :param peer_id: ID беседы
        :param collections:
        :return: 1
        """
        db = self.client[f"{collections}"]
        posts = db[f"users_warn"]
        pos = posts.find_one({"user_id": int(user_id), "vrem": int(vrem)})
        if pos is not None:
            if not pos["status"]:
                pos["status"] = True
                posts.save(pos)
                return 1, pos["peer_id"]
            else:
                return 0, ""

        return -1, ""

    async def user_info(self, user_id, peer_id, collections="bots"):

        db = self.client[f"{collections}"]
        posts = db[f"{peer_id}"]
        pos = posts.find_one({"user_id": int(user_id)})
        if pos is not None:
            return pos
        return False

    async def profile_users_add(self, user_id, achievements="0", scores=0, sms=0, reputation_plus=0, reputation_minus=0,
                                f=0,
                                collections="bots", documents="profile_users"):
        db = self.client[f"{collections}"]
        posts_peer_ids = db[f"settings"]
        pos_new = posts_peer_ids.find_one({"perv": 1})
        peer_ids = pos_new["peer_ids"].split(", ")
        flag = False
        for i in peer_ids:
            posts = db[f"{i}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is not None:
                flag = True
                break
        if flag:
            posts = db[f"{documents}"]
            pos = posts.find_one({"user_id": int(user_id)})
            if pos is None:
                if achievements != "0":
                    posts.insert_one({"user_id": int(user_id), "achievements":
                        {
                            "1":
                                {
                                    "status": True,
                                    "scores": float(scores),
                                    "name": achievements
                                }
                        },
                                      "count_achievements": 1, "scores": 0 + float(scores), "sms": sms,
                                      "reputation_plus":
                                          {
                                              "1": {
                                                  "status": True,
                                                  "vrem": reputation_plus
                                              },
                                              "2": {
                                                  "status": True,
                                                  "vrem": reputation_plus
                                              },
                                              "3": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                              "4": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                              "5": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                              "6": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                          },
                                      "count_plus": 0,
                                      "reputation_minus":
                                          {
                                              "1": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "2": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "3": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "4": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "5": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "6": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                          },
                                      "count_minus": 0
                                      })
                elif achievements == "0":
                    posts.insert_one({"user_id": int(user_id), "achievements": {},
                                      "count_achievements": 1, "scores": 0 + float(scores), "sms": sms,
                                      "reputation_plus":
                                          {
                                              "1": {
                                                  "status": True,
                                                  "vrem": reputation_plus
                                              },
                                              "2": {
                                                  "status": True,
                                                  "vrem": reputation_plus
                                              },
                                              "3": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                              "4": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                              "5": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                              "6": {
                                                  "status": False,
                                                  "vrem": reputation_plus
                                              },
                                          },
                                      "count_plus": 0,
                                      "reputation_minus":
                                          {
                                              "1": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "2": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "3": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "4": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "5": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                              "6": {
                                                  "status": False,
                                                  "vrem": reputation_minus
                                              },
                                          },
                                      "count_minus": 0
                                      })

                if sms != 0:
                    return 1
                return [achievements], 0 + round(float(scores), 3), 1

            else:
                if reputation_plus != 0:
                    if "reputation_plus" not in pos:
                        if f == 1:
                            return True
                        pos["reputation_plus"] = {}
                        pos["reputation_plus"]["1"] = {}
                        pos["reputation_plus"]["2"] = {}
                        pos["reputation_plus"]["3"] = {}
                        pos["reputation_plus"]["4"] = {}
                        pos["reputation_plus"]["5"] = {}
                        pos["reputation_plus"]["6"] = {}
                        pos["reputation_plus"]["1"] = {"status": True, "vrem": reputation_plus + 86400}
                        pos["reputation_plus"]["2"] = {"status": True, "vrem": reputation_plus}
                        if pos["scores"] > 35:
                            pos["reputation_plus"]["3"] = {"status": True, "vrem": reputation_plus}
                        else:
                            pos["reputation_plus"]["3"] = {"status": False, "vrem": reputation_plus}
                        if pos["scores"] > 45:
                            pos["reputation_plus"]["4"] = {"status": True, "vrem": reputation_plus}
                        else:
                            pos["reputation_plus"]["4"] = {"status": False, "vrem": reputation_plus}
                        if pos["scores"] > 50:
                            pos["reputation_plus"]["5"] = {"status": True, "vrem": reputation_plus}
                        else:
                            pos["reputation_plus"]["5"] = {"status": False, "vrem": reputation_plus}
                        if pos["scores"] > 60:
                            pos["reputation_plus"]["6"] = {"status": True, "vrem": reputation_plus}
                        else:
                            pos["reputation_plus"]["6"] = {"status": False, "vrem": reputation_plus}
                        #pos["reputation_plus"]["count"] = 2
                        pos["count_plus"] = 1
                        kol_c = pos["count_plus"]
                        posts.save(pos)
                        return kol_c
                    else:
                        r_3 = True
                        r_4 = True
                        r_5 = True
                        r_6 = True
                        if pos["scores"] > 40:
                            pos["reputation_plus"]["3"]["status"] = True
                            r_3 = False
                        if pos["scores"] > 45:
                            pos["reputation_plus"]["4"]["status"] = True
                            r_4 = False

                        if pos["scores"] > 50:
                            if "5" not in pos["reputation_plus"]:
                                pos["reputation_plus"]["5"] = {"status": True, "vrem": reputation_plus}
                            else:
                                pos["reputation_plus"]["5"]["status"] = True
                            r_5 = False

                        if pos["scores"] > 60:
                            if "6" not in pos["reputation_plus"]:
                                pos["reputation_plus"]["6"] = {"status": True, "vrem": reputation_plus}
                            else:
                                pos["reputation_plus"]["6"]["status"] = True
                            r_6 = False

                        if r_3:
                            pos["reputation_plus"]["3"]["status"] = False
                        if r_4:
                            pos["reputation_plus"]["4"]["status"] = False

                        if r_5:
                            if "5" not in pos["reputation_plus"]:
                                pos["reputation_plus"]["5"] = {"status": False, "vrem": reputation_plus}
                            else:
                                pos["reputation_plus"]["5"]["status"] = False

                        if r_6:
                            if "6" not in pos["reputation_plus"]:
                                pos["reputation_plus"]["5"] = {"status": False, "vrem": reputation_plus}
                            else:
                                pos["reputation_plus"]["6"]["status"] = False

                        for i in pos["reputation_plus"]:
                            if pos["reputation_plus"][str(i)]["status"]:
                                if reputation_plus >= pos["reputation_plus"][str(i)]["vrem"]:
                                    if f == 1:
                                        return True
                                    if f == 2:
                                        posts.save(pos)
                                        return True
                                    pos["reputation_plus"][str(i)]["vrem"] = reputation_plus + 86400
                                    #pos["reputation_plus"]["count"] = int(i) + 1
                                    pos["count_plus"] += 1
                                    kol_c = pos["count_plus"]
                                    posts.save(pos)
                                    return kol_c
                        posts.save(pos)
                        return False

                if reputation_minus != 0:
                    if pos["scores"] < 30:
                        return False
                    if "reputation_minus" not in pos:
                        if f == 1:
                            return True
                        pos["reputation_minus"] = {}
                        pos["reputation_minus"]["1"] = {}
                        pos["reputation_minus"]["2"] = {}
                        pos["reputation_minus"]["3"] = {}
                        pos["reputation_minus"]["4"] = {}
                        pos["reputation_minus"]["1"] = {"status": True, "vrem": reputation_minus + 86400}
                        pos["reputation_minus"]["2"] = {"status": True, "vrem": reputation_minus}
                        if pos["scores"] > 40:
                            pos["reputation_minus"]["3"] = {"status": True, "vrem": reputation_minus}
                        else:
                            pos["reputation_minus"]["3"] = {"status": False, "vrem": reputation_minus}
                        if pos["scores"] > 50:
                            pos["reputation_minus"]["4"] = {"status": True, "vrem": reputation_minus}
                        else:
                            pos["reputation_minus"]["4"] = {"status": False, "vrem": reputation_minus}
                        if pos["scores"] > 55:
                            pos["reputation_minus"]["5"] = {"status": True, "vrem": reputation_minus}
                        else:
                            pos["reputation_minus"]["5"] = {"status": False, "vrem": reputation_minus}
                        if pos["scores"] > 65:
                            pos["reputation_minus"]["6"] = {"status": True, "vrem": reputation_minus}
                        else:
                            pos["reputation_minus"]["6"] = {"status": False, "vrem": reputation_minus}
                        #pos["reputation_minus"]["count"] = 2
                        pos["count_minus"] = 1
                        kol_c = pos["count_minus"]
                        posts.save(pos)
                        return kol_c
                    else:
                        if pos["scores"] < 30 and f != 2:
                            pos["reputation_minus"]["1"]["status"] = False
                            pos["reputation_minus"]["2"]["status"] = False
                            posts.save(pos)
                            return False
                        if pos["scores"] < 30:
                            pos["reputation_minus"]["1"]["status"] = False
                            pos["reputation_minus"]["2"]["status"] = False
                        r_3 = True
                        r_4 = True
                        r_5 = True
                        r_6 = True
                        if pos["scores"] > 40:
                            pos["reputation_minus"]["3"]["status"] = True
                            r_3 = False
                        if pos["scores"] > 50:
                            pos["reputation_minus"]["4"]["status"] = True
                            r_4 = False

                        if pos["scores"] > 55:
                            if "5" not in pos["reputation_minus"]:
                                pos["reputation_minus"]["5"] = {"status": True, "vrem": reputation_minus}
                            else:
                                pos["reputation_minus"]["5"]["status"] = True
                            r_5 = False

                        if pos["scores"] > 65:
                            if "6" not in pos["reputation_minus"]:
                                pos["reputation_minus"]["6"] = {"status": True, "vrem": reputation_minus}
                            else:
                                pos["reputation_minus"]["6"]["status"] = True
                            r_6 = False

                        if r_3:
                            pos["reputation_minus"]["3"]["status"] = False
                        if r_4:
                            pos["reputation_minus"]["4"]["status"] = False

                        if r_5:
                            if "5" not in pos["reputation_minus"]:
                                pos["reputation_minus"]["5"] = {"status": False, "vrem": reputation_minus}
                            else:
                                pos["reputation_minus"]["5"]["status"] = False

                        if r_6:
                            if "6" not in pos["reputation_minus"]:
                                pos["reputation_minus"]["5"] = {"status": False, "vrem": reputation_minus}
                            else:
                                pos["reputation_minus"]["6"]["status"] = False

                        for i in pos["reputation_minus"]:
                            if pos["reputation_minus"][str(i)]["status"]:
                                if reputation_minus >= pos["reputation_minus"][str(i)]["vrem"]:
                                    if f == 1:
                                        return True
                                    if f == 2:
                                        posts.save(pos)
                                        return True
                                    pos["reputation_minus"][str(i)]["vrem"] = reputation_minus + 86400
                                    #pos["reputation_minus"]["count"] = 2
                                    pos["count_minus"] += 1
                                    kol_c = pos["count_minus"]
                                    posts.save(pos)
                                    return kol_c
                        posts.save(pos)
                        return False


                if sms != 0:
                    pos["sms"] += sms
                    kol_sms = pos["sms"]
                    posts.save(pos)
                    return kol_sms
                if achievements == "0" and scores == 0 and sms == 0 and reputation_plus == 0 and reputation_minus == 0:
                    ach = []
                    if len(pos["achievements"]) > 0:
                        for i in pos["achievements"]:
                            if pos["achievements"][i]["status"]:
                                ach.append(f'{pos["achievements"][i]["name"]} — {pos["achievements"][i]["scores"]}')

                        return ach, round(pos["scores"], 3), pos["sms"],
                    else:
                        return [achievements], round(pos["scores"], 3), pos["sms"]

                elif achievements != "0":
                    flag_new = True
                    for i in pos["achievements"]:
                        if pos["achievements"][i]["name"] == achievements:
                            flag_new = False

                    if flag_new:
                        pos["achievements"][str(pos["count_achievements"] + 1)] = {}
                        pos["achievements"][str(pos["count_achievements"] + 1)]["status"] = True
                        pos["achievements"][str(pos["count_achievements"] + 1)]["scores"] = scores
                        pos["achievements"][str(pos["count_achievements"] + 1)]["name"] = achievements
                        pos["count_achievements"] += 1
                    pos["scores"] += scores
                    pos["sms"] += sms
                    scor = pos["scores"]
                    posts.save(pos)
                elif achievements == "0":
                    pos["sms"] += sms
                    pos["scores"] += scores
                    scor = pos["scores"]
                    posts.save(pos)

                return [achievements], 0 + round(float(scor), 3)
        else:
            return False

    async def profile_users_check(self, user_id, vrem, collections="bots", documents="profile_users"):

        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        pos = posts.find_one({"user_id": int(user_id)})
        if pos is not None:
            slov = {"count_plus": 0, "count_minus": 0, "count_plus_available": 0, "count_minus_available": 0, "plus": {},
                    "minus": {}}
            for i in pos["reputation_plus"]:
                if pos["reputation_plus"][str(i)]["status"]:
                    slov["count_plus"] += 1
                    if vrem >= pos["reputation_plus"][str(i)]["vrem"]:
                        slov["count_plus_available"] += 1
                    else:
                        slov["plus"][f"{i}"] = pos["reputation_plus"][str(i)]["vrem"]
            if "reputation_minus" in pos:
                for i in pos["reputation_minus"]:
                    if pos["reputation_minus"][str(i)]["status"]:
                        slov["count_minus"] += 1
                        if vrem >= pos["reputation_minus"][str(i)]["vrem"]:
                            slov["count_minus_available"] += 1
                        else:
                            slov["minus"][f"{i}"] = pos["reputation_minus"][str(i)]["vrem"]
            return slov

    #async def profile_users_chek_(self, reputation, collections="bots", documents="profile_users"):


        # pos = posts.find_one({"user_id": int(user_id)})
        # if pos is None:

    async def globan_add(self, user_id, vrem, adm_id, cause, collections="bots", documents="globan"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': int(user_id)})
        if po_new is None:
            posts.insert_one({"user_id": int(user_id), "status": True, "cause": cause, "vrem": vrem, "admin_id": adm_id})
            posts_peer_ids = db[f"settings"]
            pos_new = posts_peer_ids.find_one({"perv": 1})
            peer_ids = pos_new["peer_ids"].split(", ")
            return 1, peer_ids
        else:
            if po_new["status"]:
                posts_peer_ids = db[f"settings"]
                pos_new = posts_peer_ids.find_one({"perv": 1})
                peer_ids = pos_new["peer_ids"].split(", ")
                return 2, peer_ids
            else:
                po_new["status"] = True
                po_new["vrem"] = vrem
                po_new["admin_id"] = adm_id
                po_new["cause"] = cause
                posts.save(po_new)
                posts_peer_ids = db[f"settings"]
                pos_new = posts_peer_ids.find_one({"perv": 1})
                peer_ids = pos_new["peer_ids"].split(", ")
                return 1, peer_ids

    async def globan_chek(self, user_id, collections="bots", documents="globan"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': int(user_id)})
        if po_new is not None:
            return po_new["status"]
        else:
            return False

    async def admin_answer_check(self, user_id, collections="bots", documents="admin_answer"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': int(user_id)})
        if po_new is None:
            return 1
        else:
            return po_new["count"] + 1

    async def admin_answer_add(self, user_id, text, msg_id, conversation_message_ids, msg_id_forwarded, vrem, collections="bots", documents="admin_answer"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': int(user_id)})
        if po_new is None:
            posts.insert_one({"user_id": int(user_id),
                              "answer":
                                  {
                                      "1":
                                          {
                                              "status": False,
                                              "msg_id": msg_id,
                                              "conversation_message_ids": conversation_message_ids,
                                              "text": text,
                                              "date": vrem,
                                              "date_answer": 0,
                                              "admin_id": 0,
                                              "msg_id_forwarded": msg_id_forwarded,
                                              "answer": ""
                                          }
                                  },
                              "count": 1
                              })
            return 1
        else:
            po_new["answer"][str(po_new["count"] + 1)] =\
                {
                    "status": False,
                    "msg_id": msg_id,
                    "conversation_message_ids": conversation_message_ids,
                    "text": text,
                    "date": vrem,
                    "date_answer": 0,
                    "admin_id": 0,
                    "msg_id_forwarded": msg_id_forwarded,
                    "answer": ""
                }
            po_new["count"] += 1
            count = po_new["count"]
            posts.save(po_new)
            return count

    async def admin_answer_otv(self, user_id=0, admin_id=0, answer=0, count_id=0, vrem=0, f=0, collections="bots",
                               documents="admin_answer"):
        db = self.client[f"{collections}"]

        if f == 1:
            post = db[f"admin_answer_id"]
            po_n = post.find_one({'user_id': int(admin_id)})
            if po_n is not None:
                user_id = po_n["priv_id"]
                count_id = po_n["count"]
                po_n["status"] = False
                post.save(po_n)

        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': int(user_id)})
        if po_new is not None:
            if not po_new["answer"][str(count_id)]["status"]:
                flag = False
                slov_new = {}
                count_old = 0
                if f == 1:
                    po_new["answer"][str(count_id)]["status"] = True
                    po_new["answer"][str(count_id)]["date_answer"] = vrem
                    po_new["answer"][str(count_id)]["admin_id"] = admin_id
                    po_new["answer"][str(count_id)]["answer"] = answer
                elif f == 0:
                    post = db[f"admin_answer_id"]
                    po_n = post.find_one({'user_id': int(admin_id)})
                    if po_n is None:
                        post.insert_one({"user_id": int(admin_id), "priv_id": int(user_id), "status": True,
                                         "count": int(count_id)})
                    else:
                        if po_n["status"]:
                            flag = True
                            slov_new = po_new["answer"][str(po_n["count"])]["msg_id_forwarded"]
                            count_old = po_n["count"]
                        po_n["priv_id"] = int(user_id)
                        po_n["status"] = True
                        po_n["count"] = int(count_id)
                        post.save(po_n)


                slov = po_new["answer"][str(count_id)]["msg_id_forwarded"]
                conversation_message_ids = po_new["answer"][str(count_id)]["conversation_message_ids"]
                msg_id = po_new["answer"][str(count_id)]["msg_id"]

                posts.save(po_new)
                return flag, slov, msg_id, conversation_message_ids, slov_new, count_old, user_id
            else:
                return False

    async def admin_answer_id_check(self, user_id, collections="bots", documents="admin_answer_id"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po_new = posts.find_one({'user_id': int(user_id)})
        if po_new is not None:
            return po_new["status"]
        else:
            return False
