import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module import WarnAdminCheck
from summer_module.punishments import BanGive


class Report(commands):

    async def run(self):
        try:
            user_id = await self.getting_user_id()
            if user_id:
                if await self.ls_open_check(self.from_id):
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message="🚔 Ваш репорт успешно отправлен администраторам", random_id=0)
                result = await self.apis.api_post("messages.getConversationsById", v=self.v, peer_ids=str(self.peer_id))
                name = result["items"][0]['chat_settings']['title']
                if self.fwd_messages:
                    conversation_message_ids = self.fwd_messages[0]["conversation_message_id"]
                elif "reply_message" in self.message:
                    conversation_message_ids = self.message["reply_message"]["conversation_message_id"]

                res = await self.apis.api_post("messages.send", v=self.v, peer_id=2000000039,
                                         message=f"🗣 Репорт от данного [id{self.from_id}|пользователя] на [id{user_id}|этого пользователя]\n\n"
                                                 f"👥 Беседа: '{name}'\n\n"
                                                 f"Заварнить?",
                                         random_id=0, keyboard=self.keyboard_warn(
                        f"{user_id}@{self.date}@{conversation_message_ids}@rep"),
                                         forward=self.answer_msg_other())
                zawarn = WarnAdminCheck(self.mongo_manager, self.settings_info, self.from_id, self.date)
                await zawarn.add_zawarn(user_id=int(user_id), peer_id=self.peer_id,
                                        conversation_message_id_forward=int(conversation_message_ids),
                                        conversation_message_id_original=int(res),
                                        type_sms="rep")
            else:
                if await self.ls_open_check(self.from_id):
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message="⚠ Перешлите сообщение, чтобы зарепортить и поймать человека с поличным.",
                                             random_id=0)
            await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                     conversation_message_ids=self.conversation_message_id,
                                     delete_for_all=1)


        except Exception as e:
            print(traceback.format_exc())



reports = command_besed.Command()

reports.keys = ['/report', '/репорт']
reports.description = 'Выдача бана'
reports.set_dictionary('report')
reports.loyal = True
reports.process = Report
reports.topics_blocks = []
reports.topics_resolution = ["tema1"]

if __name__ == "__main__":

    str = "{0}test 228"
    print(str.format("test"))
