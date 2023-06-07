import asyncio
import traceback

import command_besed
from commands import commands
from punishments import ban_give_out
from api.api_execute import kick
from record_achievements import achievements
from summer_module import Binding


class binding(commands):

    async def run(self):
        try:
            if self.from_id == -5411326 or self.from_id == -194180799:
                peer_id_ab = self.message["text"].split(" ")[0]
                peer_id_zl = self.message["peer_id"]
                #res = await self.create_mongo.add_besed_zl(peer_id_ab, peer_id_zl)
                bind = Binding(self.mongo_manager, self.settings_info)
                result = await bind.run(peer_id=peer_id_ab, peer_id_zl=peer_id_zl)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.message["peer_id"],
                                         message=result["message"], random_id=0)

        except Exception as e:
            print(traceback.format_exc())





bindings = command_besed.Command()

bindings.keys = ['родная']
bindings.description = 'Связка беседы зклюки с основой'
bindings.set_dictionary('binding')
bindings.fully = True
bindings.process = binding
bindings.topics_blocks = []
bindings.topics_resolution = ["zluka"]
