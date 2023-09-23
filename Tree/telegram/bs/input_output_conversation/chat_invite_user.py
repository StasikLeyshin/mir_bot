# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from api.api_execute import kick
from commands import commands
from summer_module.input_output_conversation import ConversationInput
from summer_module.punishments import WarnAdminCheck
from summer_module.punishments.unban import UnbanLs


class ChatInviteUser(commands):

    async def run(self):
        try:
            con = ConversationInput(self.mongo_manager, self.settings_info,
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



ChatInviteUsers = command_besed.Command()

ChatInviteUsers.keys = ['chat_invite_user']
ChatInviteUsers.description = 'Приход пользователя по ссылке'
ChatInviteUsers.set_dictionary('chat_invite_user')
ChatInviteUsers.process = ChatInviteUser
ChatInviteUsers.topics_blocks = []
ChatInviteUsers.topics_resolution = ["zluka"]
