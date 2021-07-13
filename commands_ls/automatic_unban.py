
import asyncio
import traceback

import command_ls
from commands import commands
from api import api


class automatic_unban(commands):

    async def run(self):
        try:
            slov = await self.create_mongo.ban_chek(self.from_id)
            print(slov)
            if len(slov["peer_ids"]) > 0:
                result = await self.apis.api_post("messages.getConversationsById", v=self.v, peer_ids=", ".join(slov["peer_ids"]))
                names = []
                j = 1
                for i in result["items"]:
                    names.append(f"{j}. {i['chat_settings']['title']}")
                    j += 1
                api_new = api(self.club_id, "7e57e7ab0bd4508a517b94cd935cea6c7f41698d363994ecfa6a77671a32a8fb7441297abf5ae785e254a")
                res = await api_new.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                       message="🕵 Вы попали в секретный раздел, сообщения здесь самоуляются через 1 минуту.\n"
                                               "⚠ Если вы не успеете ответить на любое сообщение из этого раздела, не включая это, "
                                               "ваша единственная попытка разбана на одну беседу сгорит.\n"
                                               "Вам необходимо пройти тест из 8 вопросов.\n"
                                               "Чтобы попасть в Программу, ответьте правильно на 5.\n"
                                               "Для ответа на вопрос отправьте сообщение с выбранным номером ответа.\n"
                                               "После выбора беседы начнётся сразу начнётся тест.\n"
                                               "Выберите номер беседы, в которой вас необходимо разбанить, "
                                               "показаны только те беседы, где доступна попытка разбана:\n" +
                                               "\n".join(names),
                                       random_id=0, expire_ttl=60, keyboard=self.keyboard_empty())

                self.create_mongo.add_user(self.peer_id, 4, 1, self.date, slov)
                #await asyncio.sleep(65)
        except Exception as e:
            print(traceback.format_exc())







automatic_unbans = command_ls.Command()

automatic_unbans.keys = ['разбан', 'разбанить']
automatic_unbans.description = 'Разбан'
automatic_unbans.process = automatic_unban
automatic_unbans.topics_blocks = []
automatic_unbans.topics_resolution = ["tema1"]
