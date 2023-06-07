
import json
import traceback

import command_besed
from commands import commands
from api import api_url, api, photo_upload


class report(commands):

    async def run(self):
        res = await self.create_mongo.profile_users_add(self.from_id)
        if res[1] > 40:
            user_id = await self.getting_user_id_fwd()
            if user_id:
                adm = await self.create_mongo.admin_check(user_id, self.peer_id)
                if not adm:
                    if await self.ls_open_check(self.from_id):
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                                 message="🚔 Ваш репорт успешно отправлен администраторам", random_id=0)
                    result = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                                      peer_ids=str(self.peer_id))
                    name = result["items"][0]['chat_settings']['title']
                    conversation_message_ids = ""
                    if self.fwd_messages:
                        conversation_message_ids = self.fwd_messages[0]["conversation_message_id"]
                    elif "reply_message" in self.message:
                        conversation_message_ids = self.message["reply_message"]["conversation_message_id"]
                    await self.apis.api_post("messages.send", v=self.v, peer_id=2000000024,
                                             message=f"🗣 Репорт от данного [id{self.from_id}|пользователя] на [id{user_id}|этого пользователя]\n\n"
                                                     f"👥 Беседа: '{name}'\n\n"
                                                     f"Заварнить?",
                                             random_id=0, keyboard=self.keyboard_warn(
                            f"{user_id}@{self.date}@{conversation_message_ids}"),
                                             forward=self.answer_msg_other())
                    await self.create_mongo.add_users_zawarn(user_id, self.date, self.peer_id)
                    await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                             conversation_message_ids=self.conversation_message_id,
                                             delete_for_all=1)
            else:
                if await self.ls_open_check(self.from_id):
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message="⚠ Перешлите сообщение, чтобы зарепортить и поймать человека с поличным.",
                                             random_id=0)










reports = command_besed.Command()

reports.keys = ['/report45trgttr', '/репорт54t4g54wrtgw']
reports.description = 'Для тестов'
reports.process = report
reports.topics_blocks = []
reports.topics_resolution = ["tema1"]
