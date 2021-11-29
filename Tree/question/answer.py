from commands import commands
import command_ls


class answer(commands):

    async def run(self):
        #vopr = await self.create_mongo.questions_get_abitur(self.apis, self.v, self.peer_id, "bachelors")
        #await self.create_mongo.add_users_ls_status(self.from_id, nap="bachelors")
        txt = self.text.lower()
        if self.is_int(txt):
            if int(txt) > 0:
                documents = await self.create_mongo.get_users_ls_status(self.from_id, nap=True)
                otvet = self.create_mongo.questions_get_one(txt, documents=documents)
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"{otvet}",
                                         random_id=0)


answers = command_ls.Command()

answers.keys = []
answers.description = 'Ответ админа на вопрос'
answers.name = 'answer'
#answers.set_dictionary('answer')
answers.process = answer
answers.topics_blocks = []
answers.topics_resolution = ["tema1", "mirea_official"]
