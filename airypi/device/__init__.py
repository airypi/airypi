from airypi.remote_obj import RemoteObj
from flask import session, request
from airypi import utils

import json
import gpio
from airypi.callback_dict import CallbackDict
from airypi import event_loop
        
class Device:
    RPI = 'RASPBERRY_PI'
    ANDROID = 'ANDROID'
    handler_for_type = {}
    
    event_loop_for_type = {'RASPBERRY_PI': event_loop.RPiEventLoop, 'ANDROID': event_loop.AndroidEventLoop}
    
    @staticmethod
    def id():
        return utils.get_hidden_session('device')['id']
        
    '''@staticmethod
    def register_for(device_type):
        def real_register_for(cls):
            def wrapper(*args):
                print device_type
                Device.handler_for_type[device_type] = cls
        
                for method in cls.__dict__.iteritems():
                    if hasattr(method, "device_event"):
                        event_loop_class = Device.event_loop_for_type[device_type]
                        event_loop_class.callback_dict[method.event_name] = method
            return wrapper
        return real_register_for'''
    
    class register_for(object):
        def __init__(self, device_type):
            self.device_type = device_type
        def __call__(self, cls):
            Device.handler_for_type[self.device_type] = cls
        
            for method in cls.__dict__.iteritems():
                if hasattr(method, "device_event"):
                    event_loop_class = Device.event_loop_for_type[self.device_type]
                    event_loop_class.callback_dict[method.event_name] = method
            return cls
    
    @staticmethod
    def event(event_name, func):
        func.event_name = event_name
    