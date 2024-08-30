import json
import os

class Jibix(dict):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.make_file()
        self.reload()
    
    def make_file(self):
        if not os.path.exists(self.name) or not os.path.getsize(self.name):
            with open(self.name, '+w') as fp:
                fp.write('{}')
    
    def reload(self):
        with open(self.name, 'rb') as fp:
            super().update(json.load(fp))
            
    def commit(self):
        with open(self.name, '+w') as fp:
            fp.write(json.dumps(self))
    
    def __setitem__(self, key, value):
        super().update({key:value})
        self.commit()
    
    def __getattr__(self, name: str) :
        return super().get(name)
    
    def pop(self, key):
        super().pop(key)
        
    def update(self, update):
        super().update(update)
        self.commit()
        
import aiofile
import asyncjson
  
class AsyncJibix:
        def __init__(self, name):
            self.name = name
            super().__init__()
        
        async def make_file(self):
            if not os.path.exists(self.name) or not os.path.getsize(self.name):
                async with aiofile.async_open(self.name, '+w') as fp:
                    fp.write('{}')
        
        async def reload(self):
            async with aiofile.async_open(self.name, '+w') as fp:
                super().update(json.loads(await fp.read()))
                
        async def commit(self):
            async with aiofile.async_open(self.name, '+w') as fp:
                await fp.write(await asyncjson.dumps(self))
        
        async def __setitem__(self, key, value):
            super().update({key:value})
            await self.commit()
        
        def __getattr__(self, name: str) :
            return super().get(name)
        
        async def pop(self, key):
            await super().pop(key)
            await self.commit()
            
        async def update(self, update):
            super().update(update)
            self.commit()


        