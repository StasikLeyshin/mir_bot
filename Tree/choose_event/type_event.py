from commands import commands
import command_ls


class type_event(commands):

    async def run(self):
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="📁 Выбери нужный формат мероприятия",
                                 random_id=0,
                                 keyboard=self.level_type_event())


type_events = command_ls.Command()

type_events.keys = ['По виду мероприятия']
type_events.description = 'По виду мероприятия'
type_events.set_dictionary('type_event')
type_events.process = type_event
type_events.topics_blocks = []
type_events.topics_resolution = ["tema1"]
