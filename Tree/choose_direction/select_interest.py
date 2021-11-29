from commands import commands
import command_ls


class select_interests(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="🎓 Выбери, что тебя интересует, чему бы ты хотел учиться.",
                                 random_id=0,
                                 keyboard=self.level_select_interests())


select_interestss = command_ls.Command()

select_interestss.keys = ['Подобрать по интересам']
select_interestss.description = 'Подобрать направление'
select_interestss.set_dictionary('select_interests')
select_interestss.process = select_interests
select_interestss.topics_blocks = []
select_interestss.topics_resolution = ["tema1"]
