from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.punishments.unban import UnbanLs
from summer_module.work_ls.work_ls import WorkLs
from api import api


class AutomaticUnban(commands):

    async def run(self):
        unban = UnbanLs(self.mongo_manager, self.settings_info, current_time=self.date)


        result = await unban.unban_all()





automatic_unbans = command_ls.Command()

automatic_unbans.keys = ['Разбанить всех', 'unban all']
automatic_unbans.description = 'разбан всех'
automatic_unbans.process = AutomaticUnban
#endless_questionss.mandatory = True
automatic_unbans.topics_blocks = []
automatic_unbans.topics_resolution = ["tema1"]
