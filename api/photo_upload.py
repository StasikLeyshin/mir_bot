# -*- coding: utf-8 -*-


import requests
import os
import traceback

from api import api, api_url


class photo_upload:

    def __init__(self, apis, V,  peer_id, file, pyt="C:/Users/Zett/Desktop/ПИИИИТОООН/mir_bot/media/"):

        self.apis = apis
        self.V = V
        self.peer_id = peer_id
        self.file = file
        self.pyt = pyt

    async def upload(self):
        try:
            print(f"{self.pyt}{self.file}")
            print("PEER_ID: ", self.peer_id)
            url = await self.apis.api_post("photos.getMessagesUploadServer", v=self.V, peer_id=self.peer_id)
            if "error" not in url:
                upload_url = url["upload_url"]
                print(upload_url)
                with open(f"{self.pyt}{self.file}", 'rb') as f:
                    #server = requests.post(upload_url, files={"photo": f})
                    server = await api_url(upload_url).post_files(photo=f)
                #print(server)
                ff = open(f"{self.pyt}{self.file}", 'rb')
                print(ff)
                ser = server["server"]
                photo = server["photo"]
                print(photo)
                hash = server["hash"]
                att = await self.apis.api_post("photos.saveMessagesPhoto", v=self.V, photo=photo, server=ser, hash=hash)
                print(att)
                if "error" not in att:
                    #< type > < owner_id > _ < media_id >
                    res = f"photo{att[0]['owner_id']}_{att[0]['id']}"
                    return res
        except Exception as e:
            print(traceback.format_exc())