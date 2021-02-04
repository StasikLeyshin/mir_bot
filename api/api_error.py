# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import json
import ujson

import logging

from log.log import logger

class api_error:
    
    def __init__(self, club_id, token, **kwargs):
        
        self.club_id = club_id
        self.token = token
        self.kwargs = kwargs    
    
    async def error(self, link=""):
    
        if "error" in self.kwargs:
            #logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - [%(name)s] - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            #logger = logging.getLogger(__name__)
            logger.error(f'club_id: {self.club_id} | error_code: {self.kwargs["error"]["error_code"]} | {self.kwargs["error"]["error_msg"]} | method: {self.kwargs["error"]["request_params"][1]["value"]} | link: {link}')
            return {"code": 0, "errcode": self.kwargs["error"]["error_code"], "error": self.kwargs["error"]["error_msg"]}
        elif "failed" in self.kwargs:
            logger.error(f'club_id: {self.club_id} | error_code: {self.kwargs["failed"]} | failed | method: failed | link: {link}')
            return {"code": 0, "errcode": self.kwargs["failed"], "failed": self.kwargs["failed"]}
        else:
            return {"code": 1}
            
        
        
        