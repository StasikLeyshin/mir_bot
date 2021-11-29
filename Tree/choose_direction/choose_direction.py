from commands import commands
import command_ls


class choose_direction(commands):

    async def run(self):

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="📚 Выбери нужный вариант",
                                 random_id=0,
                                 keyboard=self.level_choose_direction())


choose_directions = command_ls.Command()

choose_directions.keys = ['Подобрать направление']
choose_directions.description = 'Подобрать направление'
choose_directions.set_dictionary('choose_direction')
choose_directions.process = choose_direction
choose_directions.topics_blocks = []
choose_directions.topics_resolution = ["tema1"]
