from commands import commands
import command_ls


class want_university(commands):

    async def run(self):
        msg = ""
        if self.them == "mirea_official":
            msg = "💡 Для того, чтобы получать актуальную информацию по поступлению подпишитесь на сообщество Абитуриенту РТУ МИРЭА:\nhttps://vk.com/priem_mirea\n\n"

        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=f"{msg}📈 Выберите уровень обучения",
                                 random_id=0,
                                 keyboard=self.level_education_q())

want_universitys = command_ls.Command()

want_universitys.keys = ['Хочу поступать в вуз']
want_universitys.description = 'Вопросы'
want_universitys.set_dictionary('want_university')
want_universitys.process = want_university
want_universitys.topics_blocks = []
want_universitys.topics_resolution = ["tema1", "mirea_official"]
