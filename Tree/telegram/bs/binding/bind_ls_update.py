
from commands import commands
import command_ls
from summer_module import Start


class BindLsUpdate(commands):

    async def run(self):
        if self.from_id == 597624554:
            start = Start(self.mongo_manager, self.settings_info)
            peer_ids = await start.get_all_peer_ids()
            sms_list = []
            for i in peer_ids:

                get_method = await self.methods.users_chek(i, self.apis)
                if get_method:
                    result = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                                      peer_ids=str(i))
                    name = result["items"][0]['chat_settings']['title']
                    sms_list.append(f"👥 {name}")
                    await start.run(peer_id=int(i), users=get_method[0], users_all=get_method[1],
                                    user_admins=get_method[2])
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="Данные текущих бесед обновлены:\n" + "\n".join(sms_list),
                                     random_id=0)# , reply_to=sms_id)
            # for i in range(2000000060, 2000000120):
            #     try:
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=i,
            #                                  message="/update", random_id=0)
            #     except:
            #         pass



bind_ls_updates = command_ls.Command()

bind_ls_updates.keys = ['обновить', '/обновить']
bind_ls_updates.description = 'обновить'
#bind_ls_updates.set_dictionary('bind_ls_update')
bind_ls_updates.process = BindLsUpdate
#endless_questionss.mandatory = True
bind_ls_updates.topics_blocks = []
bind_ls_updates.topics_resolution = ["tema1"]
