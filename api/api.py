# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import json
import ujson

from api.api_error import api_error

class api:


    def __init__(self, club_id, token):

        self.club_id = club_id
        self.token = token
        #self.method = method
        #self.kwargs = kwargs



    async def api_get(self, method, **kwargs):

        strings = []
        #print(kwargs)
        for key,item in kwargs.items():
            strings.append("{}={}".format(key.capitalize().lower(), item))
            #print(strings)

        result = "&".join(strings)
        result1 = ", ".join(strings)
        #result = '='.join([f'{key.capitalize()}: {value}' for key, value in kwargs[0].items()])
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.vk.com/method/{method}?{result}&access_token={self.token}") as response:

                d = await response.json(loads = ujson.loads)
                if_error = api_error(self.club_id, self.token, **d)
                check = await if_error.error()

                if check["code"] == 1:
                    return d["response"]

                elif check["code"] == 0:
                    return check


    async def api_post(self, method, **kwargs):

        kwargs["access_token"] = self.token
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api.vk.com/method/{method}?", data=kwargs) as response:

                d = await response.json(loads = ujson.loads)
                if_error = api_error(self.club_id, self.token, **d)
                check = await if_error.error()

                if check["code"] == 1:
                    return d["response"]

                elif check["code"] == 0:
                    return check


class api_url:

    def __init__(self, url):

        self.url = url


    async def get_json(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}") as response:
                d = await response.json(loads=ujson.loads)
                if_error = api_error(0, "empty", **d)
                check = await if_error.error()
                if check["code"] == 1:
                    return d

                elif check["code"] == 0:
                    return check





