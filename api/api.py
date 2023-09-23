# -*- coding: utf-8 -*-
import aiohttp
import aiofiles
import asyncio
import json
import ujson
import requests
import time

from api.api_error import api_error

class api:


    def __init__(self, club_id, token, is_telegram=False):

        self.club_id = club_id
        self.token = token
        self.is_telegram = is_telegram
        #self.method = method
        #self.kwargs = kwargs
        self.start_time = time.time()



    async def api_get(self, method, **kwargs):

        strings = []
        #print(kwargs)
        for key, item in kwargs.items():
            strings.append("{}={}".format(key.capitalize().lower(), item))
            #print(strings)

        result = "&".join(strings)
        result1 = ", ".join(strings)
        #result = '='.join([f'{key.capitalize()}: {value}' for key, value in kwargs[0].items()])
        link = f"https://api.vk.com/method/{method}?{result}&access_token={self.token}&lang=ru"
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:

                d = await response.json(loads=ujson.loads)
                if_error = api_error(self.club_id, self.token, **d)
                check = await if_error.error(link)

                if check["code"] == 1:
                    return d["response"]

                elif check["code"] == 0:
                    return check


    async def api_post(self, method, **kwargs):
        if self.is_telegram:
            link = f"https://api.telegram.org/bot{self.token}/{method}"
        else:
            kwargs["access_token"] = self.token
            kwargs["lang"] = "ru"
            link = f"https://api.vk.com/method/{method}?"
        connector = aiohttp.TCPConnector(limit_per_host=500)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(link, data=kwargs) as response:

                d = await response.json(loads=ujson.loads)
                if_error = api_error(self.club_id, self.token, **d)
                check = await if_error.error(link)

                if check["code"] == 1:
                    if self.is_telegram:
                        return d["result"]
                    return d["response"]

                elif check["code"] == 0:
                    return check


class api_url:

    def __init__(self, url):

        self.url = url


    async def get_json(self, club_id=0):
        link = f"{self.url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                d = await response.json(loads=ujson.loads)
                if club_id != 0:
                    if_error = api_error(club_id, "empty", **d)
                    check = await if_error.error(self.url)
                    if check["code"] == 1:
                        return d

                    elif check["code"] == 0:
                        return check
                return d

    async def post_json(self, **kwargs):
        link = f"{self.url}"
        async with aiohttp.ClientSession() as session:
            async with session.post(link, data=kwargs) as response:
                print(await response.text())
                d = await response.json(loads=ujson.loads)
                if_error = api_error(0, "empty", **d)
                check = await if_error.error(self.url)

                if check["code"] == 1:
                    return d

                elif check["code"] == 0:
                    return check

    async def get_html(self):
        link = f"{self.url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers={'Connection': 'keep-alive'}) as response:
                d = await response.text()
                #response.close()
            #await session.close()
            return d
            #session.close()

                #if_error = api_error(club_id, "empty", **d)
                #check = await if_error.error(self.url)
                #if check["code"] == 1:
                    #return d

                #elif check["code"] == 0:
                    #return check

    async def post_files(self, **kwargs):


        #async with aiohttp.ClientSession() as session:
            #async with session.post(f"{self.url}", files=kwargs) as response:
        response = requests.post(self.url, files=kwargs)
        d = response.json()
        if_error = api_error(0, "empty", **d)
        check = await if_error.error(self.url)

        if check["code"] == 1:
            return d

        elif check["code"] == 0:
            return check

    async def download_img(self, name):
        async with aiohttp.ClientSession() as session:
            #url = "http://host/file.img"
            async with session.get(self.url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f'{name}', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

    async def post_upload(self, name):
        with open(f'{name}', 'rb') as f:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, data={'file': f}) as response:
                    #print(await response.json())
                    try:
                        d = await response.json(loads=ujson.loads)
                    except:
                        d = await response.json(content_type='text/html')
                    if_error = api_error(0, "", **d)
                    check = await if_error.error(self.url)

                    if check["code"] == 1:
                        return d

                    elif check["code"] == 0:
                        return check




