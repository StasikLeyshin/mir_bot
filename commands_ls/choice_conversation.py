
import traceback
import asyncio
import random

from commands import commands
from api import api

class choice_conversation(commands):

    async def run(self):

        #chek_user = self.create_mongo.check_user_unban(self.from_id, self.date)
        #chek = self.create_mongo.check_user(self.peer_id)
        try:
            self.create_mongo.add_user(self.peer_id, 4, 2, self.date)
            ger = self.create_mongo.generation_questions(self.from_id, self.text)
            print("GER: ", ger)
            api_new = api(self.club_id,
                          "7e57e7ab0bd4508a517b94cd935cea6c7f41698d363994ecfa6a77671a32a8fb7441297abf5ae785e254a")
            if ger[0] == 2:
                await api_new.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                       message=f"Ответ принят.\n\n{ger[1]}",
                                       random_id=0, expire_ttl=60, keyboard=self.keyboard_empty())
            elif ger[0] == 3:
                await api_new.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                       message=f"{ger[1]}",
                                       random_id=0, expire_ttl=60, keyboard=self.keyboard_empty())
            elif ger[0] == -1:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                       message=f"Вы ответили на недостаточное количество вопросов, ваша попытка разбана сгорает🔥",
                                       random_id=0, keyboard=self.menu())
                self.create_mongo.null_attempt(self.from_id)
                return
            elif ger[0] == 1:
                result = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                                  peer_ids=f"{ger[1]}")
                name = result["items"][0]["chat_settings"]["title"]
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"💥 Поздравляю!\n\nПять правильных ответов у вас в кармане."
                                                 f"\n\nРазбанил вас в беседе «{name}»\n\n"
                                                 f"✉ Перешлите это сообщение любому из администраторов и вас добавят в беседу.",
                                         random_id=0, keyboard=self.menu())
                self.create_mongo.unban(self.from_id, ger[1])
                return

            # await asyncio.sleep(65)
            slych = random.randint(1, 999999999)
            self.create_mongo.check_user_unban(self.from_id, self.date, slych, True)
            await asyncio.sleep(61)
            res = self.create_mongo.check_user_unban(self.from_id, self.date, slych, False)
            if res[1] != slych or res[1] == 0:
                return
            print(res[1], slych)
            #print(res[0], self.date)
            #if int(res[0]) > int(self.date) + 60:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=f"⏰ Ваше время ... истекло.\n\n🚫 Попытка разбана анулирована.",
                                     random_id=0, keyboard=self.menu())
            self.create_mongo.null_attempt(self.from_id)

        except Exception as e:
            print(traceback.format_exc())






