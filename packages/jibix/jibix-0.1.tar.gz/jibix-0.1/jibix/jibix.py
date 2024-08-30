import json

class Jibix(dict):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.reload()
    
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


        