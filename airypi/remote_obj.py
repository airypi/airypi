from flask import request
from flask_socketio import emit
from utils import json_unicode, hidden_key
import gevent
import redis_queue
import device
from flask import current_app

import uuid
import json
import array

import inspect

from functools import wraps

def return_val_key():
    return hidden_key("return:" + device.Device.id())

def json_unpack(value):
    if isinstance(value, dict):
        if value['type'] == 'bytearray':
            return bytearray(value['data'])
    return value

def json_pack(data):
    if data.__class__ == bytearray:
        return {'type':'bytes', 'data': str(data)}
    return data

def send_to_device(type, params):
    emit(type, params)
    
    msg = None
    mq = current_app.config['NOCLIENT_MQ'](key = return_val_key())
    
    while msg is None:
        msg = mq.pop()
        gevent.sleep(0)
    
    msg = json.loads(msg)
    if 'error' in msg:
        print msg['error']
        print "The above error occurred on the raspberry pi client"
        print "The below error is the server error"
        import airypi.errors
        raise airypi.errors.ExitError()
    
    result = msg['result']
    
    return json_unpack(result)

from functools import wraps

def send(cls, data, object = None, proc_before = None):
    data['module'] = cls.module_name
    
    #make sure the class isn't actually a wrapper for a class
    if not hasattr(cls, 'module_wrapper_class'):
        data['class'] = cls.__name__
    
    if object is not None:
        data['object'] = object.obj_id
    
    if proc_before is not None:
        data = proc_before(data)
    
    return send_to_device('io', data)

#args and kwargs are tuple and dict
def prep_args(cls, func, *args, **kwargs):
    args = [json_pack(arg) for arg in args]
    for key in kwargs:
        if kwargs[key] is None:
            del kwargs[key]
        else:
            kwargs[key] = json_pack(kwargs[key])

    data = {'func': func.__name__,
            'args': args,
            'kwargs': kwargs}
        
    return data

def func_exec(cls, func, args, kwargs, object = None):
    proc_funcs = None
    
    if object is None:
        proc_funcs = func(*args, **kwargs)
    else:
        proc_funcs = func(object, *args, **kwargs)
    data = prep_args(cls, func, *args, **kwargs)
    
    if proc_funcs is not None:
        proc_before, proc_after = proc_funcs
        
        if proc_after is not None:
            return proc_after(send(cls, data, object, proc_before))
        return send(cls, data, object, proc_before)
    return send(cls, data, object)

def object_wrapper(func):
    @wraps(func)
    def decorator(self, *args, **kwargs):
        return func_exec(self.__class__, func, args, kwargs, object = self)
    return decorator

def class_wrapper(func):
    @wraps(func)
    def decorator(cls, *args, **kwargs):
        return func_exec(cls, func, args, kwargs)
    return classmethod(decorator)

class ApiWrapper(type):
    def __new__(cls, name, bases, local):        
        for attr in local:
            value = local[attr]
            if callable(value) and not isinstance(value,type):
                #don't wrap RemoteObj
                if name != "RemoteObj":
                    local[attr] = object_wrapper(value)
            if isinstance(value, classmethod):
                local[attr] = class_wrapper(value.__get__(None, cls))
        return type.__new__(cls, name, bases, local)
    
class RemoteConstant(object):
    def __init__(self, name):
        self.name = name
        
    def __get__(self, instance, owner=None):
        data = {'property': self.name}
        
        if isinstance(instance, type):
            return send(instance, data)
        else:
            return send(owner, data, instance)
        
    def __set__(self, instance, value):
        raise TypeError("cannot assign value to constant " + self.name)
    
class RemoteDescriptor(RemoteConstant):
    def __set__(self, instance, value):
        value = json_pack(value)
        
        data = {'setter': self.name, 'value': value}
        
        if isinstance(instance, type):
            send(instance, data)
        else:
            send(instance.__class__, data, instance)

class RemoteObj():
    __metaclass__ = ApiWrapper
    
    def __init__(self):
        self.obj_id = uuid.uuid4()
        
    
        
    