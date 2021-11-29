from commands import commands
import command_ls


class select_interest_event(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="🎓 Выбери, что тебя интересует, чему бы ты хотел учиться.",
                                 random_id=0,
                                 keyboard=self.level_select_interests())


select_interest_events = command_ls.Command()

select_interest_events.keys = ['Подобрать по интересам']
select_interest_events.description = 'Подобрать по интересам'
select_interest_events.set_dictionary('select_interest_event')
select_interest_events.process = select_interest_event
select_interest_events.topics_blocks = []
select_interest_events.topics_resolution = ["tema1"]
