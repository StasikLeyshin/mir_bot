import random

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import WarnGive, BanGive
from summer_module.user_conversation import WorkUser, checking_admin, Zawarn


class WarnAdminCheck(WorkUser):

    async def add_zawarn(self, user_id, peer_id: int, conversation_message_id_forward: int,
                  conversation_message_id_original: int, type_sms: str, **kwargs):
        #return_dict = await self._add_bs_user(self.user_id, peer_id_zl)
        return_dict = await self._zawarn(user_id, peer_id, conversation_message_id_forward,
                                         conversation_message_id_original, type_sms)
        #await self.update_all_user_new()
        return return_dict

    async def _zawarn(self, user_id, peer_id: int, conversation_message_id_forward: int,
                      conversation_message_id_original: int, type_sms: str):
        action = False
        update = False
        is_delete = False
        msg = ""
        kick_id = []

        zawarn = Zawarn(user_id=self.user_id, from_id=user_id, peer_id=peer_id,
                        conversation_message_id_forward=conversation_message_id_forward,
                        conversation_message_id_original=conversation_message_id_original,
                        current_time=self.current_time,
                        type_sms=type_sms)
        zawarn.self_generator(
            await self.manager_db.zawarn_insert_one(zawarn.class_dict, self.zawarn_documents))

        return True


    async def apply_punishment(self, peer_id, user_id, current_time, conversation_message_id_forward,
                               type_sms, type_punishment):

        return_dict = await self._apply_punishment(peer_id, user_id, current_time, conversation_message_id_forward,
                                                   type_sms, type_punishment)
        await self.update_all_user_new()
        return return_dict


    async def _apply_punishment(self, peer_id, user_id, current_time, conversation_message_id_forward,
                               type_sms, type_punishment):

        result = await self.manager_db.zawarn_get_one(from_id=user_id,
                                                    conversation_message_id_forward=conversation_message_id_forward,
                                                    current_time=current_time,
                                                    documents=self.zawarn_documents)
        #print(result)
        messages = []
        if result:
            if not result["status"]:
                if type_sms == "swear":
                    cause = "Использование ненормативной лексики"
                elif type_sms == "neg":
                    cause = "Слишком негативное высказывание"
                elif type_sms == "rep":
                    cause = "Нарушение правил чата"

                zawarn = Zawarn(from_id=user_id,
                                conversation_message_id_forward=conversation_message_id_forward,
                                current_time=current_time,
                                type_sms=type_sms)
                zawarn.self_generator(result)
                zawarn.status = True
                await self.manager_db.user_update_one(zawarn.class_dict, self.zawarn_documents)

                if zawarn.user_id != self.club_id and type_sms == "rep":
                    msg = f"Ваш репорт на данного [id{user_id}|пользователя] был успешно обработан ✅\n" \
                          f"♟ Начислил вам трайб поинты."

                    await self.get_user(zawarn.user_id)
                    user_info = self.users_info[zawarn.user_id].user
                    lvl_list = await self.lvl_list(user_info.xp)
                    user_info.tribe_points += lvl_list["limit"]["report_default_tribe_points"]
                    user_info.update = True

                    messages.append({"message": msg, "peer_id": zawarn.user_id})

                if type_punishment == "wr":
                    res = await WarnGive(self.manager_db, self.settings_info, self.user_id, self.current_time,
                                         self.users_info).run(user_id=user_id, peer_id=zawarn.peer_id, cause=cause)
                    res["conversation_message_id"] = zawarn.conversation_message_id_forward
                    messages.append(res)
                elif type_punishment == "bn":
                    res = await BanGive(self.manager_db, self.settings_info, self.user_id, self.current_time,
                                        self.users_info).run(user_id=user_id, peer_id=zawarn.peer_id, cause=cause)
                    res["conversation_message_id"] = zawarn.conversation_message_id_forward
                    messages.append(res)
                messages.append({"message": f"Данный [id{user_id}|пользователь] жёстко наказан ✅", "peer_id": peer_id})
            else:
                msg = f"Данный [id{user_id}|пользователь] уже был обработан ❌"
                messages.append({"message": msg, "peer_id": peer_id})
        else:
            msg = f"Я ничего не нашёл ❌"
            messages.append({"message": msg, "peer_id": peer_id})

        return_dict = {"messages": messages}

        return return_dict



    async def get_log_users(self, peer_id, type_sms, message):
        log_dict = {
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type_sms": type_sms,
        }
        return log_dict

    async def get_log_general(self, peer_id, type_sms, message):
        log_dict = {
            "user_id": self.user_id,
            "from_id": self.user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "sms",
            "type_sms": type_sms,
        }
        for i in log_dict:
            message[i] = log_dict[i]
        return message

    async def log_user(self, peer_id, type_sms, message):
        #user_conversation = self.users_info[self.user_id].user_conversation[f"{peer_id}"]
        #user_conversation.log["sms"].append(await self.get_log_users(peer_id, type_sms))

        # if self.users_info[self.user_id].admin:
        #     self.users_info[self.user_id].admin.log["sms"].append(await self.get_log_users(user_id,
        #                                                                                                 peer_id,
        #                                                                                                 attempt, cause))
        #     self.users_info[self.user_id].admin.update = True

        await self.add_log(await self.get_log_general(peer_id, type_sms, message))
        await self.add_sms_log(await self.get_log_general(peer_id, type_sms, message))

        #user_conversation.update = True



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

    #ban = BanGive(mongo_manager, settings_info,  55, 100)
    con = WarnAdminCheck(mongo_manager, settings_info, 55, 500)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    # test2 = loop.run_until_complete(con.add_zawarn(user_id=123456, peer_id=2000001, conversation_message_id_forward=12,
    #                                      conversation_message_id_original=3, type_sms="swear"))

    test2 = loop.run_until_complete(con.apply_punishment(peer_id=2000002, user_id=123456, current_time=432,
                                                   conversation_message_id_forward=12, type_sms="rep",
                                                   type_punishment="wr"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
