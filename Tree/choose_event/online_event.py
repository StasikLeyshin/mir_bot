from commands import commands
import command_ls


class online_event(commands):

    async def run(self):

        msg = await self.get_event_online_offline(is_online=True)

        if msg[1]:

            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="\n\n".join(msg[0]),
                                     random_id=0,
                                     keyboard=self.level_interest_event(f"10&{msg[2]}"))
        else:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="\n\n".join(msg[0]),
                                     random_id=0)
        await self.step_back_bool()


online_events = command_ls.Command()

online_events.keys = ['Онлайн мероприятия']
online_events.description = 'Подобрать онлайн мероприятие'
online_events.set_dictionary('online_event')
online_events.process = online_event
online_events.topics_blocks = []
online_events.topics_resolution = ["tema1"]
