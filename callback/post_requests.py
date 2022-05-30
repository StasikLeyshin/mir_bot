from aiohttp import web
import time


from middlewares import SimpleHandler
from settings import *
from edite_text import opredel_skreen, chunks


async def executor_post(request: web.Request):
    #print(await request.text())
    event = await request.json()
    #event = await request.text()
    #tasks.append(loop.create_task(inf.main(apis[i["id"]], i["id"], i["them"])))
    #print(event)
    if "type" in event:
        if event['type'] == "confirmation":
            return web.Response(text="9d5be991")
        if event['type'] == "message_new":

            #LS
            if event['object']["message"]["from_id"] == event['object']["message"]["peer_id"]:
                #LS
                loop.create_task(
                    SimpleHandler(V, event['group_id'], event['object']["message"], apis[event['group_id']],
                                  loop_control[event['group_id']],
                                  create_mongo, collection_bots, document_tokens, url_dj, loop).middleware_ls())

            elif event['object']["message"]["from_id"] != event['object']["message"]["peer_id"]:
                #BS
                loop.create_task(
                    SimpleHandler(V, event['group_id'], event['object']["message"], apis[event['group_id']],
                                  loop_control[event['group_id']],
                                  create_mongo, collection_bots, document_tokens, url_dj, loop).middleware_ls(True))


        # if loop_control[event['group_id']] == "tema1":
        #     if event['type'] == "message_new":
        #             # loop.create_task(processing(V, event['group_id'], event['object']["message"], apis[event['group_id']], "tema1",
        #             #                             create_mongo,
        #             #                             collection_bots,
        #             #                             document_tokens,
        #             #                             url_dj).run(bad_words))
        #         if event['object']["message"]["from_id"] == event['object']["message"]["peer_id"]:
        #             loop.create_task(SimpleHandler(V, event['group_id'], event['object']["message"], apis[event['group_id']],
        #                                            loop_control[event['group_id']],
        #                                            create_mongo, collection_bots, document_tokens, url_dj, loop).middleware_ls())
        #         else:
        #             pass
        # #print(event)
        # elif loop_control[event['group_id']] == "zluka":
        #     if event['type'] == "message_new":
        #         loop.create_task(SimpleHandler(V, event['group_id'], event['object']["message"],
        #                                        apis[event['group_id']],
        #                                        loop_control[event['group_id']],
        #                                        create_mongo,
        #                                        collection_bots, document_tokens, url_dj, loop).middleware_ls())
        return web.Response(text="ok")
    if "token" in event and "soc" in event and "id" not in event:
        result = await api(0, event["token"]).api_get("groups.getById", v=f"{V}")
        if "error" not in result:
            data = {"status": 1, "id": result[0]["id"], "name": result[0]["name"]}
            apis[result[0]["id"]] = api(result[0]["id"], event["token"])
            spis.append({"id": result[0]["id"], "name": result[0]["name"], "token": event["token"], "them": event["soc"]})
            '''create_mongo.create_db(collection_bots,
                                   document_tokens,
                                   [{"id": result[0]["id"],
                                     "name": result[0]["name"],
                                     "token": event["token"],
                                     "them": event["soc"]}],
                                   [result[0]["id"]])'''
            await tokens_setting(V).main([event["token"]], [result[0]["id"]])
            loop_control[result[0]["id"]] = event["soc"]
            loop.create_task(inf.main(apis[result[0]["id"]], result[0]["id"], event["soc"], loop_control, loop))

        else:
            data = {"status": 0}

        return web.json_response(data)

    elif "id" in event:
        result = await api(0, event["token"]).api_get("groups.getById", v=f"{V}")
        if "error" not in result:
            #print("------------------")
            data = {"status": 1, "id": result[0]["id"], "name": result[0]["name"]}
            #print(event["id"], spis)
            token = apis[event["id"]].token
            del apis[event["id"]]
            for i in spis:
                if i["id"] == event["id"]:
                    soc = i["them"]
                    spis.remove(i)
                    break
            apis[result[0]["id"]] = api(result[0]["id"], event["token"])
            spis.append({"id": result[0]["id"], "name": result[0]["name"], "token": event["token"], "them": event["soc"]})
            if token != event["token"]:
                loop_control[result[0]["id"]] = event["soc"]
                loop.create_task(inf.main(apis[result[0]["id"]], result[0]["id"], event["soc"], loop_control))
            if loop_control[result[0]["id"]] != event["soc"]:
                loop_control[result[0]["id"]] = event["soc"]
                loop.create_task(inf.main(apis[result[0]["id"]], result[0]["id"], event["soc"], loop_control))


        else:
            data = {"status": 0}

        return web.json_response(data)

    elif "token" in event and "user_link" in event:
        screen_name = await opredel_skreen(event["user_link"], event["user_link"])
        #print(screen_name)
        result = await api(0, event["token"]).api_get("users.get", v=V, user_ids=screen_name)
        if "error" not in result:
            user_id = result[0]["id"]
            data = {"status": 1, "user_id": user_id}
        else:
            data = {"status": 0}
        return web.json_response(data)

    elif "token" in event and "question" in event:
        start_time = time.time()
        users = create_mongo.users_get()
        ran = ["🌝 Вопрос дня и уже у тебя в личных сообщениях, скорее отвечай!",
               "👾 Новый день, новый вопрос, новые возможности, и это всё доступно тебе уже сейчас, можешь уже отвечать:)",
               "🌚 Утро позднее, утро раннее, а вопрос дня неизменно уже у тебя)",
               "👻 Новый вопрос! Бегом отвечать!"
               ]
        #users_new = await chunks(users, 100)
        #for i in users_new:
        result = loop.create_task(collecting_list_users(V, event['club_id']).run(users,
                                                                                 api(event['club_id'],
                                                                                     event['token']),
                                                                                 event['question'],
                                                                                 event['question_id']))
        '''result = loop.create_task(api(0, event["token"]).api_post("messages.send", v=V, peer_ids=i,
                                                                      message=f"{random.choice(ran)}\n\n"
                                                                      f"{event['question']}\n\n"
                                                                      f"⚠ Чтобы ответить на вопрос, напишите /ответ номер вопроса и ваш ответ\n\n"
                                                                      f"❗Номер текущего вопроса: {event['question_id']}",
                                                                      random_id=0))'''
        #await asyncio.sleep(1)

        '''import requests
        result = requests.post("https://api.vk.com/method/messages.send", data={
        "access_token": event["token"],
        "v": 5.103,
        "random_id": 0,
        "message": "1111",
        "peer_ids":users})'''
        result = ""
        if "error" in result:
            data = {"status": 0}
        else:
            data = {"status": 1}
        return web.json_response(data)


    return web.json_response({"status": 0})