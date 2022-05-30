import asyncio
import traceback
import traceback
import os
import urllib.request
import random
from random import randint
import re
import asyncio

import command_besed
from commands import commands
from photos import text_photo
from record_achievements import achievements


class RegexpProc(object):

    PATTERN_1 = r''.join((
        r'\w{0,5}[хx]([хx\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[уy]([уy\s\!@#\$%\^&*+-\|\/]{0,6})[ёiлeеюийя]\w{0,7}|\w{0,6}[пp]',
        r'([пp\s\!@#\$%\^&*+-\|\/]{0,6})[iие]([iие\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[3зс]([3зс\s\!@#\$%\^&*+-\|\/]{0,6})[дd]\w{0,10}|[сcs][уy]',
        r'([уy\!@#\$%\^&*+-\|\/]{0,6})[4чkк]\w{1,3}|\w{0,4}[bб]',
        r'([bб\s\!@#\$%\^&*+-\|\/]{0,6})[lл]([lл\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[yя]\w{0,10}|\w{0,8}[её][bб][лске@eыиаa][наи@йвл]\w{0,8}|\w{0,4}[еe]',
        r'([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[uу]([uу\s\!@#\$%\^&*+-\|\/]{0,6})[н4ч]\w{0,4}|\w{0,4}[еeё]',
        r'([еeё\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[нn]([нn\s\!@#\$%\^&*+-\|\/]{0,6})[уy]\w{0,4}|\w{0,4}[еe]',
        r'([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[оoаa@]([оoаa@\s\!@#\$%\^&*+-\|\/]{0,6})[тnнt]\w{0,4}|\w{0,10}[ё]',
        r'([ё\!@#\$%\^&*+-\|\/]{0,6})[б]\w{0,6}|\w{0,4}[pп]',
        r'([pп\s\!@#\$%\^&*+-\|\/]{0,6})[иeеi]([иeеi\s\!@#\$%\^&*+-\|\/]{0,6})',
        r'[дd]([дd\s\!@#\$%\^&*+-\|\/]{0,6})[oоаa@еeиi]',
        r'([oоаa@еeиi\s\!@#\$%\^&*+-\|\/]{0,6})[рr]\w{0,12}',
    ))

    PATTERN_2 = r'|'.join((
        r"(\b[сs]{1}[сsц]{0,1}[uуy](?:[ч4]{0,1}[иаakк][^ц])\w*\b)",
        r"(\b(?!пло|стра|[тл]и)(\w(?!(у|пло)))*[хx][уy](й|йа|[еeё]|и|я|ли|ю)(?!га)\w*\b)",
        r"(\b(п[oо]|[нз][аa])*[хx][eе][рp]\w*\b)",
        r"(\b[мm][уy][дd]([аa][кk]|[oо]|и)\w*\b)",
        r"(\b\w*д[рp](?:[oо][ч4]|[аa][ч4])(?!л)\w*\b)",
        r"(\b(?!(?:кило)?[тм]ет)(?!смо)[а-яa-z]*(?<!с)т[рp][аa][хx]\w*\b)",
        r"(\b[к|k][аaoо][з3z]+[eе]?ё?л\w*\b)",
        r"(\b(?!со)\w*п[еeё]р[нд](и|иc|ы|у|н|е|ы)\w*\b)",
        r"(\b\w*[бп][ссз]д\w+\b)",
        r"(\b([нnп][аa]?[оo]?[xх])\b)",
        r"(\b([аa]?[оo]?[нnпбз][аa]?[оo]?)?([cс][pр][аa][^зжбсвм])\w*\b)",
        r"(\b\w*([оo]т|вы|[рp]и|[оo]|и|[уy]){0,1}([пnрp][iиеeё]{0,1}[3zзсcs][дd])\w*\b)",
        r"(\b(вы)?у?[еeё]?би?ля[дт]?[юоo]?\w*\b)",
        r"(\b(?!вело|ски|эн)\w*[пpp][eеиi][дd][oaоаеeирp](?![цянгюсмйчв])[рp]?(?![лт])\w*\b)",
        r"(\b(?!в?[ст]{1,2}еб)(?:(?:в?[сcз3о][тяaа]?[ьъ]?|вы|п[рp][иоo]|[уy]|р[aа][з3z][ьъ]?|к[оo]н[оo])?[её]б[а-яa-z]*)|(?:[а-яa-z]*[^хлрдв][еeё]б)\b)",
        r"(\b[з3z][аaоo]л[уy]п[аaeеин]\w*\b)",
    ))

    regexp = re.compile(PATTERN_1, re.U | re.I)

    @staticmethod
    def test(text):
        return bool(RegexpProc.regexp.findall(text))

    @staticmethod
    def replace(text, repl='[censored]'):
        return RegexpProc.regexp.sub(repl, text)

    @staticmethod
    def wrap(text, wrap=('<span style="color:red;">', '</span>',)):
        words = {}
        for word in re.findall(r'[А-яA-z0-9\-]+', text):
            if len(word) < 3:
                continue
            if RegexpProc.regexp.findall(word):
                words[word] = u'%s%s%s' % (wrap[0], word, wrap[1],)
        for word, wrapped in words.items():
            text = text.replace(word, wrapped)
        return text


