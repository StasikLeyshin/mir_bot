from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.punishments.unban import UnbanLs



class Shop(commands):

    async def run(self):pass




Shops = command_ls.Command()

Shops.keys = ['магазин']
Shops.description = 'разбан'
Shops.set_dictionary('shop')
Shops.process = Shop
Shops.mandatory = True
Shops.topics_blocks = []
Shops.topics_resolution = ["tema1"]
