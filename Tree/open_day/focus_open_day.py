from commands import commands
import command_ls


class focus_open_day(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="🎓 Выбери, что тебя интересует, чему бы ты хотел учиться.",
                                 random_id=0,
                                 keyboard=self.level_focus_open_day())


focus_open_days = command_ls.Command()

focus_open_days.keys = ['Хочу выбрать направленность']
focus_open_days.description = 'Хочу выбрать направленность ДОД'
focus_open_days.set_dictionary('focus_open_day')
focus_open_days.process = focus_open_day
focus_open_days.topics_blocks = []
focus_open_days.topics_resolution = ["tema1"]
