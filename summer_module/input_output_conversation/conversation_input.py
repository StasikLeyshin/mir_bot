from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import BanGive
from summer_module.user_conversation import WorkUser, checking_admin


class ConversationInput(WorkUser):

    async def run(self, user_id: int, peer_id_zl: int, type_input: str = None):
        return_dict = await self._add_bs_user(user_id, peer_id_zl, type_input)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id, attempt, cause):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "attempt": attempt,
            "cause": cause
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, attempt, cause, type_input):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": type_input,
            "attempt": attempt,
            "cause": cause
        }
        return log_dict

    async def log_user(self, user_id, peer_id, attempt, cause, type_input):
        user_conversation = self.users_info[user_id].user_conversation[f"{peer_id}"]
        user_conversation.log[type_input].append(await self.get_log_users(self.user_id, peer_id, attempt,
                                                                                  cause))

        if self.users_info[self.user_id].admin:
            self.users_info[self.user_id].admin.log[type_input].append(await self.get_log_users(user_id,
                                                                                                        peer_id,
                                                                                                        attempt, cause))
            self.users_info[self.user_id].admin.update = True

        await self.add_log(await self.get_log_general(user_id, peer_id, attempt, cause, type_input))

        user_conversation.update = True

    async def _add_bs_user(self, user_id: int, peer_id_zl: int, type_input: str = None):
        action = False
        update = False
        msg = ""
        kick_id = []
        conversation_zl = await self.get_conversation_zl(peer_id_zl)
        peer_id = conversation_zl.peer_id
        if peer_id == 0:
            #msg = "❗ Привяжите беседу."
            return_dict = {"message": msg, "action": action, "update": update, "kick_id": kick_id, "peer_id": peer_id}
            return return_dict

        # info = await self.manager_db.user_get_one(user_id, f"{peer_id}")
        # if not info and not type_input:
        #     type_input = "chat_invite_user_by_link"

        await self.get_user_conversation(user_id, f"{peer_id}")

        await self.get_user(user_id)

        user_conversation = self.users_info[user_id].user_conversation[f"{peer_id}"]

        user_conversation.output = False
        user_conversation.kicked = False

        if self.user_id == user_id:
            if not type_input:
                type_input = "chat_returned_user"
            if user_conversation.punishments["ban"].get("status"):
                end_time_msg = await unix_to_time(user_conversation.punishments["ban"]["finish_time"])
                msg = f"⚠ [id{user_id}|Вы] находитесь в бане до {end_time_msg}.\n👋 До свидания."
                action = "kick"
                attempt = False
                cause = "ban"
                kick_id.append(user_id)
                return_dict = {"message": msg, "action": action, "update": update,
                               "kick_id": kick_id, "peer_id": peer_id}
                await self.log_user(user_id, peer_id, attempt, cause, type_input)
                return return_dict
        else:
            type_input = "chat_invite_user"
            adm = await self.is_admin(self.user_id, f"{peer_id}")
            if adm["flag"]:
                await self.get_admin(self.user_id, adm["role"])
                if user_conversation.punishments["ban"].get("status"):
                    if not user_conversation.punishments["ban"].get("unban"):
                        end_time_msg = await unix_to_time(user_conversation.punishments["ban"]["finish_time"])
                        msg = f"⚠ Данный [id{user_id}|пользователь] находится в бане до " \
                              f"{end_time_msg}.\n\n" \
                              f"😡 Приглашение пользователя, не прошедшего официальный способ разабана, " \
                              f"нарушает экономику бота."
                        action = "kick"
                        cause = "unban"
                        attempt = False
                        kick_id.append(user_id)
                        return_dict = {"message": msg, "action": action,
                                       "update": update, "kick_id": kick_id, "peer_id": peer_id}

                        await self.log_user(user_id, peer_id, attempt, cause, type_input)
                        return return_dict
                    else:
                        msg = f"⚠ Данного [id{user_id}|пользователя], " \
                              f"находившегося в бане, пригласил администратор.\n" \
                              f"Так уж и быть, сниму с него бан.😌",
                        user_conversation.punishments["ban"]["status"] = False
                        attempt = True
                        cause = ""
                        return_dict = {"message": msg, "action": action,
                                       "update": update, "kick_id": kick_id, "peer_id": peer_id}
                        await self.log_user(user_id, peer_id, attempt, cause, type_input)
                        return return_dict
            else:
                if user_conversation.punishments["ban"].get("status"):
                    msg = f"⚠ Несанкционированное проникновение, кик обоих."
                    action = "kick"
                    kick_id.append(self.user_id)
                    kick_id.append(user_id)
                    attempt = False
                    cause = "ban"
                    return_dict = {"message": msg, "action": action,
                                   "update": update, "kick_id": kick_id, "peer_id": peer_id}
                    await self.log_user(user_id, peer_id, attempt, cause, type_input)
                    return return_dict

        attempt = True
        cause = ""
        await self.log_user(user_id, peer_id, attempt, cause, type_input)
        return_dict = {"message": msg, "action": action, "update": update,
                       "kick_id": kick_id, "peer_id": peer_id}
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

    #ban = BanGive(mongo_manager, settings_info,  55, 100)
    con = ConversationInput(mongo_manager, settings_info,  55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(con.run(user_id=123456, peer_id_zl=238))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
