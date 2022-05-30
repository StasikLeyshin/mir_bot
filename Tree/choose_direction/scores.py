import command_ls
from commands import commands
from sql import pol_js


class scores(commands):

    async def run(self):

        await self.create_mongo.setting_value_profile_ls(self.from_id, directions="finish",
                                                         exam=self.text)
        res = await self.create_mongo.get_value_profile_ls(self.from_id, directions="finish")

        msg = await self.strategic_directions_exam(place=res['place'], level=res['level'])

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


        # check = self.create_mongo.check_predmet(self.peer_id)
        # self.create_mongo.add_user(self.peer_id, 0)
        # predmets = self.subjects_opposite[self.text].split("&")
        # # predmets = check.split("&")
        # # print(check, predmets)
        # pol_sql = pol_js(predmets[0], predmets[1], predmets[2], "310", 1)
        # if pol_sql["quantity"] != 0:
        #     spis = []
        #     for i in pol_sql["programs"]:
        #         spis.append(
        #             f"🔮 {i['name']} {i['code']}\n📊 Прошлогодний проходной балл на бюджет: {i['bal']}\n"
        #             f"👥 Количество бюджетных мест: {i['places']}\nСсылка на более подробную информацию: {i['link']}")
        #     de = self.chunks(spis, 10)
        #     l = list(de)
        #     # print(len(l))
        #     # print(l)
        #
        #     ff = 1
        #     perv = "🔎 Высокие шансы поступления:\n\n"
        #     if pol_sql["quantity"] == -1:
        #         perv = "🔎 Гарантированное поступление на платное обучение, но на бюджет в прошлом году баллы были выше.\n\n"
        #     f = 1
        #     for i in l:
        #         if f == 1:
        #             await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                                      message=perv + "\n\n".join(i),
        #                                      random_id=0)
        #         elif f == len(l):
        #             await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                                      message="\n\n".join(i),
        #                                      random_id=0,
        #                                      keyboard=self.menu_incomplete())
        #         else:
        #             await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                                      message="\n\n".join(i),
        #                                      random_id=0)
        #         f += 1

        # self.create_mongo.edit_user(self.peer_id, self.subjects_opposite[self.text])

        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                          message="🧭 Введите сумму всех результатов ваших экзаменов\n\n"
        #                                  f"📚 Выбранные предметы: {self.subjects[self.text]}",
        #                          random_id=0,
        #                          keyboard=self.menu())


score = command_ls.Command()

score.keys = ["Рус + мат(проф.) + инф", "Рус + мат(проф.) + физ", "Рус + мат(проф.) + общ", "Рус + мат(проф.) + хим",
              "Рус + общ + ист", "Рус + общ + твор", "Рус + мат(проф.) + твор", "Рус + мат(проф.) + гео",
              "Рус + инф + гео"]
score.description = 'Направления'
score.set_dictionary('scores')
score.process = scores
score.topics_blocks = []
score.topics_resolution = ["tema1"]
