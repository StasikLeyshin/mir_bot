from commands import commands
import command_ls


class interest(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="📚 Выбери, что тебя интересует, чему бы ты хотел учиться.",
                                 random_id=0,
                                 keyboard=self.level_select_interests())


interests = command_ls.Command()

interests.keys = ['IT и анализ данных', 'Химия и биотехнология', 'Информационная/компьютерная безопасность',
                  'Радиоэлектроника', 'Робототехника и автоматизация', 'Экономика и управление',
                  'Дизайн', 'Юриспруденция']
interests.description = 'Подобрать направление по интересу'
interests.set_dictionary('interest')
interests.process = interest
interests.topics_blocks = []
interests.topics_resolution = ["tema1"]
