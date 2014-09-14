import device
from airypi import utils
import gevent
import json
from airypi import redis_queue
import traceback
from airypi import server

from flask import request, current_app
from airypi import callback_dict
from airypi import remote_obj
from flask_socketio import emit, disconnect

class Handler:
    def __init__(self):
        pass
    
    def loop(self):
        pass
    
    def ui_event(self, element):
        pass
    
    def ui_elements(self):
        return []

class EventLoop(object):
    def __init__(self, device_type):
        self.mq = current_app.config['NOCLIENT_MQ']()
        self.mq.clear()

        print "event loop queue key:" + str(self.mq.queue_key)
        
        self.handler = device.Device.handler_for_type[device_type]()

    def handle_event(self, event):
        pass
    
    def loop(self):        
        msg = self.mq.pop()
        
        if msg is not None:
            print msg
            msg = json.loads(msg)
            self.handle_event(msg)
        
        if hasattr(self.handler, 'loop'):
            self.handler.loop()

class RPiEventLoop(EventLoop):
    @staticmethod
    def revision():
        return super._class_send({'func': 'revision',
                                  'params': {}})
        
    def __init__(self):
        device.gpio.register_handler(callback_dict.CallbackDict())
        current_app.config['NOCLIENT_MQ'](remote_obj.return_val_key()).clear()
        EventLoop.__init__(self, device.Device.RPI)        

    def handle_event(self, event):
        print 'handling event:' + str(event)
        event_type = event['type']
        
        if event_type == 'gpio_callback':
            key = event['key']
            callback_data = json.loads(key)
            device.gpio.handler().do_callback(key, callback_data['channel'])
        elif event_type == 'device':
            RPiEventLoop.callback_dict.do_callback(event.name)
        elif event_type == 'ui_load':
            message = None
            if hasattr(self.handler, 'ui_elements'):
                message = utils.json_unicode(self.handler.ui_elements())
            else:
                message = '[]'
            emit('ui_load', json.loads(message))
        elif event_type == "ui":
            element_id = event['element_id']
            print 'element id:' + element_id
            
            if not hasattr(self.handler, 'ui_elements'):
                return

            for element in self.handler.ui_elements():
                print element.id
            
            element = [element for element in self.handler.ui_elements() if element.id == element_id][0]
            
            if 'update' in event:
                updates = event['update']
                for key in updates:
                    if hasattr(element, key):
                        setattr(element, key, updates[key])
            
            if hasattr(self.handler, 'ui_event'):
                self.handler.ui_event(element)
            #send_to_device({'type':'ui_load', 
            #                'data': self.handler.ui_elements()})
    
        
class AndroidEventLoop(EventLoop):
    def __init__(self):
        super.__init__('user')
    
    def handle_event(self, event):
        ws = request.environ["wsgi.websocket"]
        ws.send(json.dumps(event, 'utf-8'))

        
    