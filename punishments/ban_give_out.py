
from datetime import datetime

from api.api_execute import inf

class ban_give_out:

    def __init__(self, v):
        self.v = v


    async def ban_give(self, apis, create_mongo, peer_id, cause, chat_id, user_id, from_id, vrem, ply):

        adm = await create_mongo.admin_check(user_id, peer_id)
        if adm == 1:
            if user_id[0] == "-":
                msg = f"⚠ Данная [club{user_id[1:]}|группа] является администратором беседы"
            else:
                msg = f"⚠ Данный [id{user_id}|пользователь] является администратором беседы"
            return False, msg

        if user_id[0] == "-":
            result = await apis.api_post("execute", code=inf(v=self.v, id=user_id, f=0, from_id=from_id), v=self.v)
            name = "[club"+str(user_id[1:])+"|"+str(result[1]) + "]"
            im = f"[id{from_id}|{result[2]} {result[3]}]"
        else:
            result = await apis.api_post("execute", code=inf(v=self.v, id=user_id, f=1, from_id=from_id), v=self.v)
            name = "[id" + str(user_id) + "|" + str(result[1]) + " " + str(result[2]) + "]"
            im = f"[id{from_id}|{result[3]} {result[4]}]"

        res_ban = await create_mongo.ban_check(user_id, peer_id, cause, int(vrem) + result[0], result[0], user_id)

        if res_ban == -1:
            return False, "Это вообще кто?😳"

        if res_ban == 0:
            if user_id[0] == "-":
                msg = f"⚠ Данная [club{user_id[1:]}|группа] уже находится в бане"
            else:
                msg = f"⚠ Данный [id{user_id}|пользователь] уже находится в бане"
            return False, msg

        timestamp = int(vrem) + int(result[0])
        value = datetime.fromtimestamp(timestamp)
        time = value.strftime('%d.%m.%Y %H:%M')
        if cause != -1:
            msg = f"{name}, бан на {ply}\n📝 Причина: {cause}\n⏰ Время окончания: {time}\n" \
                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек."  # от администратора" \
                  #f" {im}" \
                  #f"\n📝 Причина: {cause}\n⏰ Время окончания: {time}"
        else:
            msg = f"{name}, бан на {ply}\n⏰ Время окончания: {time}\n" \
                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек."  # от администратора" \
                  #  f" {im}" \
                  #  f"\n⏰ Время окончания: {time}"
        return True, msg




    def ban_out(self): pass