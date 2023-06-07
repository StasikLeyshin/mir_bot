from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.punishments import BanGive
from summer_module.user_conversation import WorkUser, checking_admin


class WorkUserBot(WorkUser):

    async def run(self, peer_id: int, peer_id_zl: int, is_user_bot: bool = False):
        return_dict = await self._add_bs_zl(peer_id, peer_id_zl, is_user_bot)
        return return_dict

    async def _add_user(self, peer_id: int, peer_id_zl: int, is_user_bot: bool):
        conversation_zl = await self.get_conversation_zl(peer_id_zl, is_user_bot)
        if conversation_zl.peer_id == 0:
            conversation_zl.peer_id = peer_id
            await self.update_conversation_zl(conversation_zl, is_user_bot)
            if is_user_bot:
                msg = "Сохранил себе эту беседку"
            else:
                msg = "/update"
        else:
            msg = "⚠ Беседа уже была привязана"
        return_dict = {"message": msg}
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
    #con = ConversationInput(mongo_manager, settings_info,  55, 100)
    con = Binding(mongo_manager, settings_info)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(con.run(peer_id=2000002, peer_id_zl=239))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
