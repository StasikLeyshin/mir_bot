import command_ls
from commands import commands


class scores(commands):

    async def run(self):
        chek = self.create_mongo.check_user(self.peer_id)

        if chek == 1:
            self.create_mongo.add_user(self.peer_id, 2)
            self.create_mongo.edit_user(self.peer_id, self.subjects_opposite[self.text])

            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="🧭 Введите сумму всех результатов ваших экзаменов\n\n"
                                             f"📚 Выбранные предметы: {self.subjects[self.text]}",
                                     random_id=0,
                                     keyboard=self.menu())



score = command_ls.Command()

score.keys = ["Рус + мат(проф.) + инф", "Рус + мат(проф.) + физ", "Рус + мат(проф.) + общ", "Рус + мат(проф.) + хим",
              "Рус + общ + ист", "Рус + общ + твор", "Рус + мат(проф.) + твор"]
score.description = 'Направления'
score.process = scores
score.topics_blocks = []
score.topics_resolution = ["tema1"]
