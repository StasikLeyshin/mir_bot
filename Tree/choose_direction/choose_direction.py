# from commands import commands
# import command_ls
#
#
# class choose_direction(commands):
#
#     async def run(self):
#
#         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
#                                  message="🎓 Какой уровень будете познавать?",
#                                  random_id=0,
#                                  keyboard=self.level_where_level())
#
#
# choose_directions = command_ls.Command()
#
# choose_directions.keys = ['подобрать направление']
# choose_directions.description = 'где живёт'
# choose_directions.set_dictionary('choose_direction')
# choose_directions.process = choose_direction
# choose_directions.topics_blocks = []
# choose_directions.topics_resolution = ["tema1"]
