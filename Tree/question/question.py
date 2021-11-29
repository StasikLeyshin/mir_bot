from commands import commands
import command_ls


class question(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="📚 Выбери свой статус",
                                 random_id=0,
                                 keyboard=self.level_status())


questions = command_ls.Command()

questions.keys = ['Частые вопросы']
questions.description = 'Вопросы'
questions.set_dictionary('question')
questions.process = question
questions.topics_blocks = []
questions.topics_resolution = ["tema1"]
