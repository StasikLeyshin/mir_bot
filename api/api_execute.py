# -*- coding: utf-8 -*-
import json
import ujson


from vkscript_converter.definitions import vkscript


@vkscript
def api_one_run(v, group_id):
    d = api.groups.getLongPollSettings(v=v, group_id = group_id)
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