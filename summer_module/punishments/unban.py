
from datetime import datetime

from summer_module.convert import num2text
from summer_module.user_conversation import WorkUser, Unban, TaskUserBot, SettingTime
import numpy as np


class UnbanLs(WorkUser):

    #@checking_admin
    async def run(self, peer_id_number: int = 0, answer_number: int = 0, **kwargs):

        return_dict = await self._unban(peer_id_number, answer_number)
        await self.update_all_user_new()
        return return_dict
        # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        # if not info:
        #     msg = f"⚠ Данного [id{user_id}|пользователя], возможно, нет в беседе." \
        #           "❗ Обновите информацию командой /update."
        #     return_dict = {"message": msg, "action": "kick", "update": False, "kick_id": [user_id], "peer_id": peer_id,
        #                    "error_message": True}
        #     return return_dict
        #
        # return_dict = await self._add_ban_user(user_id, peer_id, time_plus, cause)
        # await self.update_all_user_new()
        # return_dict["peer_id"] = peer_id
        # return return_dict
        # peer_ids_dict = {
        #                     "status": False,
        #                     "user_id_bot": self.user_id_bot,
        #                     "peer_id": peer_id,
        #                     "current_time": self.current_time
        #                 }

    async def accrue_influence(self, finish_time):
        setting_time = SettingTime(start_time=self.current_time)
        setting_time.self_generator(
            await self.manager_db.user_insert_one(setting_time.class_dict, self.setting_time_documents))
        flag = False
        if setting_time.finish_time == 0:
            setting_time.finish_time = finish_time
            flag = True
        elif setting_time.finish_time <= self.current_time:
            setting_time.finish_time = finish_time
            setting_time.start_time = self.current_time
            flag = True
        await self.manager_db.user_update_one(setting_time.class_dict, self.setting_time_documents)
        return flag


    async def unban_all(self, finish_time):
        peer_ids = await self.manager_db.peer_ids_get_all(self.peer_ids)
        for i in peer_ids:
            #print(i)
            unban_list = await self.manager_db.user_get_all(str(i))
            user_list = []
            for user in unban_list:
                flag = False

                if user["punishments"]["ban"].get("status"):
                    if self.current_time >= user["punishments"]["ban"]["finish_time"]:
                        user["punishments"]["ban"]["status"] = False
                        flag = True
                if user["punishments"]["warn"].get("warn_list") and len(user["punishments"]["warn"]["warn_list"]) > 0:
                    warn_list = user["punishments"]["warn"]["warn_list"].copy()
                    for warn in user["punishments"]["warn"]["warn_list"]:
                        if self.current_time >= warn["finish_time"]:
                            warn["status"] = False
                            warn_list.remove(warn)
                            flag = True
                    #print(warn_list)
                    user["punishments"]["warn"]["warn_list"] = warn_list
                if flag:
                    user_list.append(user)
            await self.manager_db.users_update_ban_warn(user_list, str(i))

        if await self.accrue_influence(finish_time):
            users_list = await self.manager_db.user_get_all(self.users_documents)
            for user in users_list:
                #print(user)
                if user.get('xp'):
                    lvl_list = await self.lvl_list(user['xp'])
                    user['influence'] = lvl_list['limit']['influence']
            await self.manager_db.users_update_influence(users_list, self.users_documents)


        msg = "Обновил успешно"
        return_dict = {"message": msg}
        return return_dict


    async def give_permission(self, task_id, type_punishment):
        task = TaskUserBot(user_id=self.user_id)
        task.self_generator(await self.manager_db.user_insert_one(task.class_dict, self.task_user_bot_documents))

            #task.peer_ids[int(task_id)]["status"] = False
        if type_punishment == "unban":
            if not task.peer_ids[int(task_id)]["permission"]:
                task.peer_ids[int(task_id)]["permission"] = True
                task.peer_ids[int(task_id)]["processed"] = True
                msg = f"✅ Разрешаю [id{self.user_id}|пользователю] разбан"
            else:
                msg = f"⚠ Вы уже разрешили [id{self.user_id}|пользователю] разбан"
        else:
            if not task.peer_ids[int(task_id)]["permission"]:
                msg = f"😢 Данному [id{self.user_id}|пользователю] успешно отказано в разбане"
                task.peer_ids[int(task_id)]["processed"] = True
            else:
                msg = f"⚠ Вы уже запретили [id{self.user_id}|пользователю] разбан"
        await self.manager_db.user_update_one(task.class_dict, self.task_user_bot_documents)

        return_dict = {"message": msg}
        return return_dict

    async def task_user_bot_unban(self):
        task = TaskUserBot(user_id=self.user_id)
        task.self_generator(await self.manager_db.user_insert_one(task.class_dict, self.task_user_bot_documents))

        unban_peer_ids = []
        msg = ""
        if task.permission:
            for i in task.peer_ids:
                if not i["status"] and i["permission"] and i["processed"]:

                    conversation_st = await self.manager_db.peer_ids_get_one(i["peer_id"], self.conversations_st)
                    if conversation_st:
                        unban_peer_ids.append(conversation_st["peer_id_zl"])
                        i["status"] = True

            await self.manager_db.user_update_one(task.class_dict, self.task_user_bot_documents)

        if unban_peer_ids:
            msg = "Разбаниваю"
        return_dict = {"message": msg, "peer_ids": unban_peer_ids}

        return return_dict

    async def task_user_bot_unban_check(self):
        task = TaskUserBot(user_id=self.user_id)
        task.self_generator(await self.manager_db.user_insert_one(task.class_dict, self.task_user_bot_documents))

        unban_peer_ids = []
        msg = ""
        #print(task.class_dict)
        if task.permission:
            for i in task.peer_ids:
                if not i["status"] and i["permission"] and i["processed"]:

                    conversation_st = await self.manager_db.peer_ids_get_one(i["peer_id"], self.conversations_st)
                    if conversation_st:
                        unban_peer_ids.append(conversation_st["peer_id_zl"])
                        #i["status"] = True

            await self.manager_db.user_update_one(task.class_dict, self.task_user_bot_documents)

        if unban_peer_ids:
            msg = "Разбаниваю"
        return_dict = {"message": msg, "peer_ids": unban_peer_ids}

        return return_dict


    async def get_log_users(self, user_id, peer_id, action, cause, finish_time, time_plus):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "action": action,
            "cause": cause,
            "finish_time": finish_time,
            "time_plus": time_plus
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, action, cause, finish_time, time_plus):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "ban",
            "action": action,
            "cause": cause,
            "finish_time": finish_time,
            "time_plus": time_plus
        }
        return log_dict


    async def record_list_peer_ids(self):
        unban = Unban(user_id=self.user_id)
        unban.self_generator(await self.manager_db.user_insert_one(unban.class_dict, self.unban_documents))

        await self.get_user(self.user_id)
        user_info = self.users_info[self.user_id].user

        if user_info.ban_attempts == -1 or user_info.ban_attempts > 0:

            #print(user_info.class_dict)

            peer_ids = await self.manager_db.user_ban_peer_ids_check(user_info.class_dict, self.peer_ids)

            if peer_ids:

                lvl_list = await self.lvl_list(user_info.xp)

                unban.peer_ids = peer_ids
                await self.manager_db.user_update_one(unban.class_dict, self.unban_documents)

                #questions_man = ((u'вопрос', u'вопроса', u'вопросов'), 'm')

                #unban_questions_count = await num2text(lvl_list['limit']['unban_questions_count'], questions_man)

                msg = "🕵 Вы попали в разбанивающий раздел, сообщения здесь самоуляются через 1 минуту.\n\n" \
                      "⚠ Если вы не успеете ответить на любое сообщение из этого раздела, не включая этого, " \
                      "ваша попытка разбана сгорит.\n\n" \
                      f"💬 Вам необходимо пройти тест из {lvl_list['limit']['unban_questions_count']} вопросов.\n" \
                      f"🗣 Чтобы получить разбан, ответьте правильно на {lvl_list['limit']['unban_answers_count']}.\n" \
                      "✉ Для ответа на вопрос отправьте сообщение с выбранным номером ответа.\n" \
                      "❗ После выбора беседы сразу начнётся тест.\n\n" \
                      "👥 Выберите номер беседы, в которой вас необходимо разбанить, " \
                      "показаны только те беседы, где доступна попытка разбана:\n\n"

                return_dict = {"message": msg, "peer_ids": peer_ids}
            else:
                msg = "⚠ Не вижу вас забаненым ни в одной беседе."
                return_dict = {"message": msg, "peer_ids": peer_ids}
        else:
            msg = "⚠ У вас недостаточное количество попыток разбана."
            return_dict = {"message": msg, "peer_ids": []}
        return return_dict



    async def _unban(self, peer_id_number: int, answer_number: int):


        unban = Unban(user_id=self.user_id)
        unban.self_generator(await self.manager_db.user_insert_one(unban.class_dict, self.unban_documents))
        action = False
        task_id = 0
        if not unban.active:

            if peer_id_number > len(unban.peer_ids) or peer_id_number < 1 or not unban.peer_ids:
                msg = ""
                return_dict = {"message": msg, "peer_ids": []}
                return return_dict

            peer_id = unban.peer_ids[peer_id_number - 1]

            unban.count += 1
            unban.active = True
            await self.get_user(self.user_id)
            user_info = self.users_info[self.user_id].user
            user_info.update = True

            if user_info.ban_attempts == -1:
                user_info.ban_attempts = 0
            else:
                user_info.ban_attempts -= 1

            lvl_list = await self.lvl_list(user_info.xp)

            questions = await self.manager_db.questions_unban_get_all(self.collection_django,
                                                                      self.django_unban_documents)

            np.random.shuffle(questions)

            questions_list = []
            k = 1
            for i in questions:
                question_dict = {}
                question = i["question"].split('\n')
                question_new = question[0]
                question.pop(0)
                np.random.shuffle(question)
                answer = i["answer"]
                kk = 1
                answer_new = []
                for j in question:
                    l = j.split(" ")
                    if answer in l[0]:
                        question_dict[f"answer"] = str(kk)
                    l.pop(0)
                    answer_new.append(f"{kk}) {' '.join(l)}")
                    kk += 1
                question_dict["question"] = str(question_new) + "\n" + "\n".join(answer_new)
                k += 1
                questions_list.append(question_dict)


            unban.questions_answers.append(
                {
                    "questions": questions_list, "count_questions": 0,
                    "count_correct_answers": 0,
                    "unban_questions_count": lvl_list["limit"]["unban_questions_count"],
                    "unban_answers_count": lvl_list["limit"]["unban_answers_count"],
                    "unban_default_seconds": lvl_list["limit"]["unban_default_seconds"],
                    "peer_id": peer_id})
            await self.manager_db.user_update_one(unban.class_dict, self.unban_documents)

            questions_answers_unban = unban.questions_answers[unban.count - 1]
            question = questions_answers_unban["questions"][questions_answers_unban["count_questions"]]
            peer_id = questions_answers_unban['peer_id']

            msg = f"{question['question']}"

        else:
            questions_answers_unban = unban.questions_answers[unban.count-1]
            #print(questions_answers_unban)
            #print(questions_answers_unban["count_questions"])
            question = questions_answers_unban["questions"][questions_answers_unban["count_questions"]]
            peer_id = questions_answers_unban['peer_id']

            if str(answer_number) == str(question["answer"]):
                questions_answers_unban["count_correct_answers"] += 1

            questions_answers_unban["count_questions"] += 1

            if questions_answers_unban["count_correct_answers"] == questions_answers_unban["unban_answers_count"]:
                msg = f"💥 Поздравляю!\n\n" \
                      f"😎 Вы набрали нужное количество правильных ответов, разбан у вас в кармане.\n\n" \
                      "🔊 Разбаню вас в беседе «{0}»\n\n" \
                      "✉ Вам необходимо дождаться разрешение на разбан от администратора беседы.\n\n" \
                      "➕ После получения разрешения, данный администратор автоматически пригласит вас, добавьте его в друзья:\n\n" \
                      "https://vk.com/id799863315"

                unban.active = False

                await self.get_user_conversation(self.user_id, f"{questions_answers_unban['peer_id']}")
                ban_info = self.users_info[self.user_id].user_conversation[f"{questions_answers_unban['peer_id']}"].punishments["ban"]
                if not ban_info.get("unban"):
                    ban_info["unban"] = True
                self.users_info[self.user_id].user_conversation[f"{questions_answers_unban['peer_id']}"].update = True
                action = "success"

                peer_ids_dict = {
                    "status": False,
                    "permission": False,
                    "processed": False,
                    "user_id_bot": self.user_id_bot,
                    "peer_id": peer_id,
                    "current_time": self.current_time
                }

                task = TaskUserBot(user_id=self.user_id)
                task.self_generator(
                    await self.manager_db.user_insert_one(task.class_dict, self.task_user_bot_documents))
                task.peer_ids.append(peer_ids_dict)
                task_id = len(task.peer_ids) - 1
                await self.manager_db.user_update_one(task.class_dict, self.task_user_bot_documents)


            elif questions_answers_unban["count_questions"] >= questions_answers_unban["unban_questions_count"]:
                msg = "Вы ответили на недостаточное количество вопросов, ваша попытка разбана сгорает🔥"
                action = "failed"
                unban.active = False

            else:
                question = questions_answers_unban["questions"][questions_answers_unban["count_questions"]]
                msg = f"Ответ принят.\n\n{question['question']}"


            await self.manager_db.user_update_one(unban.class_dict, self.unban_documents)


        return_dict = {"message": msg, "action": action, "peer_id": peer_id,
                       "user_id_bot": self.user_id_bot, "task_id": task_id}

        return return_dict


