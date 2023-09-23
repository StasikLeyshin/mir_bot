from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.punishments.unban import UnbanLs
from summer_module.statistics.statistics import Statistics
from summer_module.user_profile import UserProfile
from summer_module.work_ls.work_ls import WorkLs
from api import api, api_url


class StatisticsLs(commands):

    async def run(self):

        text_list = self.text.lower().split(' ')

        peer_id = text_list[1]
        type_statistics = text_list[2]
        start_time = text_list[3]
        finish_time = text_list[4]

        statistics_ls = Statistics(self.mongo_manager, self.settings_info, self.from_id, self.date)
        result = await statistics_ls.run(peer_id=int(peer_id), type_statistics=type_statistics,
                                         start_time=start_time, finish_time=finish_time)

        #print(result["name_file"])

        link = await self.apis.api_post("docs.getMessagesUploadServer", v=self.v, peer_id=self.from_id, type="doc")
        #print(link)

        file = await api_url(link['upload_url']).post_upload(result["name_file"])
        #print(file)

        doc_save = await self.apis.api_post("docs.save", v=self.v, file=file['file'],
                                            title=f"Отчёт_{start_time}_{finish_time}")
        #print(doc_save)
        doc_save = doc_save['doc']
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                 message=result["message"], random_id=0,
                                 attachment=f"doc{doc_save['owner_id']}_{doc_save['id']}")






statistics_lss = command_ls.Command()

statistics_lss.keys = ['/stat', '/статистика']
statistics_lss.description = 'статистика'
statistics_lss.process = StatisticsLs
#endless_questionss.mandatory = True
statistics_lss.topics_blocks = []
statistics_lss.topics_resolution = ["tema1"]

