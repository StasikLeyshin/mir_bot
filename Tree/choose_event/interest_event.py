from commands import commands
import command_ls


class interest_event(commands):

    async def run(self):

        msg = await self.get_event_interest()

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


interest_events = command_ls.Command()

interest_events.keys = ['IT и анализ данных', 'Химия и биотехнология', 'Информационная/компьютерная безопасность',
                  'Радиоэлектроника', 'Робототехника и автоматизация', 'Экономика и управление',
                  'Дизайн', 'Юриспруденция']
interest_events.description = 'Подобрать направление по интересу'
interest_events.set_dictionary('interest_event')
interest_events.process = interest_event
interest_events.topics_blocks = []
interest_events.topics_resolution = ["tema1"]
