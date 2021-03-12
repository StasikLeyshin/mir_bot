# -*- coding: utf-8 -*-
import asyncio
from pymongo import MongoClient

class create_mongodb:
    
    def __init__(self, client, collections_django, apps_django):
        
        self.client = client
        self.collections_django = collections_django
        self.apps_django = apps_django
        #self.collections = collections
        #self.documents = documents
        #self.tokens = tokens
        #self.ids = ids

    
    
    def create_db(self, collections, documents, tokens, ids):
        db = self.client[f"{collections}"]
        #collection = db['tokens']
        posts = db[f"{documents}"]
        one_doc = posts.find_one()
        if one_doc != None:
            for post in posts.find():
                if post["id"] in ids:
                    #print(tokens)
                    del tokens[ids.index(post["id"])]
                    del ids[ids.index(post["id"])]

            if len(tokens) > 0:
                posts.insert_many(tokens)
        
        elif one_doc == None:
            result = posts.insert_many(tokens)
            #print(result)

    def get_tokens(self, collections, documents, **kwargs):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        #print(posts.find)
        if "empty" in kwargs:
            kwargs = {}
        tokens = []
        ids = []
        tokens_new = []
        for post in posts.find(kwargs):
            #print(post)
            tokens.append({"id": post["id"], "token": post["token"], "them": post["them"]})
            if "peer_id" in post:
                tokens_new.append({"id": post["id"], "token": post["token"], "them": post["them"], "name": post["name"],
                                   "peer_id": post["peer_id"]})
            else:
                tokens_new.append({"id": post["id"], "token": post["token"], "them": post["them"], "name": post["name"]})
            #tokens[post["id"]] = post["token"]
        #print(tokens)
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
        #post = posts.find_one({'id':them_id})
        return thems




    def get(self, collections, apps):
        db = self.client[f"{collections}"]
        kwargs = {}
        #if "empty" in kwargs:
            #kwargs = {}
        #self.get_them(db, apps, kwargs["them"])
        posts = db[f"{apps}_rassilka"]
        #if "empty" in kwargs:
            #kwargs = {}
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

    def get_peer_id_new(self, collections, apps, club_id):
        peer_id = 0
        db = self.client[f"{collections}"]
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
        po = posts.find_one({'nom': number})
        if po is not None:
            return po["otvet"]
        else:
            return ""

    def rating(self, user_id):
        #try:
        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_users"]
        po = posts.find_one({'user_id': str(user_id)})
        if po is not None:
            return po
        return -1
        #except Exception as e:
            #print(e)


    def answer(self, number):

        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_questions"]
        po = posts.find_one({'id': int(number)})
        if po is None:
            return 0
        else:
            po_new = posts.find_one({'id': int(number) + 1})
            #print(po_new)
            if po_new is None:
                return 1
            else:
                return 2

    def users_get(self):

        db = self.client[f"{self.collections_django}"]
        posts = db[f"{self.apps_django}_users"]
        users = ""
        for post in posts.find({}):
            if len(users) > 1:
                users += f",{post['user_id']}"
            else:
                users += f"{post['user_id']}"
        return users

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