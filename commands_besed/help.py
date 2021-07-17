
import command_besed
from commands import commands
from api.methods import messages_edit

class chance(commands):

    async def run(self):
        if self.ls_open_check(self.from_id):
            msg = "/профиль [ссылка|упомянание|пересланное сообщение] — показывает профиль участника, если он есть в одном из наших чатов (по умолчанию или если у вас меньше нужного количаства баллов показывает ваш профиль)\n\n" \
                  "+реп [ссылка|упомянание|пересланное сообщение] — повышает репутацию выбранного участника на 0.25 рейтинга\n" \
                  "-реп [ссылка|упомянание|пересланное сообщение] — понижает репутацию выбранного участника на 0.25 рейтинга (при условии набранных баллов)\n" \
                  "таймреп [ссылка|упомянание|пересланное сообщение] — показывает сколько поднятия или опускания репутации у вас доступно\n\n" \
                  "/шанс — создаёт из песка и пыли шанс (при условии набранных баллов)\n\n" \
                  "/рейтинг — показывает топ 25 человек в рейтинге (при условии набранных баллов)\n\n" \
                  "/команды — показывает все команды "
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                     message=msg, random_id=0)
        else:
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                     random_id=0)








chances = command_besed.Command()

chances.keys = ['/help', '/chance']
chances.description = 'Шанс поступления'
chances.process = chance
chances.topics_blocks = []
chances.topics_resolution = ["tema1"]
