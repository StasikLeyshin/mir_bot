
import traceback

import command_besed
from commands import commands
from summer_module.games.card_day import CardDay
from api import api, api_url


class roulette_new(commands):

    async def run(self):
        try:
            rep = CardDay(self.mongo_manager, self.settings_info, int(self.from_id), int(self.date))
            result = await rep.run(peer_id=int(self.peer_id))
            if result['message']:
                if await self.ls_open_check(self.from_id):
                    if not result['error']:
                        link = await self.apis.api_post("photos.getMessagesUploadServer", v=self.v,
                                                        peer_id=self.from_id)
                        #print(link)

                        file = await api_url(link['upload_url']).post_upload(result["file"])
                        #print(file)

                        doc_save = await self.apis.api_post("photos.saveMessagesPhoto", v=self.v, server=file['server'],
                                                            photo=file['photo'], hash=file['hash'])
                        #print(doc_save)
                        # doc_save = doc_save['doc']
                        #photo = await self.photo_r_json(doc_save)
                        #print(photo)
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                                 message=result["message"], random_id=0,
                                                 attachment=f"photo{doc_save[0]['owner_id']}_{doc_save[0]['id']}")
                        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                        #                          message=result['message'],
                        #                          random_id=0, forward=self.answer_msg(), keyboard=self.pusto())
                    else:

                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                                 message=result['message'],
                                                 random_id=0)
                else:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                             forward=self.answer_msg(),
                                             random_id=0)
            await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                     conversation_message_ids=self.conversation_message_id,
                                     delete_for_all=1)


        except Exception as e:
            print(traceback.format_exc())


roulette_news = command_besed.Command()

roulette_news.keys = ['/картадна', '/cardday', '/карта дня', 'card day', '/картадня']
roulette_news.description = 'Карта дня'
roulette_news.set_dictionary('card_day')
roulette_news.process = roulette_new
roulette_news.topics_blocks = []
roulette_news.topics_resolution = ["tema1"]
