import asyncio
import traceback

import command_besed
from commands import commands
from commands_tg import CommandsTg
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.punishments import BanGive


class ban(CommandsTg):

    async def run(self):
        try:
            res = await self.getting_user_id()
            if res:
                user_id = res[0]
                name = f"@{res[2]}"
                cause = await self.txt_warn(self.text)

                ban_give = BanGive(self.mongo_manager, self.settings_info, self.from_id, self.date, is_telegram=True)

                result = await ban_give.run(user_id=int(user_id), peer_id=self.peer_id, cause=cause, from_id_check=True)
                if result:
                    #self.apis.send_message(self.peer_id, result["message"].format(name))
                    await self.apis.api_post("sendMessage", chat_id=self.peer_id,
                                             text=result["message"].format(name))
                    if result["action"] == "kick":
                        for i in result["kick_id"]:
                            await self.apis.api_post("kickChatMember", chat_id=self.peer_id, user_id=i)
                            #self.apis.kick_chat_member(self.peer_id, i)



        except Exception as e:
            print(traceback.format_exc())





bans = command_besed.Command()

bans.keys = ['/бан', '/ban', '/Бан', '/Ban']
bans.description = 'Выдача бана'
bans.set_dictionary('ban')
bans.loyal = True
bans.process = ban
bans.topics_blocks = []
bans.topics_resolution = ["tema1"]

if __name__ == "__main__":

    str = "{0}test 228"
    print(str.format("test"))
