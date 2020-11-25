# -*- coding: utf-8 -*-
import asyncio
import json
import ujson
import os
import time


from api import api
from api.api_execute import api_one_run

class tokens_setting:

    def __init__(self, v):
        
        self.v = v
        
    
    async def main(self, tokens_new, ids):
        for i, j in zip(tokens_new, ids):
            await api(j, i).api_post("execute", code=api_one_run(v=self.v, group_id=j), v=self.v)
        return
                       
            
            
            
            
            
            
            
            
            
            
            