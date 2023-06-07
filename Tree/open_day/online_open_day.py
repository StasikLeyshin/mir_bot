# from commands import commands
# import command_ls
#
#
# class online_open_day(commands):
#
#     async def run(self):
#
#         msg = await self.get_open_day_online_offline(is_online=True)
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
# online_open_days = command_ls.Command()
#
# online_open_days.keys = ['Только онлайн']
# online_open_days.description = 'Только онлайн ДОД'
# online_open_days.set_dictionary('online_open_day')
# online_open_days.process = online_open_day
# online_open_days.topics_blocks = []
# online_open_days.topics_resolution = ["tema1"]
