

from abc import ABC, abstractmethod
from datetime import datetime

from summer_module.convert import unix_to_time, convert_seconds_to_human_time, num2text
from summer_module.user_conversation import WorkUser, checking_admin


class RepMinus(WorkUser):


    async def run(self, user_id: int, peer_id: int, number_issued: int, **kwargs):


        return_dict = await self._rep_minus(user_id, peer_id, number_issued)
        await self.update_all_user_new()
        return return_dict

    async def get_log_users(self, user_id, peer_id, number_issued):
        log_dict = {
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "number_issued": number_issued
        }
        return log_dict

    async def get_log_general(self, user_id, peer_id, number_issued):
        log_dict = {
            "user_id": self.user_id,
            "from_id": user_id,
            "peer_id": peer_id,
            "current_time": self.current_time,
            "type": "reputation_minus",
            "number_issued": number_issued
        }
        return log_dict

    async def _rep_minus(self, user_id: int, peer_id: int, number_issued: int = 0):
        await self.get_user(self.user_id)
        user_info = self.users_info[self.user_id].user
        user_info_cmd = await self.lvl_cmd_add_list(user_info.class_dict, "reputation_minus")
        msg = ""
        error = False
        if "reputation_minus" in user_info_cmd:
            info = await self.manager_db.user_get_one(user_id, self.users_documents)
            if not info:
                msg = "👽 Такого пользователя не существует"
                error = True
                return_dict = {"message": msg, "error": error}
                return return_dict

            is_admin = await self.is_admin(self.user_id, str(peer_id))

            if user_info.influence > 0 or is_admin["flag"]:
                await self.get_user(user_id)
                from_user_info = self.users_info[user_id].user
                if not number_issued:
                    number_issued = user_info_cmd["limit"]["influence_default_minus"]
                sum_xp = 0
                for i in range(number_issued):
                    if user_info.influence > 0:
                        sum_xp += 1 * user_info_cmd['multiplier']
                        if not is_admin["flag"]:
                            user_info.influence -= 1
                from_user_info.xp -= sum_xp

                user_info.update = True
                from_user_info.update = True

                if user_info.cmd["reputation_minus"].get("count"):
                    user_info.cmd["reputation_minus"]["count"] += 1
                else:
                    user_info.cmd["reputation_minus"]["count"] = 1

                achievements = self.settings_info["reputation_minus_awards"]

                await self.give_achievement(self.user_id, user_info.cmd["reputation_minus"]["count"],
                                            achievements, user_info.achievements, "reputation_minus")

                await self.set_user_xp(self.user_id, self.users_info[self.user_id].user)

                user_info.log["reputation_minus"].append(await self.get_log_users(user_id, peer_id, sum_xp))
                #from_user_info.log["reputation_plus"].append(await self.get_log_users(self.user_id, peer_id, sum_xp))

                await self.add_log(await self.get_log_general(user_id, peer_id, sum_xp))


                msg_ach = ""
                if self.users_info[self.user_id].achievements:
                    msg_ach = f"\n\n👻 [id{self.user_id}|Вы] получили ачивку:\n" + \
                              "\n".join([i['text'] for i in self.users_info[self.user_id].achievements])
                msg = f"✅ Осуждение оказано ([id{user_id}|-{round(sum_xp, 2)}]){msg_ach}"
                #return_dict = {"message": msg}
                #return return_dict

            else:
                msg = "😧 У вас закончилась репутация"
                error = True
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

    rep = RepMinus(mongo_manager, settings_info, 55, 100)

    #test2 = loop.run_until_complete(wok.test(user_id=123456, peer_id=2000001, from_id_check=True))
    test2 = loop.run_until_complete(rep.run(user_id=123456, peer_id=2000001, number_issued=4))
    # test2 = loop.run_until_complete(wok.add_warn_user(user_info=123456, cause="Спам"))
    # pprint(test2)
    print(test2)
