
import traceback

import command_besed
from commands import commands
from record_achievements import achievements
from summer_module.reputation.rep_minus import RepMinus


class rep_minus(commands):

    async def run(self):
        try:

            user_id = await self.getting_user_id()
            if not user_id:
                # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                          message="⚠ Тут что-то не так, а вот что, это предстоит понять тебе)",
                #                          random_id=0, forward=self.answer_msg())
                return
            else:
                if str(user_id) == str(self.from_id):
                    await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                             message="Самодизлайк залог провала.",
                                             random_id=0, forward=self.answer_msg())
                    return
                number_issued = await self.getting_number()

                rep = RepMinus(self.mongo_manager, self.settings_info, int(self.from_id), int(self.date))
                result = await rep.run(user_id=int(user_id), peer_id=int(self.peer_id), number_issued=number_issued)
                if result['message']:
                    if not result['error']:
                        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                 message=result['message'],
                                                 random_id=0, forward=self.answer_msg(), keyboard=self.pusto())
                    else:
                        if await self.ls_open_check(self.from_id):
                            await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
                                                     message=result['message'],
                                                     random_id=0)
                        else:
                            await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                                     message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
                                                     forward=self.answer_msg(),
                                                     random_id=0)
            await self.apis.api_post("messages.delete", v=self.v, peer_id=self.peer_id,
                                     conversation_message_ids=self.conversation_message_id,
                                     delete_for_all=1)
                # print("number_issued", number_issued)
                # res = await achievements(self.client, int(user_id), self.v).minus_rep(
                #     apis=self.apis, peer_id=self.peer_id,
                #     user_id=self.from_id, start_time=self.date, number_issued=number_issued)
                # if res:
                #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                #                              message=res,
                #                              random_id=0, forward=self.answer_msg(), keyboard=self.pusto())

            # if await self.ls_open_check(self.from_id):
            #     user_id = await self.getting_user_id()
            #     if not user_id:
            #         user_id = self.from_id
            #     #msg = await self.info_user(user_id)
            #     # await self.apis.api_post("messages.send", v=self.v, peer_id=self.from_id,
            #     #                          message=msg, random_id=0)
            #     await achievements(self.client, int(user_id), self.v).plus_rep(
            #         apis=self.apis, peer_id=self.peer_id,
            #         user_id=self.from_id)
            # else:
            #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                              message="⚠ Я не могу вам написать. Разрешите мне отправку сообщения в лс, для этого напишите мне любое сообщение",
            #                              random_id=0)
            #
            # adm = await self.create_mongo.admin_check(self.from_id, self.peer_id)
            # if adm:
            #     user_id = await self.getting_user_id()
            #     if user_id:
            #         res = await self.create_mongo.profile_users_add(user_id, scores=0.25)
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                                  message=f"✅ Уважение оказано ([id{user_id}|+0.25])",
            #                                  random_id=0, forward=self.answer_msg(), keyboard=self.pusto())
            #         return
            # res = await self.create_mongo.profile_users_add(self.from_id, reputation_plus=self.date, f=1)
            # if res:
            #     user_id = await self.getting_user_id()
            #     if not user_id:
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                                  message="⚠ Тут что-то не так, а вот что, это предстоит понять тебе)",
            #                                  random_id=0, forward=self.answer_msg())
            #         return
            #     elif str(user_id) == str(self.from_id):
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                                  message="Самолайк залог успеха.",
            #                                  random_id=0, forward=self.answer_msg())
            #         return
            #     adm_new = await self.create_mongo.admin_check(user_id, self.peer_id)
            #     if not adm_new:
            #         await self.create_mongo.profile_users_add(user_id, scores=0.25)
            #         res = await self.create_mongo.profile_users_add(self.from_id, reputation_plus=self.date)
            #         ach = ""
            #         if int(res) in self.reputation_plus_awards:
            #             res_new = await self.create_mongo.profile_users_add(self.from_id,
            #                                                             f"😇 {self.reputation_plus_awards[int(res)][0]}",
            #                                                             self.reputation_plus_awards[int(res)][1])
            #             ach = f"\n\n👻 [id{self.from_id}|Вы] получили ачивку:\n\n😇 {self.reputation_plus_awards[int(res)][0]}\n\n" \
            #                   f"📊 Рейтинг: {res_new[1]}"
            #         await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                                  message=f"✅ Уважение оказано ([id{user_id}|+0.25]){ach}",
            #                                  random_id=0, forward=self.answer_msg())
            # else:
            #     await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
            #                              message=f"⛔ Все попытки за день израсходованы",
            #                              random_id=0, forward=self.answer_msg())
        except Exception as e:
            print(traceback.format_exc())


rep_minuss = command_besed.Command()

rep_minuss.keys = ['осудить', 'осуждаю', '-rep', 'rep-', '-реп', 'реп-']
rep_minuss.description = 'Минус реп'
rep_minuss.set_dictionary('rep_minus')
rep_minuss.process = rep_minus
rep_minuss.topics_blocks = []
rep_minuss.topics_resolution = ["tema1"]

if __name__ == "__main__":
    import re
    text = "23 gffd 44 5"
    ger = re.findall(r'(?<!\w)\d+(?!\w)', text)
    print(ger)
