import asyncio
import traceback
import traceback
import os
import urllib.request
import random
from random import randint
import re
import asyncio

import aiofiles
import aiohttp

from api.api_execute import kick
#import command_besed
from commands import commands
from edite_text import URL_REGEX, positive_negative_comment_check
from photos import text_photo
from record_achievements import achievements

from summer_module import MessageAnalysis, WarnAdminCheck


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


class MessageAnalysisProcessing(commands):

    async def downland_photo(self, g_url, rand_name):

        async with aiohttp.ClientSession() as session:
            async with session.get(g_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(rand_name, mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        #urllib.request.urlretrieve(g_url, rand_name)

    async def run123(self):pass
    async def run(self):
        #print(self.message)
        if self.peer_id == 2000000039 or "action" in self.message:
            return
        f1 = open("ploxie_slova.txt", "r+", encoding="utf8")
        d1 = f1.readlines()
        f1.close()
        bad_words = d1[0].split(', ')

        us = None
        flag = False
        flag_new = False
        flag_per = False
        type_sms = "text"

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
                #adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
                #if not adm or adm:
                if len(self.message["attachments"]) != 0:
                    for i in self.message["attachments"]:
                        if "photo" in i:
                            rand = randint(0, 9999999999)
                            rand_name = f"{self.peer_id}_{self.from_id}_{self.date}_{rand}.jpg"
                            g = await self.photo_r_json(i["photo"]["sizes"])
                            g_url = g["url"]
                            await self.downland_photo(g_url, rand_name)
                            #urllib.request.urlretrieve(g_url, rand_name)
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
                            if flag:
                                break
                            type_sms = "photo"
                        if "sticker" in i:
                            type_sms = "sticker"
                        if "audio_message" in i:
                            type_sms = "sms_voice"
                elif self.fwd_messages and not flag:
                    if not flag_new:
                        #print(self.fwd_messages)
                        for j in self.fwd_messages:
                            for i in bad_words:
                                for k in j['text'].lower().split(" "):
                                    if not flag_new:
                                        if RegexpProc.test(k):
                                            flag_new = True
                                    if i in j['text'].lower():
                                        if i == k:
                                            flag_per = True
                                            break
                                if flag_per:
                                    break
                            if flag_per:
                                break
                elif "reply_message" in self.message and not flag and not flag_per:
                    if not flag_new:
                        for i in bad_words:
                            for j in self.message["reply_message"]["text"].lower().split(" "):
                                if not flag_new:
                                    if RegexpProc.test(j):
                                        flag_new = True
                                if i in self.message["reply_message"]["text"].lower():
                                    if i == j:
                                        flag_per = True
                                        break
                            if flag_per:
                                break

            except Exception as e:
                print(traceback.format_exc())

        res = re.findall(URL_REGEX, f'{self.text.lower()}')

        if flag:
            type_sms = "swear"
        elif flag_per:
            type_sms = "swear_forward_message"
        # elif res:
        #     type_sms = "sms_link"



        # if flag or flag_per:
        #     #adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
        #     type_sms = ""
        #     try:
        #
        #         #if not adm:
        #
        #             # type_sms = "mat"
        #             # #vrem = await self.preobrz(self.text)
        #             # vrem = 86400
        #             # #cause = await self.txt_warn(self.text)
        #             # if flag_per:
        #             #     cause = "Использование ненормативной лексики в пересланном сообщении"
        #             # else:
        #             #     cause = "Использование ненормативной лексики"
        #             # ply = await self.display_time(vrem)
        #             # us = achievements(self.client, int(self.from_id), self.v)
        #             # await us.add_warn(self.apis, self.peer_id, -5411326, vrem, cause, forward=self.answer_msg())
        #
        #
        #
        #     except Exception as e:
        #         print(traceback.format_exc())

        #print(type_sms)

        msg_analysis = MessageAnalysis(self.mongo_manager, self.settings_info, user_id=self.from_id,
                                current_time=self.date)
        result = await msg_analysis.run(peer_id=self.peer_id, type_sms=type_sms, message=self.message)

        #print(result)

        if result.get("is_delete"):
            res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{self.from_id}", name_case="nom")
            name = f'{res[0]["first_name"]} {res[0]["last_name"]}'
            await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                     conversation_message_ids=self.conversation_message_id,
                                     delete_for_all=1)
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=result["message"].format(name), random_id=0)
            result["message"] = ""
        if result.get("message"):
            res = await self.apis.api_post("users.get", v=self.v, user_ids=f"{self.from_id}", name_case="nom")
            name = f'{res[0]["first_name"]} {res[0]["last_name"]}'
            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=result["message"].format(name), random_id=0, forward=self.answer_msg())
        if result.get("kick_id"):
            await self.apis.api_post("execute", code=kick(users=result["kick_id"], chat_id=self.chat_id()),
                                     v=self.v)

        elif flag_new and not flag and not flag_per:
            #adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)

            if not result.get("admin"):

                result = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                                  peer_ids=str(self.peer_id))
                name = result["items"][0]['chat_settings']['title']
                #result_id = await self.apis.api_post("messages.getByConversationMessageId", v=self.v,
                                                  #peer_id=self.peer_id,
                                                  #conversation_message_ids=[self.conversation_message_id])
                #print(result_id)
                #m_id = result_id["items"][0]["id"]
                res = await self.apis.api_post("messages.send", v=self.v, peer_id=2000000039,#2000000024,
                                         message=f"⚠ Обнаружено подозрение на мат от данного [id{self.from_id}|пользователя]\n\n"
                                                 f"👥 Беседа: '{name}'\n\n"
                                                 f"Что с ним сделать?",
                                         random_id=0,
                                         keyboard=self.keyboard_warn(
                                             f"{self.from_id}@{self.date}@{self.conversation_message_id}@swear"),
                                         forward=self.answer_msg_other())
                #await self.create_mongo.add_users_zawarn(self.from_id, self.date, self.peer_id)

                #print(res)
                #try:
                zawarn = WarnAdminCheck(self.mongo_manager, self.settings_info, self.club_id, self.date)
                resu = await zawarn.add_zawarn(user_id=self.from_id, peer_id=self.peer_id,
                                        conversation_message_id_forward=self.conversation_message_id,
                                        conversation_message_id_original=res,
                                        type_sms="swear")
                # except Exception as e:
                #     print(traceback.format_exc())
                #print(resu)
        elif len(self.text.split(' ')) > 1:
            if not result.get("admin"):
                result = await positive_negative_comment_check(self.text)
                #print(result)
                if result:
                    result = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                                      peer_ids=str(self.peer_id))
                    name = result["items"][0]['chat_settings']['title']

                    res = await self.apis.api_post("messages.send", v=self.v, peer_id=2000000051,  # 2000000024,
                                             message=f"⚠ Обнаружено негативное высказывание от данного [id{self.from_id}|пользователя]\n\n"
                                                     f"👥 Беседа: '{name}'\n\n"
                                                     f"🔫 Что с ним сделать?",
                                             random_id=0,
                                             keyboard=self.keyboard_warn(
                                                 f"{self.from_id}@{self.date}@{self.conversation_message_id}@neg"),
                                             forward=self.answer_msg_other())
                    zawarn = WarnAdminCheck(self.mongo_manager, self.settings_info, self.club_id, self.date)
                    await zawarn.add_zawarn(user_id=self.from_id, peer_id=self.peer_id,
                                            conversation_message_id_forward=self.conversation_message_id,
                                            conversation_message_id_original=res,
                                            type_sms="neg")


        # if not type_sms:
        #     res = text_analysis(self.text).analysis()
        #     if res == 0.5:
        #         type_sms = "spam"
        #     else:
        #         type_sms = "text"
        # if us:
        #     res = await us.add_sms(apis=self.apis, peer_id=self.peer_id,
        #                      type_sms=type_sms, time_issuing=self.date)
        # else:
        #     res = await achievements(self.client, self.from_id, self.v).add_sms(
        #         apis=self.apis, peer_id=self.peer_id,
        #         type_sms=type_sms, time_issuing=self.date
        #     )
        # if res:
        #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                              message=res, random_id=0, forward=self.answer_msg())



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


# message_analysiss = command_besed.Command()
#
# message_analysiss.keys = [' ']
# message_analysiss.description = 'Выдача бана'
# message_analysiss.set_dictionary('ban')
# message_analysiss.mandatory = True
# message_analysiss.process = message_analysis
# message_analysiss.topics_blocks = []
# message_analysiss.topics_resolution = ["tema1"]