if __name__ == "__main__":
    from motor import MotorClient
    from mongodb import MongoManager
    import asyncio
    import yaml
    with open('../description_commands.yaml', encoding="utf-8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
    # pprint(read_data)
    loop = asyncio.get_event_loop()
    uri = 'mongodb://localhost:27017'
    client = MotorClient(uri)

    mongo_manager = MongoManager(client)
    #wok = WorkUser(mongo_manager, 55, 100) self.settings_info = await self.manager_db.settings_get_one(self.settings_documents)

    loop.run_until_complete(mongo_manager.settings_update_one(read_data, "settings"))
    settings_info = loop.run_until_complete(mongo_manager.settings_insert_one(read_data, "settings"))

    # test2 = loop.run_until_complete(wok.lvl_cmd_add_list({"xp": 12345}, "profile"))
    # test2 = loop.run_until_complete(wok.lvl_list({"xp": 700}))
    # test2 = loop.run_until_complete(wok.achievements_check(user_info_list=[123456]))
    # test2 = loop.run_until_complete(wok.add_ban_user(user_id=123456, peer_id=2000001, cause="Спам"))
    #test2 = loop.run_until_complete(wok.add_warn_user(user_id=123456, peer_id=2000001, cause="Спам"))

    #  wok = WorkUser(mongo_manager, settings_info,  55, 100)

    #unban = UnbanLs(mongo_manager, settings_info,  123456, 100)
    unban = UnbanLs(mongo_manager, settings_info, current_time=300)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    #test2 = loop.run_until_complete(unban.record_list_peer_ids())
    #test2 = loop.run_until_complete(unban.run(peer_id_number=1))
    # test2 = loop.run_until_complete(unban.run(answer_number=1))
    #test2 = loop.run_until_complete(unban.task_user_bot_unban())
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    test2 = loop.run_until_complete(unban.unban_all(400))
    # pprint(test2)
    print(test2)

