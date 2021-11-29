from commands import commands
import command_ls


class format_type_event(commands):

    async def run(self):

        msg = await self.get_event_type()

        if msg[1]:

            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="\n\n".join(msg[0]),
                                     random_id=0,
                                     keyboard=self.level_interest_event(f"10&{msg[2]}"))
        else:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="\n\n".join(msg[0]),
                                     random_id=0)


format_type_events = command_ls.Command()

format_type_events.keys = ['Лекции', 'Мастер-классы', 'Экскурсии', 'Интеллектуальные игры', 'Университетские субботы',
                           'Презентации Институтов и направлений', 'Дни открытых дверей', 'Олимпиады']
format_type_events.description = 'Подобрать по виду мероприятие'
format_type_events.set_dictionary('format_type_event')
format_type_events.process = format_type_event
format_type_events.topics_blocks = []
format_type_events.topics_resolution = ["tema1"]
