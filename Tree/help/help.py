from commands import commands
import command_ls


class help(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="😎 Я здесь, чтобы помочь разобраться с поступлением в МИРЭА – Российский технологический университет. Я умею:\n"
                                         "💬 Отвечать на частые вопросы\n"
                                         "✈ Подбирать направление подготовки\n"
                                         "👥 Подбирать мероприятие, на которое тебе стоит сходить\n"
                                         "🗣 Рассказывать о Днях открытых дверей\n\n"
                                         "⁉ Чем помочь тебе? Кликай на нужную кнопку и будем поступать в РТУ МИРЭА вместе.",
                                 random_id=0,
                                 keyboard=self.menu())

helps = command_ls.Command()

helps.keys = ['команды', 'начать', 'help', 'меню', 'Вернуться в меню']
helps.description = 'Меню'
helps.set_dictionary('help')
helps.process = help
helps.topics_blocks = []
helps.topics_resolution = ["tema1"]
