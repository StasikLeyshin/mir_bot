# from commands import commands
# import command_ls
#
#
# class offline_open_day(commands):
#
#     async def run(self):
#
#         msg = await self.get_open_day_online_offline()
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
# offline_open_days = command_ls.Command()
#
# offline_open_days.keys = ['Только очные']
# offline_open_days.description = 'Только очные ДОД'
# offline_open_days.set_dictionary('offline_open_day')
# offline_open_days.process = offline_open_day
# offline_open_days.topics_blocks = []
# offline_open_days.topics_resolution = ["tema1"]
