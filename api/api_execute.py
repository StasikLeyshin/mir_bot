# -*- coding: utf-8 -*-
import json
import ujson


from vkscript_converter.definitions import vkscript


@vkscript
def api_one_run(v, group_id):
    d = api.groups.getLongPollSettings(v=v, group_id=group_id)
    if d.is_enabled != true:
        api.groups.setLongPollSettings(v=v, group_id=group_id, enabled=1, api_version=v, message_new=1, message_reply=1, message_allow=1, message_deny = 1, message_edit = 1, wall_reply_new = 1, wall_reply_edit = 1, wall_reply_delete = 1, wall_reply_restore = 1, wall_post_new = 1, wall_repost = 1, photo_comment_new = 1, photo_comment_edit = 1, photo_comment_delete = 1, photo_comment_restore = 1, video_comment_new = 1, video_comment_edit = 1, video_comment_delete = 1, video_comment_restore = 1, group_join = 1, group_leave = 1, group_change_settings = 1, group_officers_edit = 1, user_block = 1, user_unblock = 1, message_event = 1, message_typing_state = 1)
    return 1


@vkscript
def mailing(v, users, group_id):
    sp = []
    j = 0
    for i in users:
        d = api.messages.isMessagesFromGroupAllowed(v=v, group_id=group_id, user_id=i)
        if d.is_allowed == 1:
            sp.append(i)
        j = j + 1
        #api.messages.send(v=v, random_id=0, peer_id=i, message=message)
    return sp

@vkscript
def inf(v, id, f, from_id):
    m = []
    vre = api.utils.getServerTime()
    m.append(vre)
    if f == 0:
        gname = api.groups.getById(group_id=id)
        m.append(gname[0].name)
        admin = api.users.get(user_ids=from_id, name_case="'gen'", fields="'first_name, last_name'")
        m.append(admin[0].first_name)
        m.append(admin[0].last_name)
    else:
        chel = api.users.get(user_ids=id, fields="'first_name, last_name'")
        m.append(chel[0].first_name)
        m.append(chel[0].last_name)
        admin = api.users.get(user_ids=from_id, name_case="'gen'", fields="'first_name, last_name'")
        m.append(admin[0].first_name)
        m.append(admin[0].last_name)
    return m

@vkscript
def kick(users, chat_id):
    #names = []
    #u = users.split(" ")
    #u = ['363434084', '454049560']
    #if flag == 1:
        #api.messages.send(peer_id = peer_id, random_id = 0, message = "Сейчас вас кикну. Если хотите вернуться, напишите кикнувшему администратору https://vk.com/id"+ from_id)
    for i in users:
        #while i < l:
        #if u[i][0] == "-":
        #api.messages.removeChatUser(chat_id = chat_id, member_id = u[i])
        #else:
        api.messages.removeChatUser(chat_id=chat_id, member_id=i)
        #names.append(user.first_name)
    return 1