class message_analysis(commands):

    async def downland_photo(self, g_url, rand_name):
        urllib.request.urlretrieve(g_url, rand_name)

    async def run(self, bad_words):
        try:
            if self.peer_id == 2000000024:
                return

            type_sms = "text"
            res = await achievements(int(self.from_id), self.v).add_sms(self.apis, self.peer_id, type_sms)
            if res:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=res, random_id=0, forward=self.answer_msg())






            kol_sms = await self.create_mongo.profile_users_add(self.from_id, sms=1)
            if kol_sms in self.sms_awards:
                res = await self.create_mongo.profile_users_add(self.from_id, f"🏆 {self.sms_awards[int(kol_sms)][0]}",
                                                                self.sms_awards[int(kol_sms)][1])
                ach = f"👻 [id{self.from_id}|Вы] получили ачивку:\n\n🏆 {self.sms_awards[int(kol_sms)][0]}\n\n📊 Рейтинг: {res[1]}"
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=ach, random_id=0, forward=self.answer_msg())
            flag = False
            flag_new = False
            for i in bad_words:
                for j in self.text.lower().split(" "):

                    if not flag_new:
                        if RegexpProc.test(j):
                            flag_new = True
                    if i in self.text.lower():
                        if i == j:
                            flag = True
                            break
            if not flag:
                try:
                    adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
                    if not adm:
                        if len(self.message["attachments"]) != 0:
                            for i in self.message["attachments"]:
                                if "photo" in i:
                                    rand = randint(0, 9999999999)
                                    rand_name = f"{self.peer_id}_{self.from_id}_{self.date}_{rand}.jpg"
                                    g = await self.photo_r_json(i["photo"]["sizes"])
                                    g_url = g["url"]
                                    await self.downland_photo(g_url, rand_name)
                                    # urllib.request.urlretrieve(g_url, rand_name)
                                    txt = await text_photo().run(rand_name)
                                    os.remove(rand_name)
                                    for i in bad_words:
                                        for j in txt.lower().split(" "):
                                            if not flag_new:
                                                if RegexpProc.test(j):
                                                    flag_new = True
                                            if i in txt.lower():
                                                if i == j:
                                                    flag = True
                                                    break
                                    if flag:
                                        break
                except Exception as e:
                    print(traceback.format_exc())
            if flag:
                adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
                try:
                    if not adm:
                        vrem = 86400
                        cause = "Использование ненормативной лексики"
                        ply = await self.display_time(vrem)
                        result = await warn_give_out(self.v).ban_give(self.apis, self.create_mongo, self.peer_id, cause,
                                                                      self.chat_id(), str(self.from_id), "-5411326",
                                                                      vrem, ply)

                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message=result[1], random_id=0, forward=self.answer_msg())

                        if len(result) == 3:
                            loop = asyncio.get_running_loop()
                            for i in result[2]:
                                try:
                                    loop.create_task(
                                        self.apis.api_post("messages.removeChatUser", chat_id=self.chat_id_param(i),
                                                           member_id=self.from_id,
                                                           v=self.v))
                                except:
                                    pass
                            return

                        if result[0]:
                            await self.apis.api_post("execute", code=kick(users=[self.from_id], chat_id=self.chat_id()),
                                                     v=self.v)
                except Exception as e:
                    print(traceback.format_exc())

            elif flag_new:
                adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
                if not adm:
                    result = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                                      peer_ids=str(self.peer_id))
                    name = result["items"][0]['chat_settings']['title']
                    # result_id = await self.apis.api_post("messages.getByConversationMessageId", v=self.v,
                    # peer_id=self.peer_id,
                    # conversation_message_ids=[self.conversation_message_id])
                    # print(result_id)
                    # m_id = result_id["items"][0]["id"]
                    await self.apis.api_post("messages.send", v=self.v, peer_id=2000000024,
                                             message=f"⚠ Обнаружено подозрение на мат от данного [id{self.from_id}|пользователя]\n\n"
                                                     f"👥 Беседа: '{name}'\n\n"
                                                     f"Заварнить?",
                                             random_id=0, keyboard=self.keyboard_warn(
                            f"{self.from_id}@{self.date}@{self.conversation_message_id}"),
                                             forward=self.answer_msg_other())
                    await self.create_mongo.add_users_zawarn(self.from_id, self.date, self.peer_id)
        except Exception as e:
            print(traceback.format_exc())


message_analysiss = command_besed.Command()

message_analysiss.keys = [' ']
message_analysiss.description = 'Выдача бана'
message_analysiss.set_dictionary('ban')
message_analysiss.mandatory = True
message_analysiss.process = message_analysis
message_analysiss.topics_blocks = []
message_analysiss.topics_resolution = ["tema1"]
