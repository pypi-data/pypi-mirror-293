import json
import math

from json import JSONEncoder

from nizaba.api import set_history

def nan2None(obj):
    if isinstance(obj, dict):
        return {k:nan2None(v) for k,v in obj.items()}
    elif isinstance(obj, list):
        return [nan2None(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

class NanConverter(JSONEncoder):
    def encode(self, obj, *args, **kwargs):
        return super().encode(nan2None(obj), *args, **kwargs)

def nzb_create(
        self
):
    
    def f(*args, **kwargs):
        completion = self.chat.completions._NZB_create(*args, **kwargs)
    
        new_message = dict(completion.choices[0].message)
    
        all_messages = kwargs.get("messages", []) + [new_message]
    
        data = json.loads(json.dumps(all_messages, cls=NanConverter))
    
        set_history(data)
    
        return completion
    
    return f

def nzb_init(
        self, *args, **kwargs
):
    
    self._NZB__init__(*args, **kwargs)
    
    self.chat.completions._NZB_create = self.chat.completions.create
    
    self.chat.completions.create = nzb_create(self)
    
def init():
    import openai
    
    if not hasattr(openai.OpenAI, "_NZB__init__"):
        openai.OpenAI._NZB__init__ = openai.OpenAI.__init__
    
        openai.OpenAI.__init__ = nzb_init