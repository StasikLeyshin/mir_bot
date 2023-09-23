# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from api.api_execute import kick
from commands import commands
from summer_module.input_output_conversation import ConversationInput
from summer_module.punishments import WarnAdminCheck
from summer_module.punishments.unban import UnbanLs


class ChatInviteUserByLink(commands):

    async def run(self):
        try:
            print("ОН ПРИШОЛ")
            con = ConversationInput(self.mongo_manager, self.settings_info,
                                    user_id=self.from_id, current_time=self.date)
            result = await con.run(user_id=self.from_id, peer_id_zl=self.peer_id, type_input="chat_invite_user_by_link")

            if result["message"]:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=result["message"], random_id=0)
            if result["action"] == "kick":
                await self.apis.api_post("execute", code=kick(users=result["kick_id"], chat_id=self.chat_id()),
                                         v=self.v)
        except Exception as e:
            print(traceback.format_exc())



ChatInviteUserByLinks = command_besed.Command()

ChatInviteUserByLinks.keys = ['chat_invite_user_by_link']
ChatInviteUserByLinks.description = 'Приход пользователя по ссылке'
ChatInviteUserByLinks.set_dictionary('chat_invite_user_by_link')
ChatInviteUserByLinks.process = ChatInviteUserByLink
ChatInviteUserByLinks.topics_blocks = []
ChatInviteUserByLinks.topics_resolution = ["zluka"]
