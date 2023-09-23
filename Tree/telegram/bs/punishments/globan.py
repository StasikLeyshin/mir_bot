import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module.punishments.globan import GloBan


class ban(commands):

    async def run(self):
        try:
            user_id = await self.getting_user_id()
            if user_id:
                cause = await self.txt_warn(self.text)

                ban_give = GloBan(self.mongo_manager, self.settings_info, self.from_id, self.date)

                result = await ban_give.run(user_id=int(user_id), peer_id=self.peer_id, cause=cause)
                if result:


                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=result["message"], random_id=0)
                    if result["action"] == "kick":
                        loop = asyncio.get_running_loop()
                        for i in result["peer_ids"]:
                            try:
                                loop.create_task(self.apis.api_post("messages.removeChatUser",
                                                                    chat_id=self.chat_id_param(i),
                                                                    member_id=user_id,
                                                                    v=self.v))
                            except:pass
                    # await self.apis.api_post("execute", code=kick(users=result["kick_id"], chat_id=self.chat_id()),
                    #                          v=self.v)


        except Exception as e:
            print(traceback.format_exc())





bans = command_besed.Command()

bans.keys = ['/глобан', '/globan']
bans.description = 'Выдача бана'
bans.set_dictionary('ban')
bans.loyal = True
bans.process = ban
bans.topics_blocks = []
bans.topics_resolution = ["tema1"]

if __name__ == "__main__":

    str = "{0}test 228"
    print(str.format("test"))
