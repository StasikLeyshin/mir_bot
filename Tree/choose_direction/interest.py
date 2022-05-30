from commands import commands
import command_ls


class interest(commands):

    async def run(self):

        await self.create_mongo.setting_value_profile_ls(self.from_id, directions="finish",
                                                         interest=self.text)
        res = await self.create_mongo.get_value_profile_ls(self.from_id, directions="finish")

        #print(res)

        msg = await self.strategic_directions(res['place'], level=res['level'])

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
        #await self.step_back_bool()

        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                          message="📚 Выбери, что тебя интересует, чему бы ты хотел учиться.",
        #                          random_id=0,
        #                          keyboard=self.level_select_interests())


interests = command_ls.Command()

interests.keys = ['IT и анализ данных', 'Химия и биотехнология', 'Информационная/компьютерная безопасность',
                  'Радиоэлектроника', 'Робототехника и автоматизация', 'Экономика и управление',
                  'Дизайн', 'Юриспруденция']
interests.description = 'Подобрать направление по интересу'
interests.set_dictionary('interest')
interests.process = interest
interests.topics_blocks = []
interests.topics_resolution = ["tema1"]
