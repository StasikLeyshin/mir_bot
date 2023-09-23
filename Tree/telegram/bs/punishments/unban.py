from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.punishments.unban import UnbanLs



class unbanLs(commands):

    async def run(self):
        unban = UnbanLs(self.mongo_manager, self.settings_info, self.from_id, self.date)

        result = await unban.task_user_bot_unban_check()

        flag = False

        if result["message"]:
            from settings import apis, user_bot_id

            flag = True
            keyboard = self.generations_keyboard_unban([])
            is_friends = await apis[int(user_bot_id)].api_post("friends.areFriends", v=self.v,
                                             user_ids=f"{self.from_id}")

            if is_friends[0]["friend_status"] == 1:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"👶 Примите заявку от Стаса: https://vk.com/id{user_bot_id}\n\n"
                                                 f"❗ Стас добавит вас в нужную беседу",
                                         random_id=0, keyboard=keyboard)

            if is_friends[0]["friend_status"] == 0:
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"👶 Добавьте Стаса в друзья: https://vk.com/id{user_bot_id}\n\n"
                                                 f"❗ Стас добавит вас в нужную беседу",
                                         random_id=0, keyboard=keyboard)

            if is_friends[0]["friend_status"] == 2:
                await apis[int(user_bot_id)].api_post("friends.add", v=self.v,
                                                      user_id=int(self.from_id))
                is_friends[0]["friend_status"] = 3
            if is_friends[0]["friend_status"] == 3:
                result = await unban.task_user_bot_unban()

                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=f"Начинаю процедуру вашего разбана",
                                         random_id=0, keyboard=keyboard)
                for i in result['peer_ids']:
                    group_id = abs(2000000000 - i)
                    chat_id = group_id
                    await apis[int(user_bot_id)].api_post("messages.addChatUser", v=self.v, chat_id=chat_id,
                                                          user_id=self.from_id, visible_messages_count=1000)

        result = await unban.record_list_peer_ids()
        names = []
        if len(result["peer_ids"]) > 0:
            res = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                           peer_ids=", ".join(str(x) for x in result["peer_ids"]))

            j = 1
            for i in res["items"]:
                names.append(f"{j}. {i['chat_settings']['title']}")
                j += 1
        elif flag:
            return
        keyboard = self.generations_keyboard_unban([str(i + 1) for i in range(0, len(result["peer_ids"]))])
        await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                 message=result["message"] + "\n".join(names),
                                 random_id=0,
                                 keyboard=keyboard)



unbanLss = command_ls.Command()

unbanLss.keys = ['разбан', '/разбан']
unbanLss.description = 'разбан'
unbanLss.set_dictionary('unban_ls')
unbanLss.process = unbanLs
#endless_questionss.mandatory = True
unbanLss.topics_blocks = []
unbanLss.topics_resolution = ["tema1"]
