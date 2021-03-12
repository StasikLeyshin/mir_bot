# -*- coding: utf-8 -*-
import asyncio

from api.methods import methods
class commands:

    def __init__(self, v, club_id, message, apis, them, create_mongo, collection_bots, document_tokens, url_dj):

        self.v = v
        self.club_id = club_id
        self.message = message
        self.peer_id = self.message["peer_id"]
        self.from_id = self.message["from_id"]
        self.date = self.message["date"]
        self.id_sms = self.message["id"]
        self.text = self.message["text"]
        self.conversation_message_id = self.message["conversation_message_id"]
        self.fwd_messages = self.message["fwd_messages"]
        self.attachments = self.message["attachments"]
        self.methods = methods(self.v, self.club_id)
        self.apis = apis
        self.them = them
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.url_dj = url_dj

    '''async def bind(self):
        ad = methods(self.v, self.club_id)
        adm = await ad.admin_chek(self.message)
        if adm == 1:pass'''


