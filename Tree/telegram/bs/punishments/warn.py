import asyncio
import traceback

import command_besed
from commands import commands
from commands_tg import CommandsTg
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.punishments import WarnGive


class warn(CommandsTg):

    async def run(self):
        try:
            res = await self.getting_user_id()
            if res:
                user_id = res[0]
                name = f"@{res[2]}"

                cause = await self.txt_warn(self.text)

                ban_give = WarnGive(self.mongo_manager, self.settings_info, self.from_id, self.date, is_telegram=True)

                result = await ban_give.run(user_id=int(user_id), peer_id=self.peer_id, cause=cause, from_id_check=True)
                #print(result)
                if result:
                    #res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{user_id}", name_case="nom")
                    #name = f'{res[0]["first_name"]} {res[0]["last_name"]}'

                    # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                    #                          message=result["message"].format(name), random_id=0)
                    #self.apis.send_message(self.peer_id, result["message"].format(name))
                    await self.apis.api_post("sendMessage", chat_id=self.peer_id,
                                             text=result["message"].format(name))
                    if result["action"] == "kick":
                        for i in result["kick_id"]:
                            await self.apis.api_post("kickChatMember", chat_id=self.peer_id, user_id=i)
                            #self.apis.kick_chat_member(self.peer_id, i)
                        # await self.apis.api_post("execute", code=kick(users=result["kick_id"], chat_id=self.chat_id()),
                        #                          v=self.v)


        except Exception as e:
            print(traceback.format_exc())





warns = command_besed.Command()

warns.keys = ['наказать', 'варн', 'warn']
warns.description = 'Выдача варна'
warns.loyal = True
warns.set_dictionary('warn')
warns.process = warn
warns.topics_blocks = []
warns.topics_resolution = ["tema1"]
