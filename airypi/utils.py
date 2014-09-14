import json
from flask import g, session, request
import message_queue

def json_unicode(obj):
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, o):
            return o.to_json()
    
    return json.dumps(obj, 
                      ensure_ascii=False, 
                      cls=CustomJSONEncoder).encode('utf8')

GLOBAL_HIDDEN_ID = 'NoclientIfYouMessWithThisYoullSeriouslyBreakThings'

def make_key(key):
    return GLOBAL_HIDDEN_ID + ':' + key

def make_hidden_global(key, value):
    setattr(g, make_key(key), value)
    
def get_hidden_global(key):
    return getattr(g, make_key(key))

def make_hidden_session(key, value):
    session[make_key(key)] = value
    
def get_hidden_session(key):
    return session.get(make_key(key))

def hidden_key(key):
    return message_queue.PREFIX + key

def user_id():
    return get_hidden_session('user_id')

def generate_tracker_key(handler_type):
    return hidden_key(user_id() + ':' + str(handler_type))

'''def send_to_all_of_type(type, value):
    key = generate_tracker_key(type)
    event_queue_keys = redis_queue.db().lrange(key, 0, -1)
    
    for key in event_queue_keys:
        redis_queue.db().rpush(key, request.data)'''
