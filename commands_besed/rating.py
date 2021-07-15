import traceback

import command_besed
from commands import commands

class rating(commands):

    async def run(self):pass


ratings = command_besed.Command()

ratings.keys = ['/рейтинг', '/rating']
ratings.description = 'Рейтинг'
ratings.process = rating
ratings.topics_blocks = []
ratings.topics_resolution = ["tema1"]
