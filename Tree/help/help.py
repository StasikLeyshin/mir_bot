from commands import commands
import command_ls
from summer_module.work_ls.work_ls import WorkLs


class help(commands):

    async def run(self):

        # if self.them == "mirea_official":
        #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                              message="😎 Я здесь, чтобы ответить на частые вопросы и поделиться полезными ссылками.\n"
        #                                      "💬 Если вы хотите посмотреть список часто задаваемых вопросов и получить ответ на них, нажмите на соответствующую кнопку.",
        #                              random_id=0,
        #                              keyboard=self.menu_mirea())
        # else:
        #
        #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                              message="😎 Я здесь, чтобы помочь разобраться с поступлением в МИРЭА – Российский технологический университет. Я умею:\n"
        #                                      "💬 Отвечать на частые вопросы\n"
        #                                      "✈ Подбирать направление подготовки\n"
        #                                      "👥 Подбирать мероприятие, на которое тебе стоит сходить\n"
        #                                      "🗣 Рассказывать о Днях открытых дверей\n\n"
        #                                      "⁉ Чем помочь тебе? Кликай на нужную кнопку и будем поступать в РТУ МИРЭА вместе.",
        #                              random_id=0,
        #                              keyboard=self.menu())

        work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
        res = await work_ls.location_tree_check()
        res.ignore_tree = False
        await work_ls.location_tree_update()
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="😎 Привет, я — бот приёмной комиссии. "
                                         "Я попробую ответить на ваши вопросы. "
                                         "Если что-то пойдёт не так, переведу на сотрудника. "
                                         "Укажите, о чём вы хотели бы узнать.\n\n"
                                         "💬 Помощь по приёму\n"
                                         "✈ Подбор направлений\n"
                                         "🆘 Репорт",
                                 random_id=0,
                                 keyboard=self.menu())

helps = command_ls.Command()

helps.keys = ['команды', 'начать', 'help', 'меню', 'Вернуться в меню']
helps.description = 'Меню'
helps.set_dictionary('help')
helps.process = help
helps.topics_blocks = []
helps.topics_resolution = ["tema1"]
