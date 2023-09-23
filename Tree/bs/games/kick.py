
import traceback

import command_besed
from commands import commands
from record_achievements import achievements
from api.api_execute import kick
from summer_module.games.kick import KickGame


class kick_game(commands):

    async def run(self):
        try:
            #print(self.date, 1661490839)
            if self.date > 1692705655:
                if int(self.peer_id) != 2000000052 and int(self.peer_id) != 2000000049:
                    user_id = await self.getting_user_id()
                    #adm = await self.create_mongo.admin_check(user_id, self.peer_id)
                    #if adm:
                    kick1 = KickGame(self.mongo_manager, self.settings_info, self.from_id, self.date)
                    result = await kick1.run(user_id=int(user_id), peer_id=self.peer_id)
                    if result['kick']:
                        await self.apis.api_post("execute", code=kick(users=[int(user_id)], chat_id=self.chat_id()),
                                                 v=self.v)
            else:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                         message="🧿 Команда накапливает ману", random_id=0)

            # number = await self.getting_number()
            # res = await achievements(self.client, self.from_id, self.v).roulette(
            #     apis=self.apis, peer_id=self.peer_id, start_time=self.date, number_issued=1, number=number)
            # if res[0] == 1 and res[1]:
            #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                              message=res,
            #                              random_id=0, forward=self.answer_msg(), keyboard=self.pusto())
            # elif res[0] == 0:
            #     if await self.ls_open_check(self.from_id):
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
            #                                  message=res,
            #                                  random_id=0)
            #         await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
            #                                  conversation_message_ids=self.conversation_message_id,
            #                                  delete_for_all=1)
            #     else:
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                                  message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
            #                                  forward=self.answer_msg(),
            #                                  random_id=0)
        except Exception as e:
            print(traceback.format_exc())


kicks = command_besed.Command()

kicks.keys = ['до свидания', '/до свидания']
kicks.description = 'кик юзера'
kicks.loyal = True
kicks.set_dictionary('kick')
kicks.process = kick_game
kicks.topics_blocks = []
kicks.topics_resolution = ["tema1"]
