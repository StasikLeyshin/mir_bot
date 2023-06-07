from Tree.step_back.step_back import step_back
from commands import commands
import command_ls
from summer_module.punishments.unban import UnbanLs
from summer_module.work_ls.work_ls import WorkLs
from api import api


class AutomaticUnban(commands):

    async def run(self):
        unban = UnbanLs(self.mongo_manager, self.settings_info, self.from_id, self.date)
        work_ls = WorkLs(manager_db=self.mongo_manager, settings_info=self.settings_info, user_id=self.from_id)
        res = await work_ls.location_tree_check()
        if not res.ignore_tree:
            result = await unban.run(peer_id_number=int(self.text))
            res.ignore_tree = True
            await work_ls.location_tree_update()
            #keyboard = self.generations_keyboard_not_back_button([i for i in range(1, len(result["peer_ids"]))])
            api_new = api(self.club_id,
                          "7e57e7ab0bd4508a517b94cd935cea6c7f41698d363994ecfa6a77671a32a8fb7441297abf5ae785e254a")
            await api_new.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                     message=result["message"],
                                     random_id=0, expire_ttl=60,
                                     keyboard=self.keyboard_empty())
        else:
            result = await unban.run(answer_number=int(self.text))
            #print(result)
            if result["action"] == "failed":
                await self.step_back_bool_new(res, work_ls)
                #result = await unban.run(peer_id_number=int(self.text))
                res.ignore_tree = False
                await work_ls.location_tree_update()
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=result["message"],
                                         random_id=0,
                                         keyboard=self.keyboard_empty())
            elif result["action"] == "success":
                await self.step_back_bool_new(res, work_ls)
                #result = await unban.run(peer_id_number=int(self.text))
                res.ignore_tree = False
                await work_ls.location_tree_update()
                res = await self.apis.api_post("messages.getConversationsById", v=self.v,
                                               peer_ids=f"{result['peer_id']}")
                names = []
                for i in res["items"]:
                    names.append(f"{i['chat_settings']['title']}")
                await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=result["message"].format(names[0]),
                                         random_id=0,
                                         keyboard=self.keyboard_empty())
                msg = f"👣 Данный [id{self.from_id}|пользователь] прошёл процедуру разбана\n\n" \
                      f"👥 Беседа: '{names[0]}'\n\n" \
                      "⚖ Разбанить?"
                await self.apis.api_post("messages.send", v=self.v, peer_id=2000000039,
                                         message=msg,
                                         random_id=0,
                                         keyboard=self.keyboard_unban(
                                             f"{self.from_id}@{self.date}@{result['task_id']}"),
                                         forward=self.answer_msg_other())
            else:
                api_new = api(self.club_id,
                              "7e57e7ab0bd4508a517b94cd935cea6c7f41698d363994ecfa6a77671a32a8fb7441297abf5ae785e254a")
                await api_new.api_post("messages.send", v=self.v, peer_id=self.peer_id,
                                         message=result["message"],
                                         random_id=0, expire_ttl=60,
                                         keyboard=self.keyboard_empty())


        # keyboard = self.generations_keyboard([i for i in range(1, len(result["peer_ids"]))])
        # await self.apis.api_post("messages.send", v=self.v, peer_id=self.peer_id,
        #                          message=result["message"],
        #                          random_id=0,
        #                          keyboard=keyboard)



automatic_unbans = command_ls.Command()

automatic_unbans.keys = [r'(?<!\w)\d(?!\w)']
automatic_unbans.regular = True
automatic_unbans.description = 'разбан'
automatic_unbans.set_dictionary('automatic_unban')
automatic_unbans.process = AutomaticUnban
#endless_questionss.mandatory = True
automatic_unbans.topics_blocks = []
automatic_unbans.topics_resolution = ["tema1"]


if __name__ == "__main__":
    import re
    result = re.findall(r'(?<!\w)\d(?!\w)', '4 rgergrg3 5 ')
    #result = re.findall(r'/wmeste', ' 4 rgergrg3 5 ')
    #result = re.findall(r'^\d(?!\w)', ' 4 rgergrg3 5 ')
    print(result)
    #print(type((1, 2)))

    # key_list = ['заварнить', 'бан', 'глобальный бан']
    # text = "[club194180799 | @ club194180799] разбанить"
    # flag = False
    # for k in key_list:
    #
    #     if k == text or k == text[1:]:
    #         flag = True
    #         break
    #     elif k == text.split(" ")[0] or k == text.split(" ")[0][1:]:
    #         flag = True
    #         break
    #     if text != 'chat_invite_user' and text != 'chat_invite_user_by_link':
    #         if k in text:
    #             flag = True
    #             break
    # print(flag)
