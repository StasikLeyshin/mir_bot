# -*- coding: utf-8 -*-
import traceback

import command_besed
from api.api_execute import kick
from commands import commands
from summer_module.input_output_conversation import ConversationOutput


class ChatKickUser(commands):

    async def run(self):
        try:
            con = ConversationOutput(self.mongo_manager, self.settings_info,
                                     user_id=self.from_id, current_time=self.date)
            result = await con.run(user_id=int(self.message["action"]["member_id"]), peer_id_zl=self.peer_id)

            if result["message"]:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=result["message"], random_id=0)
            if result["action"] == "kick":
                await self.apis.api_post("execute", code=kick(users=result["kick_id"], chat_id=self.chat_id()),
                                         v=self.v)
        except Exception as e:
            print(traceback.format_exc())



ChatKickUsers = command_besed.Command()

ChatKickUsers.keys = ['chat_kick_user']
ChatKickUsers.description = 'Выход или кик пользователя'
ChatKickUsers.set_dictionary('chat_kick_user')
ChatKickUsers.process = ChatKickUser
ChatKickUsers.topics_blocks = []
ChatKickUsers.topics_resolution = ["zluka"]
