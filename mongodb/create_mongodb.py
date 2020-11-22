# -*- coding: utf-8 -*-
import asyncio
from pymongo import MongoClient

class create_mongodb:
    
    def __init__(self, client):
        
        self.client = client
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
        for post in posts.find(kwargs):
            #print(post)
            tokens.append({"id": post["id"], "token": post["token"], "them": post["them"]})
            #tokens[post["id"]] = post["token"]
        #print(tokens)
        return tokens

    def update(self, collections, documents, club_id, peer_id):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        po = posts.find_one({'peer_id': peer_id})
        if po is None:
            post = posts.find_one({'id': club_id})
            if post is not None:
                post['peer_id'] = peer_id
                posts.save(post)
                return 1
        return 0

    def get_them(self, db, apps, them):
        posts = db[f"{apps}_topics"]
        post = posts.find_one({'them':"1"})




    def get(self, collections, apps, **kwargs):
        db = self.client[f"{collections}"]
        if "empty" in kwargs:
            kwargs = {}
        self.get_them(db, apps, kwargs["them"])
        posts = db[f"{apps}_rassilka"]
        if "empty" in kwargs:
            kwargs = {}
        thems = []
        for post in posts.find(kwargs):
            thems.append(post)

        return thems


