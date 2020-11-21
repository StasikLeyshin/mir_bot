# -*- coding: utf-8 -*-
import asyncio
from pymongo import MongoClient

class create_mongodb:
    
    def __init__(self, client, collections, documents):
        
        self.client = client
        self.collections = collections
        self.documents = documents
        #self.tokens = tokens
        #self.ids = ids

    
    
    def create_db(self, tokens, ids):
        
        #client = MongoClient(self.host, self.port)
        db = self.client[f"{self.collections}"]
        #collection = db['tokens']
        posts = db[f"{self.documents}"]
        one_doc = posts.find_one()
        #posts.find_one({"": "Eliot"})
        tokens_new = []
        if one_doc != None:
            #print(posts.find())
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

    def get_tokens(self, **kwargs):
        db = self.client[f"{self.collections}"]
        posts = db[f"{self.documents}"]
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

    def update(self, club_id, peer_id):
        db = self.client[f"{self.collections}"]
        posts = db[f"{self.documents}"]
        #posts.update({'_id': club_id}, {'$set': {'them.$': 'united+states'}}, upsert=True)
        #posts.update({'_id':mongo_id}, {"$set": post}, upsert=False)
        #result = mycollection.insert_one(post)
        po = posts.find_one({'peer_id': peer_id})
        if po is None:
            post = posts.find_one({'id': club_id})
            if post is not None:
                post['peer_id'] = peer_id
                posts.save(post)
                return 1
        return 0
