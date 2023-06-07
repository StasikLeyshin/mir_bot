
import traceback

import command_besed
from commands import commands
from record_achievements import achievements


class roulette_new(commands):

    async def run(self):
        try:

            number = await self.getting_number()
            res = await achievements(self.client, self.from_id, self.v).roulette(
                apis=self.apis, peer_id=self.peer_id, start_time=self.date, number_issued=1, number=number)
            if res[0] == 1 and res[1]:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=res,
                                         random_id=0, forward=self.answer_msg(), keyboard=self.pusto())
            elif res[0] == 0:
                if await self.ls_open_check(self.from_id):
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=res,
                                             random_id=0)
                    await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                             conversation_message_ids=self.conversation_message_id,
                                             delete_for_all=1)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             forward=self.answer_msg(),
                                             random_id=0)
        except Exception as e:
            print(traceback.format_exc())


roulette_news = command_besed.Command()

roulette_news.keys = ['выстрел']
roulette_news.description = 'Рулетка новая'
roulette_news.set_dictionary('roulette_new')
roulette_news.process = roulette_new
roulette_news.topics_blocks = []
roulette_news.topics_resolution = ["tema1"]
