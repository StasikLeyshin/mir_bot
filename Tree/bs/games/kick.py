
import traceback

import command_besed
from commands import commands
from record_achievements import achievements
from api.api_execute import kick


class kick_game(commands):

    async def run(self):
        try:
            #print(self.date, 1661490839)
            if self.date > 1661490839:
                user_id = await self.getting_user_id()
                adm = await self.create_mongo.admin_check(user_id, self.peer_id)
                if adm:
                    await self.apis.api_post("execute", code=kick(users=[int(user_id)], chat_id=self.chat_id()), v=self.v)

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

kicks.keys = ['кик']
kicks.description = 'кик юзера'
kicks.set_dictionary('kick')
kicks.process = kick_game
kicks.topics_blocks = []
kicks.topics_resolution = ["tema1"]
