from commands import commands
import command_ls


class type_event(commands):

    async def run(self):
        if "payload" in self.message:

            list_payload = self.message["payload"].replace('"', '').split("&")

            if list_payload[1] == "event":
                msg = await self.get_event_type(event_id=list_payload[2], offset=int(list_payload[0]))
            elif list_payload[1] == "online":
                flag = False
                if list_payload[2] == "1":
                    flag = True
                msg = await self.get_event_online_offline(is_online=flag, offset=int(list_payload[0]))
            elif list_payload[1] == "direction":
                msg = await self.get_event_interest(event_id=list_payload[2], offset=int(list_payload[0]))
            elif list_payload[1] == "open_day_online":
                flag = False
                if list_payload[2] == "1":
                    flag = True
                msg = await self.get_open_day_online_offline(is_online=flag, offset=int(list_payload[0]))
            else:
                return
            if msg[1]:

                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="\n\n".join(msg[0]),
                                         random_id=0,
                                         keyboard=self.level_interest_event(f"{int(int(list_payload[0]) + 10)}&{msg[2]}"))
            else:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="\n\n".join(msg[0]),
                                         random_id=0)


type_events = command_ls.Command()

type_events.keys = ['Показать ещё']
type_events.description = 'Показать ещё'
#type_events.set_dictionary('type_event')
type_events.process = type_event
type_events.topics_blocks = []
type_events.topics_resolution = ["tema1"]
