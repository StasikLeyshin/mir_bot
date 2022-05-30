from commands import commands
import command_ls
from api import api_url


class questions_survey(commands):


    async def run(self):
        result = await api_url(f"{self.url_dj}poll").post_json(name=self.text.lower())
        if result["status"] == "0":
            await self.step_back_bool()
            return



        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="Опросы",
                                 random_id=0,
                                 keyboard=self.level_where_study())


questions_surveys = command_ls.Command()

questions_surveys.keys = ['']
questions_surveys.mandatory = True
questions_surveys.description = 'Ответы на вопросы опроса'
questions_surveys.set_dictionary('questions_survey')
questions_surveys.process = questions_survey
questions_surveys.topics_blocks = []
questions_surveys.topics_resolution = ["tema1"]
