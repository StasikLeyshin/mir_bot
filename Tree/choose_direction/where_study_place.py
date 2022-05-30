from commands import commands
import command_ls


class where_study_place(commands):


    async def run(self):
        #print(111111111)
        res = await self.create_mongo.get_value_profile_ls(self.from_id, directions=1)
        #print(res)
        if res:
            if res.get('place') and self.text.lower() == "шаг назад":
                place = res['place']
            else:
                place = self.place[self.text.lower()]
        else:
            place = self.place[self.text.lower()]
        await self.create_mongo.setting_value_profile_ls(self.from_id, directions=1,
                                                         place=place)

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="📚 Выбери нужный вариант",
                                 random_id=0,
                                 keyboard=self.level_choose_direction())


where_study_places = command_ls.Command()

where_study_places.keys = ['москва', 'фрязино', 'ставрополь']
where_study_places.description = 'Подобрать направление по интересу'
where_study_places.set_dictionary('where_study_place')
where_study_places.process = where_study_place
where_study_places.topics_blocks = []
where_study_places.topics_resolution = ["tema1"]
