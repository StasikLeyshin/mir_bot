from commands import commands
import command_ls
from api import api_url

class survey(commands):


    async def run(self):

        result = await api_url(f"{self.url_dj}poll").get_json()
        if result["status"] == "0":
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="К сожалению опросов сейчас нет:(",
                                     random_id=0)
            await self.step_back_bool()
            return
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=#"Начнём опрос, выход из опроса по нажатию кнопки Меню."
                                         "📊 Выберите опрос, который хотите пройти.",
                                 random_id=0,
                                 keyboard=self.menu_naked_survey(result["polls"]))


surveys = command_ls.Command()

surveys.keys = ['пройти опрос о мероприятиях', 'опрос']
surveys.description = 'Опросы'
surveys.set_dictionary('survey')
surveys.process = survey
surveys.topics_blocks = []
surveys.topics_resolution = ["tema1"]
