
import json
import traceback

import command_besed
from commands import commands
from api import api_url, api, photo_upload


class test(commands):

    async def run(self):
        if self.from_id == 597624554:
            try:
                # msg = {
                #     "conversation_message_ids": [self.conversation_message_id],
                #     "peer_id": self.peer_id
                #     #"is_reply": True
                # }
                # msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
                # msg = str(msg.decode('utf-8'))
                # print(msg)
                res = await photo_upload(self.apis, self.v, self.peer_id, f"2021/06/29/28ae1abb0bcacd6e81ad2de947ba86da.jpg", "/home/stas/mir_bot/media/").upload()

                #"/home/stas/mir_bot/media/2021/06/28/28ae1abb0bcacd6e81ad2de947ba86da.jpg"
                await self.apis.api_post("messages.send", v=self.v, peer_id=2000000023,
                                         message="test", random_id=0)  # , attachment=res)#, forward=msg)
            except Exception as e:
                print(traceback.format_exc())


tests = command_besed.Command()

tests.keys = ['тест', 'test']
tests.description = 'Для тестов'
tests.process = test
tests.topics_blocks = []
tests.topics_resolution = ["tema1"]
