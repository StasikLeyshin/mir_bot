# -*- coding: utf-8 -*-
import asyncio
import json
import ujson
import os
import time


from api.api import api
from vkscript_converter.definitions import vkscript
from api.api_execute import api_one_run

class tokens_setting:

    def __init__(self, v):
        
        self.v = v
        
    
    async def main(self, tokens_new, ids):
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        #print("Files in %r: %s" % (cwd, files))
        start_time = time.time()
        print("Vtoroe --- %s seconds ---" % (time.time() - start_time))
        for i, j in zip(tokens_new, ids):
            await api(j, i).api_post("execute", code=api_one_run(v=self.v, group_id=j), v=self.v)
        print("Tretee --- %s seconds ---" % (time.time() - start_time))
                       
            
            
            
            
            
            
            
            
            
            
            