import asyncio
import traceback

import command_besed
from commands_tg import CommandsTg
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.user_profile import UserProfile


class user_profile_info(CommandsTg):

    async def run(self):
        try:
            #if await self.ls_open_check(self.from_id):
            res = await self.getting_user_id()
            if not res:
                user_id = self.from_id
                name = f"@{self.message['message']['from']['username']}"
            else:
                user_id = res[0]
                name = f"@{res[2]}"


            user_info = UserProfile(self.mongo_manager, self.settings_info, self.from_id, self.date,
                                    is_telegram=True)
            result = await user_info.run(user_id=int(user_id), peer_id=self.peer_id)

            # if result.get("user_id"):
            #     res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{result['user_id']}",
            #                                    name_case="gen")
            #     name = f'{res[0]["first_name"]} {res[0]["last_name"]}'

            # await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
            #                          message=result["message"].format(name), random_id=0)
            #self.apis.send_message(self.from_id, result["message"].format(name))
            await self.apis.api_post("sendMessage", chat_id=self.from_id,
                                     text=result["message"].format(name))


        except Exception as e:
            print(traceback.format_exc())
            await self.apis.api_post("sendMessage", chat_id=self.peer_id,
                                     text="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение")
            # self.apis.send_message(self.peer_id,
            #                        "⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение")





user_profile_infos = command_besed.Command()

user_profile_infos.keys = ['inf', 'info', 'профиль']
user_profile_infos.description = 'Профиль'
user_profile_infos.set_dictionary('user_profile_info')
user_profile_infos.process = user_profile_info
user_profile_infos.topics_blocks = []
user_profile_infos.topics_resolution = ["tema1"]
