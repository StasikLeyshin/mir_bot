# from commands import commands
# import command_ls
#
#
# class choose_event(commands):
#
#     async def run(self):
#
#         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
#                                  message="🔑 Мы можем подобрать мероприятие по интересам, формату проведения, "
#                                          "виду мероприятия или даже дате проведения.\n"
#                                          "‼ Обрати внимание, на все наши мероприятия тебе нужно регистрироваться.\n"
#                                          "💡 Для этого нужно завести личный кабинет абитуриента на сайте приёмной комиссии:\n\n"
#                                          "🌐 https://priem.mirea.ru/lk\n\n"
#                                          "⚙ Выбери нужный параметр для подбора мероприятия.",
#                                  random_id=0,
#                                  keyboard=self.level_choose_event())
#
#
# choose_events = command_ls.Command()
#
# choose_events.keys = ['Подобрать мероприятие']
# choose_events.description = 'Подобрать мероприятие'
# choose_events.set_dictionary('choose_event')
# choose_events.process = choose_event
# choose_events.topics_blocks = []
# choose_events.topics_resolution = ["tema1"]
