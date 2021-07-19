# -*- coding: utf-8 -*-

import asyncio
import datetime as DT
from bs4 import BeautifulSoup
import traceback
import requests
from time import gmtime, strftime

from date_compare import date_compare
from api import api_url, api, photo_upload
from help_text import opredel_screen
from Telegram.bot_setting import bot

class infinity_beskon:

    def __init__(self, V, create_mongo, collection_django, apps, collection_bots, document_tokens, apis, st, url_dj):

        self.V = V
        self.create_mongo = create_mongo
        self.apps = apps
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.apis = apis
        self.st = st
        self.collection_django = collection_django
        self.url_dj = url_dj
        self.slov_directions_general = {}
        self.list_directions_general = []
        self.list_direction_dop = {}
        self.list_directions = [{'identifier': '1701894965225893174', 'title': 'Прикладная математика и информатика (Киб)', 'plan': '48', 'code': '01.03.02', 'general_plan': 58}, {'identifier': '1700361513988042038', 'title': 'Прикладная математика (ИТ)', 'plan': '24', 'code': '01.03.04', 'general_plan': 28}, {'identifier': '1700360591214947638', 'title': 'Статистика (ИТУ)', 'plan': '18', 'code': '01.03.05', 'general_plan': 32}, {'identifier': '1700361605881048374', 'title': 'Фундаментальная информатика и информационные технологии (КБСП)', 'plan': '16', 'code': '02.03.02', 'general_plan': 21}, {'identifier': '1700361649693699382', 'title': 'Химия (ИТХТ)', 'plan': '53', 'code': '04.03.01', 'general_plan': 67}, {'identifier': '1698268858631105846', 'title': 'Информатика и вычислительная техника (ИТ)', 'plan': '87', 'code': '09.03.01', 'general_plan': 115}, {'identifier': '1700361394138950966', 'title': 'Информатика и вычислительная техника (Киб)', 'plan': '153', 'code': '09.03.01', 'general_plan': 180}, {'identifier': '1700361765783645494', 'title': 'Информационные системы и технологии (КБСП)', 'plan': '231', 'code': '09.03.02', 'general_plan': 288}, {'identifier': '1700361828395167030', 'title': 'Информационные системы и технологии (РТС)', 'plan': '54', 'code': '09.03.02', 'general_plan': 60}, {'identifier': '1700361912410221878', 'title': 'Информационные системы и технологии (ФТИ)', 'plan': '51', 'code': '09.03.02', 'general_plan': 60}, {'identifier': '1700362013307350326', 'title': 'Прикладная информатика (ИТ)', 'plan': '184', 'code': '09.03.03', 'general_plan': 229}, {'identifier': '1700362082409557302', 'title': 'Программная инженерия (ИТ)', 'plan': '240', 'code': '09.03.04', 'general_plan': 298}, {'identifier': '1700362158971333942', 'title': 'Информационная безопасность (КБСП)', 'plan': '30', 'code': '10.03.01', 'general_plan': 44}, {'identifier': '1700362217000578358', 'title': 'Компьютерная безопасность (Киб)', 'plan': '32', 'code': '10.05.01', 'general_plan': 47}, {'identifier': '1700362246813691190', 'title': 'Информационная безопасность телекоммуникационных систем (Киб)', 'plan': '32', 'code': '10.05.02', 'general_plan': 49}, {'identifier': '1700362450358021430', 'title': 'Информационная безопасность автоматизированных систем (КБСП)', 'plan': '42', 'code': '10.05.03', 'general_plan': 54}, {'identifier': '1700362477555985718', 'title': 'Информационно-аналитические системы безопасности (КБСП)', 'plan': '31', 'code': '10.05.04', 'general_plan': 36}, {'identifier': '1700362501294697782', 'title': 'Безопасность информационных технологий в правоохранительной сфере (КБСП)', 'plan': '31', 'code': '10.05.05', 'general_plan': 39}, {'identifier': '1700362536269950262', 'title': 'Радиотехника (РТС)', 'plan': '36', 'code': '11.03.01', 'general_plan': 58}, {'identifier': '1700362577792511286', 'title': 'Инфокоммуникационные технологии и системы связи (РТС)', 'plan': '96', 'code': '11.03.02', 'general_plan': 119}, {'identifier': '1700362615293783350', 'title': 'Конструирование и технология электронных средств (РТС)', 'plan': '45', 'code': '11.03.03', 'general_plan': 58}, {'identifier': '1700362711047646518', 'title': 'Электроника и наноэлектроника (ФТИ)', 'plan': '24', 'code': '11.03.04', 'general_plan': 30}, {'identifier': '1700362763577109814', 'title': 'Радиоэлектронные системы и комплексы (РТС)', 'plan': '14', 'code': '11.05.01', 'general_plan': 59}, {'identifier': '1700362791098035510', 'title': 'Приборостроение (КБСП)', 'plan': '21', 'code': '12.03.01', 'general_plan': 28}, {'identifier': '1700362847057390902', 'title': 'Биотехнические системы и технологии (Киб)', 'plan': '45', 'code': '12.03.04', 'general_plan': 57}, {'identifier': '1700362893096168758', 'title': 'Лазерная техника и лазерные технологии (ФТИ)', 'plan': '42', 'code': '12.03.05', 'general_plan': 58}, {'identifier': '1700362929710345526', 'title': 'Электронные и оптико-электронные приборы и системы специального назначения (ФТИ)', 'plan': '15', 'code': '12.05.01', 'general_plan': 50}, {'identifier': '1700362957420014902', 'title': 'Машиностроение (ФТИ)', 'plan': '15', 'code': '15.03.01', 'general_plan': 22}, {'identifier': '1700363013105691958', 'title': 'Автоматизация технологических процессов и производств (Киб)', 'plan': '27', 'code': '15.03.04', 'general_plan': 35}, {'identifier': '1700363057406979382', 'title': 'Мехатроника и робототехника (Киб)', 'plan': '27', 'code': '15.03.06', 'general_plan': 33}, {'identifier': '1700363095337119030', 'title': 'Химическая технология (ИТХТ)', 'plan': '247', 'code': '18.03.01', 'general_plan': 306}, {'identifier': '1700363180783480118', 'title': 'Биотехнология (ИТХТ)', 'plan': '82', 'code': '19.03.01', 'general_plan': 103}, {'identifier': '1700363228772609334', 'title': 'Техносферная безопасность (ИТХТ)', 'plan': '32', 'code': '20.03.01', 'general_plan': 41}, {'identifier': '1700363268567117110', 'title': 'Материаловедение и технологии материалов (ФТИ)', 'plan': '43', 'code': '22.03.01', 'general_plan': 55}, {'identifier': '1700363307964214582', 'title': 'Стандартизация и метрология (ФТИ)', 'plan': '19', 'code': '27.03.01', 'general_plan': 25}, {'identifier': '1700363410621902134', 'title': 'Системный анализ и управление (Киб)', 'plan': '40', 'code': '27.03.03', 'general_plan': 50}, {'identifier': '1700641481938742582', 'title': 'Инноватика (ИТУ)', 'plan': '43', 'code': '27.03.05', 'general_plan': 55}, {'identifier': '1700641541179092278', 'title': 'Нанотехнологии и микросистемная техника (ФТИ)', 'plan': '20', 'code': '28.03.01', 'general_plan': 26}, {'identifier': '1700641579533905206', 'title': 'Технология художественной обработки материалов (ФТИ)', 'plan': '16', 'code': '29.03.04', 'general_plan': 21}, {'identifier': '1701637932235926838', 'title': 'Управление персоналом (ИТУ)', 'plan': '0', 'code': '38.03.03', 'general_plan': 0}, {'identifier': '1700641782685019446', 'title': 'Экономическая безопасность (КБСП)', 'plan': '2', 'code': '38.05.01', 'general_plan': 3}, {'identifier': '1700641803721551158', 'title': 'Юриспруденция (ИТУ)', 'plan': '8', 'code': '40.03.01', 'general_plan': 12}, {'identifier': '1700641839206411574', 'title': 'Правовое обеспечение национальной безопасности (КБСП)', 'plan': '5', 'code': '40.05.01', 'general_plan': 9}, {'identifier': '1700641870393158966', 'title': 'Документоведение и архивоведение (ИТУ)', 'plan': '11', 'code': '46.03.02', 'general_plan': 14}, {'identifier': '1700641902061202742', 'title': 'Дизайн (ФТИ)', 'plan': '3', 'code': '54.03.01', 'general_plan': 5}]

    async def current_time(self):
        tek = DT.datetime.now()
        dt = DT.datetime.fromisoformat(tek.strftime('%Y-%m-%d %H:%M:%S'))
        return str(dt.timestamp())[:-2]


    async def generate(self, st):
        thems = {}
        for i in st:
            if i["them"] in thems:
                thems[i["them"]].append(i["id"])
            elif i["them"] not in thems:
                thems[i["them"]] = [i["id"]]
        return thems


    async def send(self, kwargs, club_id, peer_id, text, post):
        for i in range(9):
            #print(kwargs)
            image = kwargs[f"image_{i+1}"]
            if image != "0":
                res = await photo_upload(self.apis[int(club_id)], self.V, peer_id, kwargs[f"image_{i+1}"],
                                         '/home/stas/mir_bot/media/').upload()
                #res = await photo_upload(self.apis[int(club_id)], self.V, peer_id, "2021/06/29/28ae1abb0bcacd6e81ad2de947ba86da.jpg",
                                         #"/home/stas/mir_bot/media/").upload()
                if res != None:
                    if len(post) > 1:
                        post += f",{res}"
                    else:
                        post += f"{res}"
        #print(post)
        await self.apis[int(club_id)].api_post("messages.send", v=self.V, peer_id=peer_id, random_id=0, message=text, attachment=post)

    async def send_telegram(self, chat_id, text):
        bot.send_message(chat_id, f"{text}")

    async def dispatch(self, kwargs, spis_ras, gen, id_ras):
        loop = asyncio.get_running_loop()
        post = kwargs["post"]
        if len(post) > 1:
            post = await opredel_screen(post)
        text = kwargs["text"]
        for i in spis_ras:
            if i in gen:
                for j in gen[i]:
                    #peer_id = self.create_mongo.get_peer_id(self.collection_bots, self.document_tokens, j)
                    peer_id = self.create_mongo.get_peer_id_new(self.collection_django, self.apps, j, id_ras)
                    #print(peer_id)
                    if peer_id[0] != "0":
                        for i in peer_id:
                            if int(i) > 0:
                                loop.create_task(self.send(kwargs, j, int(i), text, post))
                            else:
                                loop.create_task(self.send_telegram(i, text))




    async def get_rass(self, gen):
        results = self.create_mongo.get(self.collection_django, self.apps)
        for i in results:
            #print(i["text"])
            date_chek = date_compare(i["date_start"], i["period"]).compare_date()
            #print(date_chek)
            if date_chek == "1":
                #await api_url(f"{self.url_dj}").post_json(id=i["id"], delete="1")
                spis_ras = self.create_mongo.get_them(self.collection_django, self.apps, i["id"])
                await self.dispatch(i, spis_ras, gen, i["id"])
                await api_url(f"{self.url_dj}").post_json(id=i["id"], delete="1")

            elif date_chek != "0":
                await api_url(f"{self.url_dj}").post_json(id=i["id"], date_start=date_chek)
                spis_ras = self.create_mongo.get_them(self.collection_django, self.apps, i["id"])
                await self.dispatch(i, spis_ras, gen, i["id"])

    async def peer_ids_add(self, apis_new, club_id):
        #for i in self.apis:
        p = await self.apis[int(club_id)].api_post("messages.getConversations", v=self.V, count=200)
        for i in p["items"]:
            #print(i)
            if int(i["conversation"]["peer"]["id"]) > 2000000000:
                print(i["conversation"]["peer"]["id"], club_id)
        return
            #self.create_mongo.update(self.collection_bots, self.document_tokens, i, self.peer_id)

    async def withdrawal_warn_ban(self):
        tek = await self.current_time()
        await self.create_mongo.remove_ban_warn(tek)

    async def parsing_mirea(self, l_id):

        #txt = await api_url("https://priem.mirea.ru/accepted-entrants-list/#bach").get_html()
        #soup = BeautifulSoup(txt, 'html.parser')
        try:
            #txt = await api_url(f"https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition={l_id}").get_html()
            url = (f'https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition={l_id}')
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            #soup = BeautifulSoup(txt, 'html.parser')
            table = soup.find('table')
            x = (len(table.findAll('tr')) - 1)
            for row in table.findAll('tr')[1:x]:
                col = row.findAll('td')
                #name = col[1].getText()
                if col[1].getText() not in self.slov_directions_general:
                    self.slov_directions_general[col[1].getText()] = \
                        {
                            "snils": col[1].getText(),
                            "1":
                                {
                                    "position": col[0].getText(), "consent": col[2].getText(), "hostel": col[3].getText(),
                                    "scores": col[4].getText(), "sum": col[5].getText(),
                                    "achievement_score": col[6].getText(),
                                    "total_amount": col[7].getText(), "note": col[8].getText(), "code_directions": l_id,
                                    "position_consent": 0
                                  },
                            "count": 1
                        }


                else:
                    count = self.slov_directions_general[col[1].getText()]["count"] + 1
                    self.slov_directions_general[col[1].getText()][str(count)] =\
                        {
                            "position": col[0].getText(), "consent": col[2].getText(), "hostel": col[3].getText(),
                            "scores": col[4].getText(), "sum": col[5].getText(),
                            "achievement_score": col[6].getText(),
                            "total_amount": col[7].getText(), "note": col[8].getText(), "code_directions": l_id,
                            "position_consent": 0
                        }
                    # self.slov_directions_general[col[1].getText()][count]["position"] = col[0].getText()
                    # self.slov_directions_general[col[1].getText()][count]["consent"] = col[2].getText()
                    # self.slov_directions_general[col[1].getText()][count]["hostel"] = col[3].getText()
                    # self.slov_directions_general[col[1].getText()][count]["scores"] = col[4].getText()
                    # self.slov_directions_general[col[1].getText()][count]["sum"] = col[5].getText()
                    # self.slov_directions_general[col[1].getText()][count]["achievement_score"] = col[6].getText()
                    # self.slov_directions_general[col[1].getText()][count]["total_amount"] = col[7].getText()
                    # self.slov_directions_general[col[1].getText()][count]["note"] = col[8].getText()
                    self.slov_directions_general[col[1].getText()]["count"] += 1

                #self.list_direction_dop.append({"code_directions": l_id, "consent": col[2].getText()})
                if l_id not in self.list_direction_dop:
                    self.list_direction_dop[l_id] = []
                self.list_direction_dop[l_id].append({"snils": col[1].getText(), "code_directions": l_id, "position": col[0].getText(),
                                                      "consent": col[2].getText()})
                # self.list_direction_dop[l_id][col[1].getText()] = {}
                # self.list_direction_dop[l_id][col[1].getText()]["pos ition"] = col[0].getText()
                # self.list_direction_dop[l_id][col[1].getText()]["consent"] = col[2].getText()
            return

        except Exception as e:
            print(f"Code_directions: {l_id}")
            print(traceback.format_exc())
        try:
            # txt = await api_url(
            #     f"https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition={l_id}").get_html()
            url = (f'https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition={l_id}')
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            #soup = BeautifulSoup(txt, 'html.parser')
            table = soup.find('table')
            x = (len(table.findAll('tr')) - 1)
            for row in table.findAll('tr')[1:x]:
                col = row.findAll('td')
                # name = col[1].getText()
                if col[1].getText() not in self.slov_directions_general:
                    self.slov_directions_general[col[1].getText()] = \
                        {
                            "snils": col[1].getText(),
                            "1": {"position": col[0].getText(), "consent": col[2].getText(), "hostel": col[3].getText(),
                                  "scores": col[4].getText(), "sum": col[5].getText(),
                                  "achievement_score": col[6].getText(),
                                  "total_amount": col[7].getText(), "note": col[8].getText(), "code_directions": l_id,
                                  "position_consent": 0
                                  },
                            "count": 1
                        }

                else:
                    count = self.slov_directions_general[col[1].getText()]["count"] + 1
                    self.slov_directions_general[col[1].getText()][str(count)] = \
                        {
                            "position": col[0].getText(), "consent": col[2].getText(), "hostel": col[3].getText(),
                            "scores": col[4].getText(), "sum": col[5].getText(),
                            "achievement_score": col[6].getText(),
                            "total_amount": col[7].getText(), "note": col[8].getText(), "code_directions": l_id,
                            "position_consent": 0
                        }
                    self.slov_directions_general[col[1].getText()]["count"] += 1

                if l_id not in self.list_direction_dop:
                    self.list_direction_dop[l_id] = []
                self.list_direction_dop[l_id].append({"snils": col[1].getText(), "code_directions": l_id, "position": col[0].getText(),
                                                      "consent": col[2].getText()})
                # self.list_direction_dop[l_id][col[1].getText()] = {}
                # self.list_direction_dop[l_id][col[1].getText()]["position"] = col[0].getText()
                # self.list_direction_dop[l_id][col[1].getText()]["consent"] = col[2].getText()
        except Exception as e:
            print(f"Code_directions: {l_id}")
            print(traceback.format_exc())
        return

    async def parsing_mirea_add(self, loop):
        self.slov_directions_general = {}
        for i in self.list_directions:
            #await self.parsing_mirea(i)
            loop.create_task(self.parsing_mirea(i['identifier']))
        await asyncio.sleep(60)
        try:
            for i in self.slov_directions_general:
                for j in range(1, self.slov_directions_general[i]["count"] + 1):
                    ll = 1
                    for k in self.list_direction_dop[self.slov_directions_general[i][f"{j}"]["code_directions"]]:
                        if k["snils"] == self.slov_directions_general[i]["snils"]:
                            #ll += 1
                            self.slov_directions_general[i][f"{j}"]["position_consent"] = ll
                            break
                        if k["consent"] == "да":
                            ll += 1
            print(self.slov_directions_general)
        except Exception as e:
            print(traceback.format_exc())


        print(self.slov_directions_general)

            #for j in i["count"]:
        for i in self.slov_directions_general:
            #print(i, self.slov_directions_general[i])
            self.list_directions_general.append(self.slov_directions_general[i])
        #print(self.list_directions_general)
        await self.create_mongo.users_directions(self.list_directions_general, self.list_directions)
        #print(self.slov_directions_general)

    async def beskon(self):
        #[await self.peer_ids_add(self.apis[i], i) for i in self.apis]
        #loop = asyncio.get_running_loop()
        #tasks = [loop.create_task(self.peer_ids_add(self.apis[i], i)) for i in self.apis]
        #loop.run_until_complete(asyncio.wait(tasks))
        #await self.peer_ids_add()
        #gen = await self.generate(self.st)
        loop = asyncio.get_running_loop()
        tim = 0
        while True:
            gen = await self.generate(self.st)
            loop.create_task(self.get_rass(gen))
            loop.create_task(self.withdrawal_warn_ban())
            if tim == 60 or tim == 0:
                await self.create_mongo.directions_time(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                loop.create_task(self.parsing_mirea_add(loop))
            await asyncio.sleep(60)
            tim += 1
