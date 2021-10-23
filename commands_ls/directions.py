import command_ls
from commands import commands


class directions(commands):

    async def run(self):

        self.create_mongo.add_user(self.peer_id, 1)
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message="💡 Для выбора сданных вами предметов используйте соответствующие кнопки.\n\n",
                                 random_id=0,
                                 keyboard=self.direction())


direction = command_ls.Command()

direction.keys = ['напркер', 'направленияер', 'направлениенер']
direction.description = 'Направления'
direction.process = directions
direction.topics_blocks = []
direction.topics_resolution = ["tema1"]
