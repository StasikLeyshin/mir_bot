import asyncio
import traceback

import command_besed
from commands import commands
from commands_tg import CommandsTg
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.help.help import Help
from summer_module.user_profile import UserProfile


class HelpBs(CommandsTg):

    async def run(self):
        try:
            res = await self.getting_user_id()
            if not res:
                user_id = self.from_id
                name = f"@{self.message['message'].from_user.username}"
            else:
                user_id = res[0]
                name = f"@{res[2]}"
            user_info = Help(self.mongo_manager, self.settings_info, self.from_id, self.date, is_telegram=True)
            result = await user_info.run(user_id=int(user_id), peer_id=self.peer_id)

            if result.get("user_id"):

                self.apis.send_message(self.from_id, result["message"].format(name))


        except Exception as e:
            print(traceback.format_exc())
            self.apis.send_message(self.peer_id,
                                   "⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение")





help_bss = command_besed.Command()

help_bss.keys = ['help', 'команды', 'помощь']
help_bss.description = 'Список доступных команд'
help_bss.set_dictionary('help_bss')
help_bss.process = HelpBs
help_bss.topics_blocks = []
help_bss.topics_resolution = ["tema1"]
