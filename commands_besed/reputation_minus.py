import traceback

import command_besed
from commands import commands

class reputation_minus(commands):

    async def run(self):
        try:
            adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            if adm:
                user_id = await self.getting_user_id()
                if user_id:
                    res = await self.create_mongo.profile_users_add(user_id, scores=-0.25)
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"✅ Осуждение оказано ([id{user_id}|-0.25])",
                                             random_id=0, forward=self.answer_msg())
                    return
            res = await self.create_mongo.profile_users_add(self.from_id, reputation_minus=self.date, f=1)
            if res:
                user_id = await self.getting_user_id()
                if not user_id:
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="⚠ Тут что-то не так, а вот что, это предстоит понять тебе)",
                                             random_id=0, forward=self.answer_msg())
                    return
                elif str(user_id) == str(self.from_id):
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="Самодизлайк залог провала.",
                                             random_id=0, forward=self.answer_msg())
                    return
                adm_new = await self.create_mongo.admin_check(user_id, self.peer_id)
                if not adm_new:
                    ach = ""
                    await self.create_mongo.profile_users_add(user_id, scores=-0.25)
                    res = await self.create_mongo.profile_users_add(self.from_id, reputation_minus=self.date)
                    if int(res) in self.reputation_minus_awards:
                        res_new = await self.create_mongo.profile_users_add(self.from_id,
                                                                        f"😈 {self.reputation_minus_awards[int(res)][0]}",
                                                                        self.reputation_minus_awards[int(res)][1])
                        ach = f"\n\n👻 [id{self.from_id}|Вы] получили ачивку:\n\n😈 {self.reputation_minus_awards[int(res)][0]}\n\n" \
                              f"📊 Рейтинг: {res_new[1]}"
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message=f"✅ Осуждение оказано ([id{user_id}|-0.25]){ach}",
                                             random_id=0, forward=self.answer_msg())

        except Exception as e:
            print(traceback.format_exc())

reputation_minuss = command_besed.Command()

reputation_minuss.keys = ['uyrjthgrf', 'rtytheruyjtiko']
reputation_minuss.description = 'Минус репутация'
reputation_minuss.process = reputation_minus
reputation_minuss.topics_blocks = []
reputation_minuss.topics_resolution = ["tema1"]
