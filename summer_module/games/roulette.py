import random
from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin


class Roulette(WorkUser):


    async def run(self, peer_id: int, number_issued: int, **kwargs):


        return_dict = await self._roulette(peer_id, number_issued)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id, number_issued, status_victory, xp):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "number_issued": number_issued,
            "status_victory": status_victory,
            "xp": xp
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, number_issued, status_victory, xp):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "roulette",
            "number_issued": number_issued,
            "status_victory": status_victory,
            "xp": xp
        }
        return log_dict

    async def _roulette(self, peer_id: int, number_issued: int = 0):
        await self.get_user(self.user_id)
        user_info = self.users_info[self.user_id].user
        user_info_cmd = await self.lvl_cmd_add_list(user_info.class_dict, "roulette")
        msg = ""
        error = False
        rul = {
            1: (-13, 9),
            2: (-18, 13),
            3: (-23, 17),
            4: (-28, 21),
            5: (-33, 25)
        }
        if "roulette" in user_info_cmd:
            if number_issued >= 1:
                if number_issued < 6:
                    if user_info.cmd["roulette"].get("finish_time"):
                        if user_info.cmd["roulette"]["finish_time"] <= self.current_time:
                            user_info.cmd["roulette"]["finish_time"] = self.current_time +\
                                                                       user_info_cmd['limit']['roulette_default_time']
                            user_info.cmd["roulette"]["start_time"] = self.current_time
                        else:
                            end_time_msg = await unix_to_time(user_info.cmd["roulette"]["finish_time"])
                            msg = f"🔌 Ваш пистолет на подзарядке, приходите после {end_time_msg}"
                            error = True
                            return_dict = {"message": msg, "error": error}
                            return return_dict
                    else:
                        user_info.cmd["roulette"]["finish_time"] = self.current_time + \
                                                                   user_info_cmd['limit']['roulette_default_time']
                        user_info.cmd["roulette"]["start_time"] = self.current_time
                    user_info.update = True
                    ran = random.randint(1, 6)
                    if ran > number_issued:
                        status_victory = True
                        await self.set_count_cmd(user_info, "roulette")

                        achievements = self.settings_info["roulette_awards"]
                        await self.give_achievement(self.user_id, user_info.cmd["roulette"]["count"],
                                                    achievements, user_info.achievements, "roulette")

                        await self.set_user_xp(self.user_id, self.users_info[self.user_id].user)
                        msg_ach = ""
                        if self.users_info[self.user_id].achievements:
                            msg_ach = f"\n\n👻 [id{self.user_id}|Вы] получили ачивку:\n" + \
                                      "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])

                        ran = rul[number_issued][1]
                    else:
                        status_victory = False
                        ran = rul[number_issued][0]


                    user_info.xp += ran * user_info_cmd['multiplier']
                    xp = ran * user_info_cmd['multiplier']

                    await self.add_log_user(user_info, "roulette",
                                            await self.get_log_users(self.user_id, peer_id, number_issued, status_victory, xp))

                    await self.add_log(await self.get_log_general(self.user_id, peer_id, number_issued, status_victory, xp))

                    if ran < 0:
                        msg = f"😭 К сожалению вы проиграли."
                    else:
                        msg = f"🤠 Сегодня фортуна на вашей стороне, вы победили.{msg_ach}"

                    return_dict = {"message": msg, "error": error}

                else:
                    msg = f"😳 Как я столько пуль в барабан заряжу, только если солью или дробью, но так не интересно"
                    error = True
                    return_dict = {"message": msg, "error": error}
                    return return_dict
            elif number_issued == 0:
                msg = "🧐 Холостой пистолет не заряжаем"
                error = True
                return_dict = {"message": msg, "error": error}
                return return_dict
            else:
                msg = f"😳 Это куда ж минус то, пуля назад лететь будет??"
                error = True
                return_dict = {"message": msg, "error": error}
                return return_dict
        return_dict = {"message": msg, "error": error}
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

    rep = Roulette(mongo_manager, settings_info, 55, 100000)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(rep.run(peer_id=2000001, number_issued=5))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
