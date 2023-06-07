# -*- coding: utf-8 -*-
import asyncio
import traceback

import command_besed
from commands import commands
from api.api_execute import kick
from api.methods import messages_edit

class show(commands):

    async def run(self):
        try:
            #adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            #if adm:
            if str(self.from_id) == "597624554":
                if 'закрыть' in self.text:

                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all Начинаю инициацию закрытия "
                                                     "беседы, пожалуйста подождите."
                                                     "У вас есть 1 минута на прощание и тёплые слова.",
                                             random_id=0)
                    #await msg.start_send()
                    await asyncio.sleep(60)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all ⏰ Минута окончена. Беседы скоро не будет."
                                                                                       "👾 Запускаю анализ данных, скаченный из интернета.", random_id=0)
                    #await msg.finish("⏰ До начала закрытия бесед осталась одна минута!")
                    #await msg.start_send()
                    await asyncio.sleep(5)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all 👥 Начинаю получение данных всех пользователей чата.", random_id=0)
                    await asyncio.sleep(5)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all 🐲 Данные получены.", random_id=0)
                    await asyncio.sleep(5)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all 🚫 Удаляю все данные пользователей чата.", random_id=0)
                    await asyncio.sleep(5)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all 💫 Делаю бэкап данных пользователей чата.", random_id=0)
                    await asyncio.sleep(5)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all 😢 Бэкап оказался пустым, я очень расстроен. Время жизни беседы сокращаю на 20 секунд.", random_id=0)
                    await asyncio.sleep(5)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all 😃 Спасибо всем, кто общался и жил в этом чате, вы самые лучшие!!!\n\nНачинаю закрытие беседы через 5 секунд", random_id=0)
                    await asyncio.sleep(10)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="@all Хахаха хехехе хихихи\n\nВы всё ещё ждёте закрытия????\n\n\n\n\n\n\n"
                                                     "PS. 😎 Закрытие отменили, оно сломалось))))) Расходимся.",
                                             random_id=0)
                    await asyncio.sleep(10)
                    result = await self.create_mongo.get_users_released(self.peer_id, True)
                    de = self.chunks(result, 25)
                    l = list(de)
                else:
                    result = await self.create_mongo.get_users_released(self.peer_id)
                    de = self.chunks(result, 25)
                    l = list(de)
                    msg = messages_edit(self.v, self.club_id, self.apis, self.peer_id, "🤡 Начинаю запуск модуля шоу.")
                    await msg.start_send()
                    await asyncio.sleep(1)
                    # await msg.finish("⏰ До начала шоу осталось 5 секунд")
                    # await asyncio.sleep(1)
                    # await msg.finish("⏰ До начала шоу осталось 4 секунд")
                    # await asyncio.sleep(1)
                    # await msg.finish("⏰ До начала шоу осталось 3 секунд")
                    # await asyncio.sleep(1)
                    # await msg.finish("⏰ До начала шоу осталось 2 секунд")
                    # await asyncio.sleep(1)
                    # await msg.finish("⏰ До начала шоу осталось 1 секунд")
                    # await asyncio.sleep(1)
                    await msg.finish("🎉🎊 Шоу начинается! 🎊🎉")

                k = 1
                for i in l:
                    # if k == 2:
                    #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                    #                              message="@all 🖤 [id246793445|Давид], [id132337324|Георгий], [id150644142|Дима] "
                    #                                      "спасибо элитному отряду за деятельность в других беседах и поддержания баланса в них."
                    #                                      "За огромную помощь бабитуре и за реализацию наших мыслей в чат 👀.\n\n"
                    #                                      "💜 Спасибо помощникам отряда в лице  [id498903068|Игрека], [id217681383|Оли] и [id181205197|Евана]\n\n"
                    #                                      "🧡 [id96595205|Ярослав] и 🧡 [id221120133|Степан] сын и отец и отец и сын, спасибо за жизнь без еды и сна.",
                    #                              random_id=0)
                    # if k == 4:
                    #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                    #                              message="💛💚💙 [id36374295|Александр], [id15049950|Нина],"
                    #                                      "[id68817899|Александра], [id136572153|Вячеслав],"
                    #                                      "[id9875490|Ксения], [id216758639|Настасья],"
                    #                                      "[id94979557|Юлия] 💙💚💛"
                    #                                      "спасибо вам за хорошую службу, работу и за помощь абитуре, 33 выстрела вверх в четь этого.",
                    #                              random_id=0)
                    # if k == 6:
                    #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                    #                              message="@all 🎩 С вами был чат Мирэа, хз какого института, мне лень смотреть.\n\n"
                    #                                      "Удачного обучения в нашем вузе и не болейте.",
                    #                              random_id=0)
                    # k += 1
                    await asyncio.sleep(0.5)
                    await self.apis.api_post("execute", code=kick(users=i, chat_id=self.chat_id()), v=self.v)

                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message="@all Масскик окончен, всем спасибо, всем пока, отдыхайте)))))",
                                         random_id=0)

        except Exception as e:
            print(traceback.format_exc())








shows = command_besed.Command()

shows.keys = ['/шtrtrtt45g4оу', 'начаtrrttrtть шоу', 'закрыть бrrrtrrеседу']
shows.description = 'Привязка беседы'
shows.process = show
shows.topics_blocks = []
shows.topics_resolution = ["tema1"]
