import json
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class CommandsTg:
    def __init__(self, v, club_id, message, apis, them, create_mongo, collection_bots, document_tokens, url_dj,
                 client=None, tree_questions=None, mongo_manager=None, settings_info=None):
        self.v = v
        self.club_id = club_id
        self.message = message
        self.peer_id = self.message["peer_id"]
        self.from_id = self.message["from_id"]
        self.date = self.message["date"]
        self.id_sms = self.message["id"]
        self.text = self.message["text"]
        self.conversation_message_id = 0
        self.message_id = self.message["id"]
        self.fwd_messages = []
        self.attachments = []
        self.apis = apis
        self.them = them
        self.create_mongo = create_mongo
        self.collection_bots = collection_bots
        self.document_tokens = document_tokens
        self.url_dj = url_dj
        self.client = client
        self.tree_questions = tree_questions
        self.mongo_manager = mongo_manager
        self.settings_info = settings_info
        self.admin_list = [447019454]

    def is_int(self, s):
        try:
            int(s)
            return True
        except:
            return False

    async def getting_number(self, limit=20):
        try:
            s = [int(s) for s in re.findall(r'(?<!\w)\d+(?!\w)', self.text.lower())]
            for i in s:
                if i < limit:
                    return i
            return 1
        except:
            return 1


    async def getting_user_id(self):

        if self.message["message"].get("reply_to_message"):
            #if "reply_message" in self.message:
            user_id = self.message["message"]["reply_to_message"]["from"]["id"]
            first_name = self.message["message"]["reply_to_message"]["from"]["first_name"]
            username = self.message["message"]["reply_to_message"]["from"]["username"]
            # else:
            #     user_id = self.fwd_messages[0]["from_id"]
            if self.is_int(user_id):
                user_id = str(user_id)
                return user_id, first_name, username
            else:
                return False
        # if "@" in self.text.lower():
        #     mention = re.search(r'@(\w+)', self.text)
        #     user_id = self.apis.resolve_peer(mention.group(1))
        #     first_name = self.message["message"].reply_to_message.first_name
        #     username = self.message["message"].reply_to_message.username
        #     return user_id, first_name, username
        return False

    async def txt_warn(self, g):
        l = g.find('\n')
        if l == -1:
            return ''
        k = g[l:]
        k = k.replace(".", " ")
        k = k.replace("\n", "")
        k = k.lstrip()
        return k

    async def admin_chek(self, user_id, chat_id):
        #adm_list = self.apis.get_chat_administrators(chat_id)
        adm_list = await self.apis.api_post("getChatAdministrators", chat_id=self.peer_id)
        for i in adm_list:
            if int(i["user"]["id"]) == int(user_id):
                return True
        return False

    async def generations_keyboard(self, cmd_list):
        # markup = InlineKeyboardMarkup()
        # for i in cmd_list:
        #     txt = i[1]
        #     # if len(i[1]) > 40:
        #     #     txt = str(i[1][:37]) + "..."
        #     markup.add(InlineKeyboardButton(txt, callback_data=i[1]))
        # return markup
        keyboard_list = []
        for i in cmd_list:
            txt = i[1]
            # if len(i[1]) > 40:
            #     txt = str(i[1][:37]) + "..."
            if "шаг назад" not in txt.lower():
                keyboard_list.append([{"text": txt, "callback_data": txt}])
        keyboard_list.append([{"text": "Шаг назад", "callback_data": "Шаг назад"}])
        keyboard = {
            "inline_keyboard": keyboard_list
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def menu(self):
        # markup = InlineKeyboardMarkup()
        # #for i in cmd_list:
        # markup.add(InlineKeyboardButton("Помощь по приёму", callback_data="Помощь по приёму"))
        # return markup
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Помощь по приёму", "callback_data": "Помощь по приёму"}
                ]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard