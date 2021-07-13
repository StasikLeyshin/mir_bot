
from datetime import datetime

from api.api_execute import inf
from record_achievements import record_achievements

class warn_give_out:

    def __init__(self, v):
        self.v = v

    async def display_time(self, seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])


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

        res_warn = await create_mongo.add_warn(user_id, peer_id, cause, int(vrem) + result[0], result[0], from_id)
        if res_warn == -1:
            return False, "Это вообще кто?😳"


        #res = await create_mongo.profile_users_add(user_id, )
        res = []
        msg_n = ""
        if len(res_warn) == 3:
            res = await record_achievements(create_mongo, user_id).run(res_warn[1], res_warn[2])
        else:
            res = await record_achievements(create_mongo, user_id).run(res_warn[1])
        if res[1]:
            msg_n = "\n\n👻 Полученные ачивки:\n" + "\n".join(res[1])

        if res[0] == 1:
            timestamp = 604800 + int(result[0])
            value = datetime.fromtimestamp(timestamp)
            time = value.strftime('%d.%m.%Y %H:%M')
            await create_mongo.ban_check(user_id, peer_id, "Рейтинг достиг отметки ниже -30", 604800 + result[0],
                                         result[0], from_id)
            ply = await self.display_time(604800)
            msg = f"{name}, вам бан на {ply}\n📝 Причина: Рейтинг достиг отметки ниже -30\n⏰ Время окончания: {time}\n\n" \
                  f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.{msg_n}\n\n📊 Рейтинг: {res[2]}"
            return True, msg

        elif res[0] == 2:
            res_new = await create_mongo.globan_add(user_id, result[0], from_id, "Рейтинг достиг отметки ниже -50")
            if res_new[0] == 1:
                msg = f"Данный [id{user_id}|пользователь] добавлен в глобальный бан.\n\n" \
                      f"📝 Причина: Рейтинг достиг отметки ниже -50.\n\n" \
                      f"P.S. Оттуда ещё никто не возвращался..."
                return True, msg, res_new[1]
            elif res_new[0] == 2:
                msg = f"Данный [id{user_id}|пользователь] уже есть в глобальном бане.\n\n" \
                      f"P.S. И он оттуда скорее всего не вернётся..."
                return True, msg, res_new[1]


        elif res[0] == 0:
            timestamp = int(vrem) + int(result[0])
            value = datetime.fromtimestamp(timestamp)
            time = value.strftime('%d.%m.%Y %H:%M')

        if res_warn[0] != 3:
            if cause != -1:
                msg = f"{name}, вам выдан варн [{res_warn[0]}/3] на {ply} \n📝 Причина: {cause}\n⏰ Время окончания: {time}{msg_n}\n\n📊 Рейтинг: {res[2]}" # от администратора" \
                      #f" {im}" \
                      #f"\n📝 Причина: {cause}\n⏰ Время окончания: {time}"
            else:
                msg = f"{name}, вам выдан варн [{res_warn[0]}/3] на {ply}\n⏰ Время окончания: {time}{msg_n}\n\n📊 Рейтинг: {res[2]}" # от администратора" \
                      #f" {im}" \
                      #f"\n⏰ Время окончания: {time}"
            return False, msg
        else:
            await create_mongo.ban_check(user_id, peer_id, cause, int(vrem) + result[0], result[0],
                                         from_id)
            if cause != -1:
                msg = f"{name}, достигнут лимит варнов, поэтому бан на {ply}\n📝 Причина: {cause}\n⏰ Время окончания: {time}\n\n" \
                      f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.{msg_n}\n\n📊 Рейтинг: {res[2]}"  # от администратора" \
                # f" {im}" \
                # f"\n📝 Причина: {cause}\n⏰ Время окончания: {time}"
            else:
                msg = f"{name}, достигнут лимит варнов, поэтому бан на {ply}\n⏰ Время окончания: {time}\n\n" \
                      f"🎁 У вас есть одна попытка разбана на одну беседу. Напишите в мои личные сообщения 'разбан' без кавычек.{msg_n}\n\n📊 Рейтинг: {res[2]}"  # от администратора" \
                # f" {im}" \
                # f"\n⏰ Время окончания: {time}"
            return True, msg




    def ban_out(self): pass