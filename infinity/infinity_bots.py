# -*- coding: utf-8 -*-

import asyncio
import traceback
import json
import pprint
from pymongo import MongoClient

from api import api_url
from api.methods import methods
from command_besed import command_list
from command_ls import command_ls_list

from commands_ls import issuing_directions, choice_conversation, response_text_admin, adding_change_snils
from message_handling import processing, processing_new
from api.api_execute import add_friends
from middlewares import SimpleHandler
from summer_module import Binding
from summer_module.punishments.unban import UnbanLs

localhost = "localhost"
port = 27017
client = MongoClient(localhost, int(port))


class infinity_bots:

    def __init__(self, V, create_mongo, collection_bots, document_tokens, url_dj):

        self.V = V
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.url_dj = url_dj
        #self.simple_handler = SimpleHandler()

    def if_int(self, number):
        try:
            return int(number)
        except:
            return False

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # async def selection(self, command_list, text, them):
    #     flag = False
    #     for c in command_list:
    #         #print(c.keys)
    #         for k in c.keys:
    #             if k == text or k == text[1:]:
    #                 # print(c)
    #                 if c.condition(text) or c.condition(text[1:]):
    #                     flag = True
    #                     break
    #             elif k == text.split(" ")[0] or k == text.split(" ")[0][1:]:
    #                 if c.condition(text.split(" ")[0]) or c.condition(text.split(" ")[0][1:]):
    #                     flag = True
    #                     break
    #
    #             #print(text.split(" ")[0])
    #         #print(flag)
    #         if flag:
    #             for m in c.topics_blocks:
    #                 if m == them or m == them[1:]:
    #                     return 0
    #             if len(c.topics_resolution) == 0:
    #                 return c
    #             for n in c.topics_resolution:
    #                 if n == them or n == them[1:]:
    #                     return c
    #             return 0
    #     return 0
    def button_vk(self, label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    def level_education(self):
        keyboard = {
            "one_time": False,
            "buttons": [
                [self.button_vk(label="Бакалавриат / Специалитет", color="positive"),
                 self.button_vk(label="Магистратура", color="positive"),
                 self.button_vk(label="Колледж", color="positive")],
                [self.button_vk(label="Команды", color="negative")]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    async def selection(self, command_list, text, them):
        flag = False
        for c in command_list:
            #print(c.keys, text)
            for k in c.keys:
                if k == text or k == text[1:]:
                    # print(c)
                    flag = True
                    break
                elif k == text.split(" ")[0] or k == text.split(" ")[0][1:]:
                    flag = True
                    break
                if text != 'chat_invite_user' and text != 'chat_invite_user_by_link':
                    if k in text:
                        flag = True
                        break
                # elif k in text:
                #     flag = True
                #     break
                #print(text.split(" ")[0])
            #print(flag)
            if flag:
                for m in c.topics_blocks:
                    if m == them or m == them[1:]:
                        return 0
                if len(c.topics_resolution) == 0:
                    return c
                for n in c.topics_resolution:
                    if n == them or n == them[1:]:
                        return c
                return 0
        return 0

    async def main(self, apis, club_id, them, control, loop1):
        #apis = api(club_id, token)
        #print("-" * 40)
        #print(f"Start group ID: [{club_id}] Them: [{them}]")
        if them == "tema1":
            f1 = open("ploxie_slova.txt", "r+", encoding="utf8")
            d1 = f1.readlines()
            f1.close()
            bad_words = d1[0].split(', ')
            # try:
            #     peer_ids = await self.create_mongo.get_settings()
            #     for i in peer_ids:
            #         star = await methods(self.V, club_id).users_chek(int(i), apis)
            #         if star:
            #             self.create_mongo.start_bs(int(i), star[0], star[1], star[2])
            # except Exception as e:
            #     print(traceback.format_exc())
        if them == "zluka1":
            await asyncio.sleep(5)
            for i in range(2000000055, 2000000090):
                try:
                    await apis.api_post("messages.send", v=self.V, peer_id=i,
                                        message="Привязать", random_id=0)
                except:pass

        #loop = asyncio.get_running_loop()
        asd = await apis.api_get("groups.getLongPollServer", v=self.V, group_id=club_id)
        #print(asd)
        if "error" not in asd:
            #print(asd)
            server = asd['server']
            key = asd['key']
            ts = asd['ts']

            while True:
                try:
                    loop = asyncio.get_running_loop()
                    if control[club_id] != them:
                        print(f"Close {club_id}")
                        return
                    otvet = await api_url(f"{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2").get_json(club_id)
                    if "failed" in otvet:
                        if otvet["failed"] == 2 or otvet["failed"] == 3:
                            asd = await apis.api_get("groups.getLongPollServer", v=self.V, group_id=club_id)
                            if "error" not in asd:
                                server = asd['server']
                                key = asd['key']
                                ts = asd['ts']
                                continue
                        elif otvet["failed"] == 1:
                            ts = otvet['ts']
                            continue

                        else:
                            continue

                    updates = otvet["updates"]
                    if "ts" in otvet:
                        ts = otvet['ts']
                    if len(updates) > 0:
                        slovar = updates[0]
                        if "type" in slovar and slovar["type"] == "message_new":
                            message = slovar["object"]["message"]
                            from_id = message["from_id"]
                            peer_id = message["peer_id"]
                            # print(message)

                            # LS
                            if from_id == peer_id:
                                await SimpleHandler(self.V, club_id, message, apis, them,
                                                                self.create_mongo,
                                                                self.collection_bots,
                                                                self.document_tokens,
                                                                self.url_dj, loop).middleware_ls()
                                continue
                                #print("LS: ", message)
                                text = message["text"].lower()
                                sel = await self.selection(command_ls_list, text, them)
                                #print(sel, text, command_ls_list)
                                blocs = ["target", "consultants", "tema1"]
                                ##print("SEL: ", sel)
                                if them == "tema1":
                                    if await self.create_mongo.admin_answer_id_check(message["peer_id"]):
                                        loop.create_task(
                                            response_text_admin(self.V, club_id, message, apis, them,
                                                                self.create_mongo,
                                                                self.collection_bots,
                                                                self.document_tokens,
                                                                self.url_dj).run())
                                        continue

                                # if sel != 0:
                                #     loop.create_task(sel.process(self.V, club_id, message, apis, them,
                                #                                  self.create_mongo,
                                #                                  self.collection_bots,
                                #                                  self.document_tokens,
                                #                                  self.url_dj).run())
                                #     continue
                                else:
                                    number = self.if_int(text)
                                    chek = self.create_mongo.check_user(peer_id)
                                    if number:
                                        if 310 >= number >= 0:
                                            number = number - 10
                                            #chek = self.create_mongo.check_user(peer_id)
                                            if chek == 2:
                                                loop.create_task(issuing_directions(self.V, club_id, message, apis, them,
                                                                 self.create_mongo,
                                                                 self.collection_bots,
                                                                 self.document_tokens,
                                                                 self.url_dj).run())
                                                continue


                                    if them not in blocs:
                                        otvet = self.create_mongo.questions_get_one(text)
                                        if otvet != "":
                                            await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                                                message=otvet, random_id=0)
                                            continue
                                    elif chek == 4:
                                        loop.create_task(
                                            choice_conversation(self.V, club_id, message, apis, them,
                                                                self.create_mongo,
                                                                self.collection_bots,
                                                                self.document_tokens,
                                                                self.url_dj).run())
                                        continue
                                    elif chek == 5 or chek == 6:
                                        loop.create_task(
                                            adding_change_snils(self.V, club_id, message, apis, them,
                                                                self.create_mongo,

                                                                self.collection_bots,
                                                                self.document_tokens,
                                                                self.url_dj).run())


                                    elif them == "tema1":

                                        chek_nap = self.create_mongo.check_user_nap(message["from_id"])
                                        if chek_nap != "0":
                                            if chek_nap == "bac":
                                                documents = "questions_abitur"
                                            elif chek_nap == "col":
                                                documents = "questions_col"
                                            elif chek_nap == "mac":pass
                                            otvet = self.create_mongo.questions_get_one(text, documents=documents)
                                            if otvet != "":
                                                await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                                                    message=otvet, random_id=0)
                                                continue
                                        # else:
                                        #     await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                        #                         message="Для получения ответа, выберите интересующий уровень образования.",
                                        #                         random_id=0,
                                        #                         keyboard=self.level_education())

                            # BS
                            if from_id != peer_id:
                                print("EST")
                                await SimpleHandler(self.V, club_id, message, apis, them,
                                                    self.create_mongo,
                                                    self.collection_bots,
                                                    self.document_tokens,
                                                    self.url_dj, loop, client=client).middleware_ls(True)
                                #continue
                                #continue
                                #print("BS: ", message)
                                if them == "zluka111":
                                    #if message["from_id"] == 597624554:
                                        #await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                                            #message="Начнём", random_id=0)
                                    print("zluka")
                                    if message["from_id"] == -5411326 and "родная" in message["text"].lower():
                                        peer_id_ab = message["text"].split(" ")[0]
                                        peer_id_zl = message["peer_id"]
                                        res = await self.create_mongo.add_besed_zl(peer_id_ab, peer_id_zl)
                                        if res == 1:
                                            await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                                                message="Стартуем", random_id=0)
                                        else:
                                            await apis.api_post("messages.send", v=self.V, peer_id=message["peer_id"],
                                                                message="Уже стартовали", random_id=0)

                                    if "action" in message:
                                        sel = await self.selection(command_list, message["action"]["type"], them)
                                        ##print("SEL: ", sel)
                                        if sel != 0:
                                            loop.create_task(sel.process(self.V, club_id, message, apis, them,
                                                                         self.create_mongo,
                                                                         self.collection_bots,
                                                                         self.document_tokens,
                                                                         self.url_dj).run())
                                        continue

                                text = message["text"].lower()
                                # sel = await self.selection(command_list, text, them)
                                # print("SEL: ", sel)
                                # if sel != 0:
                                #     loop.create_task(sel.process(self.V, club_id, message, apis, them,
                                #                                  self.create_mongo,
                                #                                  self.collection_bots,
                                #                                  self.document_tokens,
                                #                                  self.url_dj).run())
                                    #await sel.process(self.V, club_id, message, apis, them, self.create_mongo).run()
                                if them == "tema1":
                                    loop.create_task(processing_new(self.V, club_id, message, apis, them,
                                                                self.create_mongo,
                                                                self.collection_bots,
                                                                self.document_tokens,
                                                                self.url_dj, client=client).run())
                                    # await processing(self.V, club_id, message, apis, them,
                                    #                             self.create_mongo,
                                    #                             self.collection_bots,
                                    #                             self.document_tokens,
                                    #                             self.url_dj).run(bad_words)
                                continue


                except Exception as e:
                    print(traceback.format_exc())
                    continue
        #print(asd["code"])
        elif "error" in asd and asd["errcode"] in [5, 38]:
            #print(111111111111111111111)
            await api_url(f"{self.url_dj}").post_json(club_id=club_id, status=1)
            return
        #print(asd)

    async def main_user(self, apis, user_id, mongo_manager): #  8eeeba5ca7ebdaed6fa6163a6053722bbfe9eaca70be274d024dcac817010305e267eb749b28d6f0bd54d
        #vk1.a.y_smypVLUu0DX0g_Ob3wCwISwlYeQYvhPSlZwn47VQ8dUeKQEyKmHenM6_zigawvIM3RQ5uHS69BIyR_FqgfXqXIV1cAg8rtn62TYV1HJ3y5R31jO_FBAvtB0yOC8QE2x2-4nBXFDDQtv6n25in1Oe4xZFW7uHJznniKguIVfBTB6NLJMpozsiB3wjpn5yWJ
        # vk1.a.kJQxN4b2pgLtQxApgjhBwOV1vuHqb5v9S2yM6EksHyeH5kaEXYO3OwZ1bDaBqauaJzhPfpIQb83zIyJKWqRLFoD8_F89RrOPgDBVXDfWAVMYZqpqqek_vRj-NVBSfiAoyYNOKxugG3Bfai0Cd7PnyLWBkU0aXEgCS_sNteyhtp_HbRaEphaMHdgI9EBSps69
        #print("DOSHLO")
        title_list = ['Институт перспективных технологий и индустриального программирования РТУ МИРЭА',
                      'Колледж программирования и кибербезопасности',
                      'Институт информационных технологий РТУ МИРЭА',
                      'Институт искусственного интеллекта РТУ МИРЭА',
                      'Институт технологий управления РТУ МИРЭА',
                      'Институт международного образования РТУ МИРЭА',
                      'Магистратура РТУ МИРЭА',
                      'Институт радиоэлектроники и информатики РТУ МИРЭА',
                      'Институт кибербезопасности и цифровых технологий РТУ МИРЭА']
        ids = []
        # result = await apis.api_post("messages.getConversations", v=self.V, count=100)
        # for i in result["items"]:
        #     #print(i["conversation"]["peer"])
        #     if i["conversation"]["peer"]["type"] == 'chat':
        #         print(i["conversation"])
        #         title = i["conversation"]["chat_settings"]["title"]
        #         if title in title_list:
        #             ids.append(i["conversation"]["peer"]["id"])

        #print(result)
        #pprint.pprint(result)
        #print(ids)

        # ids = [2000000242, 2000000247, 2000000246, 2000000243, 2000000241, 2000000245, 2000000244, 2000000239, 2000000240]
        #
        # for i in ids:
        #     res = await api_url(f'https://api.vk.com/method/bot.addBotToChat?v=5.92&access_token=vk1.a.8CqjPAT9cqqMMcJQ0RpZe4DXrb7zQBnpCCnUlFL9kUbn7T86KYQjWbf-s53NCAzAZ0Jawf9y0RJJapcElHKaAKi5RV2vSRbFT88EQQ5Olo095IZBW-_1xfi-p8GMjICQ0UDZ4WSI_w_TkoZ7jwuxynGUckrZ0imhIEglnA5HRQyhkoltIBIgiuTmjk2EOhTe&peer_id={i}&bot_id=-174516461').get_json()
        #     print(res)
            # a = await fet(
            #     f'https://api.vk.com/method/bot.addBotToChat?v=5.92&access_token={bots2[str(uid)]}&peer_id={chat}&bot_id={botid}')
        # while True:
            # try:
            #     result = await apis.api_post("friends.getRequests", v=self.V, count=100)
            #     #for i in result["items"]:
            #     if result["items"]:
            #         de = self.chunks(result["items"], 5)
            #         l = list(de)
            #         for i in l:
            #             await apis.api_post("execute", code=add_friends(users=i), v=self.V)
            #     await asyncio.sleep(60)
            # except Exception as e:
            #     print(traceback.format_exc())
            #     continue



        # print("TYT")
        asd = await apis.api_get("messages.getLongPollServer", v=self.V, need_pts=1, lp_version=3)
        #print(asd)
        # print(asd)
        if "error" not in asd:
            # print(asd)
            server = asd['server']
            key = asd['key']
            ts = asd['ts']

            while True:
                try:
                    otvet = await api_url(f"http://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2").get_json(1)
                    if "failed" in otvet:
                        if otvet["failed"] == 2 or otvet["failed"] == 3 or otvet["failed"] == 1:
                            asd = await apis.api_get("messages.getLongPollServer", v=self.V, need_pts=1, lp_version=3)
                            if "error" not in asd:
                                server = asd['server']
                                key = asd['key']
                                ts = asd['ts']
                                continue

                        else:
                            asd = await apis.api_get("messages.getLongPollServer", v=self.V, need_pts=1, lp_version=3)
                            if "error" not in asd:
                                server = asd['server']
                                key = asd['key']
                                ts = asd['ts']
                                continue

                    updates = otvet["updates"]
                    #print(updates)
                    if "ts" in otvet:
                        ts = otvet['ts']

                    for i1 in range(0, len(updates)):
                        # time.sleep(0.03)
                        await asyncio.sleep(0.03)
                        #print(updates)
                        if updates[i1][0] == 4 and updates[i1][7].get('from', None):
                            from_id = int(updates[i1][7]["from"])
                            if updates[i1][7].get("from", None):
                                uid = updates[i1][7]["from"]
                                groupChat = True
                            else:
                                uid = updates[i1][3]
                                groupChat = False
                            if groupChat:
                                group_id = abs(2000000000 - updates[i1][3])
                                chat_id = group_id
                            args = updates[i1][6].split()

                            #print(args)

                            if int(from_id) == int(597624554) or int(from_id) == -5411326 or int(from_id) == -194180799:
                                #print("MSG: ", updates[i1][6].lower())
                                if "родная" in updates[i1][6].lower():
                                    peer_id_ab = updates[i1][6].lower().split(" ")[0]
                                    peer_id_zl = updates[i1][3]
                                    # res = await self.create_mongo.add_besed_zl(peer_id_ab, peer_id_zl)
                                    bind = Binding(mongo_manager)
                                    result = await bind.run(peer_id=int(peer_id_ab), peer_id_zl=int(peer_id_zl),
                                                            is_user_bot=True)

                                    await apis.api_post("messages.send", v=self.V, peer_id=updates[i1][3],
                                                             message=result["message"], random_id=0)

                            if args != []:pass
                                #print(updates)
                        else:
                            #print(updates, i1)
                            if len(updates[i1]) > 5:
                                uid = updates[i1][3]
                                text = updates[i1][6].lower()
                                if text == "разбан":
                                    unban = UnbanLs(mongo_manager, user_id=int(uid), current_time=int(updates[i1][4]))
                                    result = await unban.task_user_bot_unban_check()
                                    #print(result)
                                    if result["message"]:
                                        is_friends = await apis.api_post("friends.areFriends", v=self.V,
                                                                         user_ids=f"{updates[i1][3]}")

                                        if is_friends[0]["friend_status"] == 1:
                                            await apis.api_post("messages.send", v=self.V, peer_id=int(updates[i1][3]),
                                                                message="Ты сам решил со мной не дружить, прощай.",
                                                                random_id=0)
                                            await apis.api_post("account.ban", v=self.V, owner_id=int(updates[i1][3]))
                                            continue

                                        if is_friends[0]["friend_status"] == 0:
                                            await apis.api_post("messages.send", v=self.V, peer_id=int(updates[i1][3]),
                                                                message="Добавь для начала меня в друзья", random_id=0)
                                            continue

                                        if is_friends[0]["friend_status"] == 2:
                                            await apis.api_post("friends.add", v=self.V,
                                                                user_id=int(updates[i1][3]))
                                        result = await unban.task_user_bot_unban()

                                        await apis.api_post("messages.send", v=self.V, peer_id=int(updates[i1][3]),
                                                            message=result["message"], random_id=0)
                                        for i in result['peer_ids']:
                                            group_id = abs(2000000000 - i)
                                            chat_id = group_id
                                            await apis.api_post("messages.addChatUser", v=self.V, chat_id=chat_id,
                                                                user_id=uid, visible_messages_count=1000)


                        # if len(updates) > 0:
                    #     slovar = updates[0]
                    #     if "type" in slovar and slovar["type"] == "message_new":
                    #         message = slovar["object"]["message"]
                    #         from_id = message["from_id"]
                    #         peer_id = message["peer_id"]
                except Exception as e:
                    #print(traceback.format_exc())
                    asd = await apis.api_get("messages.getLongPollServer", v=self.V, need_pts=1, lp_version=3)
                    if "error" not in asd:
                        server = asd['server']
                        key = asd['key']
                        ts = asd['ts']
                        continue
                    continue
