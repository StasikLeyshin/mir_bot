from commands import commands
import command_ls


class open_day(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="🚪 День открытых дверей — отличный способ познакомиться с вузом, "
                                         "посмотреть на него своими глазами, порасспрашивать представителей Институтов "
                                         "обо всём, что тебя интересует.\n"
                                         "🦠 В этом году мы проводим Дни открытых дверей в очном и онлайн формате.\n"
                                         "📅 Рассказать о датах всех открытых дверей или интересует конкретный?",
                                 random_id=0,
                                 keyboard=self.level_open_day())


open_days = command_ls.Command()

open_days.keys = ['Дни открытых дверей']
open_days.description = 'Дни открытых дверей'
open_days.set_dictionary('open_day')
open_days.process = open_day
open_days.topics_blocks = []
open_days.topics_resolution = ["tema1"]
