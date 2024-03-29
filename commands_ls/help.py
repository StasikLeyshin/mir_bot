import command_ls
from commands import commands


class help(commands):

    async def run(self):

        chek = self.create_mongo.check_user(self.peer_id)

        if chek != 0:
            self.create_mongo.add_user(self.peer_id, 0)

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 # message="🌐 Команды бота:\n\n"
                                 #         #"📝 Вопросы — покажет список часто задаваемых вопросов.\n\n"
                                 #         #"📈 Направления — подберёт перспективные направления по проходным баллам\n\n"
                                 #         #"📊 Конкурс — покажет текущее положение в списке\n\n"
                                 #         "👑 Админ [ваш вопрос] — перешлёт ваш вопрос админу для более быстрого ответа.\n"
                                 #         "❗ Пример написания:\n"
                                 #         "Админ, есть изменения в информации о зачислении?",
                                 message="😎 Я здесь, чтобы помочь разобраться с поступлением в МИРЭА – Российский технологический университет. Я умею:\n"
                                         "💬 Отвечать на частые вопросы\n"
                                         "✈ Подбирать направление подготовки\n"
                                         "👥 Подбирать мероприятие, на которое тебе стоит сходить\n"
                                         "🗣 Рассказать о Днях открытых дверей\n\n"
                                         "⁉ Чем помочь тебе? Кликай на нужную кнопку и будем поступать в РТУ МИРЭА вместе.",
                                 random_id=0,
                                 keyboard=self.menu())



helps = command_ls.Command()

helps.keys = ['командыetet', 'начатьett', 'helpertert']
helps.description = 'Вопросы'
helps.process = help
helps.topics_blocks = []
helps.topics_resolution = ["tema1"]
