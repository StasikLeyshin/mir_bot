# from commands import commands
# import command_ls
#
#
# class all_open_day(commands):
#
#     async def run(self):
#
#         msg = await self.get_event_type(event_id=15)
#
#         if msg[1]:
#
#             await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
#                                      message="\n\n".join(msg[0]),
#                                      random_id=0,
#                                      keyboard=self.level_interest_event(f"10&{msg[2]}"))
#         else:
#             await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
#                                      message="\n\n".join(msg[0]),
#                                      random_id=0)
#         await self.step_back_bool()
#
#
# all_open_days = command_ls.Command()
#
# all_open_days.keys = ['Хочу посмотреть все']
# all_open_days.description = 'Хочу посмотреть все ДОД'
# all_open_days.set_dictionary('all_open_day')
# all_open_days.process = all_open_day
# all_open_days.topics_blocks = []
# all_open_days.topics_resolution = ["tema1"]
