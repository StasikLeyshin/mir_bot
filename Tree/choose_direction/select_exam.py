# from commands import commands
# import command_ls
#
#
# class select_exam(commands):
#
#     async def run(self):
#
#         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
#                                  message="💡 Выбери, какой набор экзаменов ты собираешься сдавать.",
#                                  random_id=0,
#                                  keyboard=self.direction())
#
#
# select_exams = command_ls.Command()
#
# select_exams.keys = ['Подобрать по экзаменам']
# select_exams.description = 'Подобрать по экзаменам'
# select_exams.set_dictionary('select_exam')
# select_exams.process = select_exam
# select_exams.topics_blocks = []
# select_exams.topics_resolution = ["tema1"]
