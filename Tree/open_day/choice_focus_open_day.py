from commands import commands
import command_ls


class choice_focus_open_day(commands):

    async def run(self):

        msg = await self.get_choice_focus_open_day()

        if msg[1]:

            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="\n\n".join(msg[0]),
                                     random_id=0,
                                     keyboard=self.level_interest_event(f"10&{msg[2]}"))
        else:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="\n\n".join(msg[0]),
                                     random_id=0)
        await self.step_back_bool()

        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                          message="🎓 Выбери, что тебя интересует, чему бы ты хотел учиться.",
        #                          random_id=0,
        #                          keyboard=self.level_focus_open_day())


choice_focus_open_days = command_ls.Command()

choice_focus_open_days.keys = ['Все программы', 'IT и анализ данных', 'Безопасность и приборостроение',
                               'Кибернетика, робототехника', 'Экономика и управление', 'Юриспруденция',
                               'Химия и биотехнологии', 'Радиоэлектроника', 'Дизайн', 'Колледж']
choice_focus_open_days.description = 'Выбор направленности ДОД'
choice_focus_open_days.set_dictionary('choice_focus_open_day')
choice_focus_open_days.process = choice_focus_open_day
choice_focus_open_days.topics_blocks = []
choice_focus_open_days.topics_resolution = ["tema1"]
