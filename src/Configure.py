import json

from Exception import *

class DataType:

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataType, cls).__new__(cls,*args,**kwargs)
        return cls.instance
    
    def set_value(self, val):
        self.val = val

    def as_bool(self):
        return bool(self.val)
    
    def as_int(self):
        return int(self.val)

    def as_float(self):
        return float(self.val)
    
    def as_string(self):
        return str(self.val)
    
    def raw(self):
        return self.val

class AIWConfigure(object):

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AIWConfigure, cls).__new__(cls,*args,**kwargs)
        return cls.instance
    
            
    @classmethod
    def init(cls):
        with open("../config/aiw_config.json", 'r') as f:
            cls._root = json.load(f)
        if not hasattr(cls, '_root'):
            raise AIWConfigureLoadException("Could not load ai server config file.")
    
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'inited'):
            cls.init()
            cls.inited = True
        return cls
        
    @classmethod
    def get_config_info(cls, s) -> DataType:
        tmp = DataType()
        tmp.set_value(cls._root[s])
        return tmp