
# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands

from punishments import warn_give_out
from api.api_execute import kick

class warn(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                user_id = await self.getting_user_id()
                if user_id:
                    pass


        except Exception as e:
            print(traceback.format_exc())








warns = command_besed.Command()

warns.keys = ['/warn', '/варн', '/Варн', '/Warn']
warns.description = 'Выдача варна'
warns.process = warn
warns.topics_blocks = []
warns.topics_resolution = ["tema1"]
