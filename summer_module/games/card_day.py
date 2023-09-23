import random
from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin


class CardDay(WorkUser):


    async def run(self, peer_id: int, **kwargs):


        return_dict = await self._card_day(peer_id)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "card_day",
        }
        return log_dict

    async def _card_day(self, peer_id: int):
        await self.get_user(self.user_id)
        user_info = self.users_info[self.user_id].user
        user_info_cmd = await self.lvl_cmd_add_list(user_info.class_dict, "card_day")
        msg = ""
        error = False
        file = ""
        if "card_day" in user_info_cmd:
            if not user_info.cmd.get("card_day"):
                user_info.cmd["card_day"] = {}
            if user_info.cmd["card_day"].get("finish_time"):
                if user_info.cmd["card_day"]["finish_time"] <= self.current_time:
                    user_info.cmd["card_day"]["finish_time"] = self.current_time +\
                                                               user_info_cmd['limit']['card_day_default_time']
                    user_info.cmd["card_day"]["start_time"] = self.current_time
                else:
                    end_time_msg = await unix_to_time(user_info.cmd["card_day"]["finish_time"])
                    msg = f"🙅‍♀ Рамона сегодня тебе уже погадала, яхонтовый соколик мой.\n" \
                          f"💁‍♀ Вас много, а я одна. Дай и другим получить свое предсказание, будь котиком.\n\n" \
                          f"🤫 Вот времечко, после которого, ты не будешь прежним: {end_time_msg}"
                    error = True
                    return_dict = {"message": msg, "file": file, "error": error}
                    return return_dict
            else:
                user_info.cmd["card_day"]["finish_time"] = self.current_time + \
                                                           user_info_cmd['limit']['card_day_default_time']
                user_info.cmd["card_day"]["start_time"] = self.current_time
            user_info.update = True
            await self.set_count_cmd(user_info, "card_day")

            achievements = self.settings_info["card_day_awards"]
            await self.give_achievement(self.user_id, user_info.cmd["card_day"]["count"],
                                        achievements, user_info.achievements, "card_day")

            await self.set_user_xp(self.user_id, self.users_info[self.user_id].user)
            msg_ach = ""
            if self.users_info[self.user_id].achievements:
                msg_ach = f"\n\n👻 [id{self.user_id}|Вы] получили ачивку:\n" + \
                          "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])

            value = random.choice(self.settings_info["taro"])

            await self.add_log_user(user_info, "card_day",
                                    await self.get_log_users(self.user_id, peer_id))

            await self.add_log(await self.get_log_general(self.user_id, peer_id))

            msg = f"{value['text']}{msg_ach}"
            file = "Таро/" + value['file'] + ".jpg"

        return_dict = {"message": msg, "file": file, "error": error}
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

    rep = CardDay(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(rep.run(peer_id=2000001))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
