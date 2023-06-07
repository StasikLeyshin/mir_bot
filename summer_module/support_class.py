

async def lvl_cmd_add_list(user, cmd, settings_info: dict):
    #settings = await self.manager_db.settings_get_one(self.settings_documents)
    command_level = settings_info["command_level"]
    xp = user["xp"]
    cmd_dict = {}
    sum_xp = 0
    for i in command_level:
        sum_xp += i["xp"]
        if xp >= sum_xp:
            if i.get("cmd_list"):
                for j in i["cmd_list"]:
                    if cmd == j["cmd"]:
                        cmd_dict[cmd] = j
        else:
            break
        cmd_dict["limit"] = i["limit"]
    return cmd_dict


async def lvl_list(user, settings_info: dict):
    command_level = settings_info["command_level"]
    xp = user["xp"]
    cmd_dict = {}
    sum_xp = 0
    end_xp = 0
    for i in command_level:
        cmd_dict["lvl"] = i["lvl"]
        sum_xp += i["xp"]
        end_xp = i["xp"]
        if xp >= sum_xp or sum_xp == 0:
            cmd_dict["limit"] = i["limit"]
            cmd_dict["multiplier"] = i["multiplier"]
        else:
            break

    if end_xp <= 0:
        cmd_dict["lvl_percent_short"] = int((xp - (sum_xp - end_xp)) / end_xp * 10)
        cmd_dict["lvl_percent"] = int((xp - (sum_xp - end_xp)) / end_xp * 100)
    else:
        cmd_dict["lvl_percent_short"] = 0
        cmd_dict["lvl_percent"] = 0
    if cmd_dict["lvl"] != 0:
        cmd_dict["lvl"] -= 1

    return cmd_dict


async def is_admin(manager_db, user_id: int, users_documents_bs: str, users_admin_documents: str, settings_info: dict):
    flag = False
    return_dict = {"flag": flag}
    for i in settings_info["user_id_admins"]:
        if user_id == i:
            flag = True
            return_dict = {"flag": flag,
                           "role": settings_info["role_admin"][len(settings_info["role_admin"]) - 1]}
            break
    if not flag:
        info = await manager_db.user_get_one(user_id, users_documents_bs)
        if info:
            if info["admin"]:
                flag = True
                return_dict = {"flag": flag,
                               "role": settings_info["role_admin"][0]}
    if not flag:
        info = await manager_db.user_get_one(user_id, users_admin_documents)
        if info:
            if info["status"]:
                flag = True
                return_dict = {"flag": flag,
                               "role": info["role"]}
    return return_dict
