from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import BanGive
from summer_module.user_conversation import WorkUser, checking_admin


class ConversationOutput(WorkUser):

    async def run(self, user_id: int, peer_id_zl: int):
        return_dict = await self._add_bs_user(user_id, peer_id_zl)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, type_output):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": type_output,
        }
        return log_dict

    async def log_user(self, user_id, peer_id, type_output):
        user_conversation = self.users_info[user_id].user_conversation[f"{peer_id}"]
        user_conversation.log[type_output].append(await self.get_log_users(self.user_id, peer_id))

        if self.users_info[self.user_id].admin:
            self.users_info[self.user_id].admin.log[type_output].append(await self.get_log_users(user_id, peer_id))
            self.users_info[self.user_id].admin.update = True

        await self.add_log(await self.get_log_general(user_id, peer_id, type_output))

        user_conversation.update = True

    async def _add_bs_user(self, user_id: int, peer_id_zl: int):
        action = False
        update = False
        msg = ""
        kick_id = []
        type_output = ""
        conversation_zl = await self.get_conversation_zl(peer_id_zl)
        peer_id = conversation_zl.peer_id
        if peer_id == 0:
            #msg = "❗ Привяжите беседу."
            return_dict = {"message": msg, "action": action, "update": update, "kick_id": kick_id, "peer_id": peer_id}
            return return_dict

        await self.get_user_conversation(user_id, f"{peer_id}")

        await self.get_user(user_id)

        user_conversation = self.users_info[user_id].user_conversation[f"{peer_id}"]


        if self.user_id == user_id:
            user_conversation.output = True
            user_conversation.kicked = False
            if not type_output:
                type_output = "chat_exit_user"

        else:
            user_conversation.kicked = True
            user_conversation.output = False
            if not type_output:
                type_output = "chat_kick_user"
            adm = await self.is_admin(self.user_id, f"{peer_id}")
            if adm["flag"]:
                await self.get_admin(self.user_id, adm["role"])

            else:
                if user_conversation.punishments["ban"].get("status"):
                    msg = f"⚠ Не зарегестрированный кик пользователя."
                    action = "kick"
                    kick_id.append(self.user_id)
                    kick_id.append(user_id)
                    return_dict = {"message": msg, "action": action,
                                   "update": update, "kick_id": kick_id, "peer_id": peer_id}
                    await self.log_user(user_id, peer_id, type_output)
                    return return_dict

        attempt = True
        cause = ""
        await self.log_user(user_id, peer_id, type_output)
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
    # wok = WorkUser(mongo_manager, 55, 100) self.settings_info = await self.manager_db.settings_get_one(self.settings_documents)

    loop.run_until_complete(mongo_manager.settings_update_one(read_data, "settings"))
    settings_info = loop.run_until_complete(mongo_manager.settings_insert_one(read_data, "settings"))

    # test2 = loop.run_until_complete(wok.lvl_cmd_add_list({"xp": 12345}, "profile"))
    # test2 = loop.run_until_complete(wok.lvl_list({"xp": 700}))
    # test2 = loop.run_until_complete(wok.achievements_check(user_info_list=[123456]))
    # test2 = loop.run_until_complete(wok.add_ban_user(user_id=123456, peer_id=2000001, cause="Спам"))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_id=123456, peer_id=2000001, cause="Спам"))

    #  wok = WorkUser(mongo_manager, settings_info,  55, 100)

    # ban = BanGive(mongo_manager, settings_info,  55, 100)
    con = ConversationOutput(mongo_manager, settings_info, 1234, 100)

    # test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(con.run(user_id=1234, peer_id_zl=238))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
