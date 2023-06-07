# from commands import commands
# import command_ls
#
#
# class offline_event(commands):
#
#     async def run(self):
#
#         msg = await self.get_event_online_offline()
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
# offline_events = command_ls.Command()
#
# offline_events.keys = ['Очные мероприятия']
# offline_events.description = 'Подобрать очное мероприятие'
# offline_events.set_dictionary('offline_event')
# offline_events.process = offline_event
# offline_events.topics_blocks = []
# offline_events.topics_resolution = ["tema1"]
