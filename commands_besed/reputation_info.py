import traceback

import command_besed
from commands import commands

class reputation_info(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                user_id = await self.getting_user_id()
                if not user_id:
                    user_id = self.from_id

                msg = await self.info_reputation(user_id)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=msg, random_id=0)
                return
            res = await self.create_mongo.profile_users_add(self.from_id)
            if res[1] > 30:
                if await self.ls_open_check(self.from_id):
                    user_id = await self.getting_user_id()
                    if not user_id:
                        user_id = self.from_id
                    msg = await self.info_reputation(user_id)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=msg, random_id=0)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             random_id=0)

            else:
                if await self.ls_open_check(self.from_id):
                    msg = await self.info_reputation(self.from_id)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                             message=msg, random_id=0)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             random_id=0)
        except Exception as e:
            print(traceback.format_exc())




reputation_infos = command_besed.Command()

reputation_infos.keys = ['рептайм', 'реп тайм', 'rep time', 'reptime', 'таймреп']
reputation_infos.description = 'Минус репутация'
reputation_infos.process = reputation_info
reputation_infos.topics_blocks = []
reputation_infos.topics_resolution = ["tema1"]
