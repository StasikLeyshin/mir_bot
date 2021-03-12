
import datetime

import command_ls
from commands import commands


class rating(commands):

    async def run(self):

        #self.create_mongo.questions_get()
        ret = self.create_mongo.rating(self.from_id)
        #print(ret)
        #d = datetime.strptime(ret["date_editing"], '%a %b %d %Y %H:%M:%S %Z 0300')
        #print(d)
        date = ret["date_editing"].strftime('%m.%d.%Y')
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=f"✅ Баллы доверия прибавляются:\n\n"
                                         f"➕ 3 за посещение очного мастер-класса/тренинга;\n\n"
                                         f"➕ 2 за посещение онлайн мастер-класса/тренинга;\n\n"
                                         f"➕ 4 за посещение очного занятия с кураторами;\n\n"
                                         f"➕ 3 за посещение онлайн занятия с кураторами;\n\n"
                                         f"➕ 5 за посещение очных мероприятий в выходной день;\n\n"
                                         f"➕ 4 за выполнение домашнего задания;\n\n"
                                         f"➕ 1 за посещение всех мероприятий на неделе;\n\n"
                                         f"➕ 1 за активность в течение онлайн встречи (оценка куратора/тренера);\n\n"
                                         f"➕ (1-5) за активность на очном занятии с куратором;\n\n"
                                         f"❌ Баллы доверия списываются:\n\n"
                                         f"➖ 5 за неявку на мастер-класс/тренинг с ограниченными местами без предупреждения заранее (за 3 часа до начала мастер-класса);\n\n"
                                         f"➖ 3 за нарушение норм поведения (нецензурная брань, хамство, неуважение по отношению к другим слушателям школы и ее организаторам и т.д.);\n\n"
                                         f"➖ 2 за невыполнение домашнего задания\n\n"
                                         f"📊 Ваш текущий рейтинг: {ret['rating']}\n⌚ Последнее обновление: {date}",
                                 random_id=0)



ratings = command_ls.Command()

ratings.keys = ['/рейтинг', '/рет', 'рейтинг']
ratings.description = 'Рейтинг'
ratings.process = rating
ratings.topics_blocks = []
ratings.topics_resolution = ["consultants"]
