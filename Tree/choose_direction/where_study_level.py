# from commands import commands
# import command_ls
#
#
# class where_study_level(commands):
#
#
#     async def run(self):
#         #print(111111111)
#         res = await self.create_mongo.get_value_profile_ls(self.from_id, directions=1)
#         #print(res)
#         if res:
#             if res.get('level') and self.text.lower() == "шаг назад":
#                 level = res['level']
#             else:
#                 level = self.level[self.text.lower()]
#         else:
#             level = self.level[self.text.lower()]
#         print(level)
#         await self.create_mongo.setting_value_profile_ls(self.from_id, directions=1,
#                                                          level=level)
#
#         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
#                                  message="🏤 Где вы хотите обучаться?",
#                                  random_id=0,
#                                  keyboard=self.level_where_study())
#
#
# where_study_levels = command_ls.Command()
#
# where_study_levels.keys = ['бакалавриат/специалитет', 'магистратура', 'аспирантура']
# where_study_levels.description = 'Выбор уровня'
# where_study_levels.set_dictionary('where_study_level')
# where_study_levels.process = where_study_level
# where_study_levels.topics_blocks = []
# where_study_levels.topics_resolution = ["tema1"]
