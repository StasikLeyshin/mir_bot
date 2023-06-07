# -*- coding: utf-8 -*-
import asyncio

import command_besed
from commands import commands

class start(commands):

    async def run(self):
        adm = await self.methods.admin_chek(self.peer_id, self.from_id, self.apis)

        if adm == 1:
            star = await self.methods.users_chek(self.peer_id, self.apis)
            if star:
                self.create_mongo.start_bs(self.peer_id, star[0], star[1], star[2])
                # result = await self.apis.api_post("messages.getByConversationMessageId", v=self.v, peer_id=self.peer_id,
                                                  # conversation_message_ids=str(self.conversation_message_id))
                #sms_id = result["items"][0]["id"]
                #print(sms_id)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="Вдох-выдох ✅", random_id=0)  # , reply_to=sms_id)





starts = command_besed.Command()

starts.keys = ['старткупиуерепик', 'стартуемсауакикаам']
starts.description = 'Привязка беседы'
starts.process = start
starts.topics_blocks = []
starts.topics_resolution = ["tema1"]
