import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.user_profile import UserProfile


class user_profile_info(commands):

    async def run(self):
        try:
            #adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            # if adm:
            #     user_id = await self.getting_user_id()
            #     if not user_id:
            #         user_id = self.from_id
            #
            #     msg = await self.info_user(user_id)
            #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                              message=msg, random_id=0)
            #     return
            # res = await self.create_mongo.profile_users_add(self.from_id)
            #if res[1] > 20 or adm:
            if await self.ls_open_check(self.from_id):
                user_id = await self.getting_user_id()
                if not user_id:
                    user_id = self.from_id
                #msg = await self.info_user(user_id)
                # await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                #                          message=msg, random_id=0)
                # await achievements(self.client, int(user_id), self.v).user_profile_info(
                #     apis=self.apis, peer_id=self.peer_id,
                #     user_id=self.from_id)
                user_info = UserProfile(self.mongo_manager, self.settings_info, self.from_id, self.date)
                result = await user_info.run(user_id=int(user_id), peer_id=self.peer_id)

                name = ""
                if result.get("user_id"):
                    res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{result['user_id']}",
                                                   name_case="gen")
                    name = f'{res[0]["first_name"]} {res[0]["last_name"]}'

                await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                         message=result["message"].format(name), random_id=0)
                await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                         conversation_message_ids=self.conversation_message_id,
                                         delete_for_all=1)
            else:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                         random_id=0)

            #else:
                # if await self.ls_open_check(self.from_id):
                #     msg = await self.info_user(self.from_id, res)
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                #                              message=msg, random_id=0)
                # else:
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                              message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                #                              random_id=0)


        except Exception as e:
            print(traceback.format_exc())





user_profile_infos = command_besed.Command()

user_profile_infos.keys = ['inf', 'info', 'профиль']
user_profile_infos.description = 'Профиль'
user_profile_infos.set_dictionary('user_profile_info')
user_profile_infos.process = user_profile_info
user_profile_infos.topics_blocks = []
user_profile_infos.topics_resolution = ["tema1"]
