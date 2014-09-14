from airypi.remote_obj import ApiWrapper, RemoteObj, RemoteConstant

from airypi import utils
import json

def register_handler(handler):
    utils.make_hidden_global('gpio_event_handler', handler)

def handler():
    return utils.get_hidden_global('gpio_event_handler')    

class MetaGPIO(ApiWrapper):
    VERSION = RemoteConstant('VERSION')
    RPI_REVISION = RemoteConstant('RPI_REVISION')
    
    HIGH = RemoteConstant('HIGH')
    LOW = RemoteConstant('LOW')
    
    RISING = RemoteConstant('RISING')
    FALLING = RemoteConstant('FALLING')
    BOTH = RemoteConstant('BOTH')
    
    EVENT_ID = RemoteConstant('EVENT_ID')
    
    BOARD = RemoteConstant('BOARD')
    BCM = RemoteConstant('BCM')
    
    IN = RemoteConstant('IN')
    OUT = RemoteConstant('OUT')
    
    PUD_UP = RemoteConstant('PUD_UP')
    PUD_DOWN = RemoteConstant('PUD_DOWN')
    
    INPUT = RemoteConstant('INPUT')
    OUTPUT = RemoteConstant('OUTPUT')
    SPI = RemoteConstant('SPI')
    I2C = RemoteConstant('I2C')
    HARD_PWM = RemoteConstant('HARD_PWM')
    SERIAL = RemoteConstant('SERIAL')
    UNKNOWN = RemoteConstant('UNKNOWN')

class GPIO(RemoteObj):
    __metaclass__ = MetaGPIO
    module_name = 'RPi.GPIO'
    module_wrapper_class = True
    
    #setup
    @classmethod
    def setmode(cls, mode): pass
    
    @classmethod
    def setwarnings(cls, warning): pass
    
    @classmethod
    def setup(cls, channel, mode, initial = None, pull_up_down = None): pass
        
    #input
    @classmethod
    def input(cls, channel): pass
    
    @classmethod
    def wait_for_edge(cls, channel, edge_type): pass
        
    @classmethod
    def event_detected(cls, channel): pass
    
    @classmethod
    def add_event_detect(cls, channel, edge_type, callback = None, bouncetime = None):
        key = json.dumps({'type':'gpio_callback', 'channel': channel})
        
        if callback is not None:
            handler().set_callback(key, callback)
            
        def proc_before(data):
            if 'callback' in data['kwargs']:
                del data['kwargs']['callback']
            data['extra'] = key
            return data
        return proc_before, None
        
    @classmethod
    def add_event_callback(cls, channel, callback, bouncetime = None):
        key = json.dumps({'type':'gpio_callback', 'channel': channel})
        handler().append_callback(key, callback)
        def proc_before(data):
            print data['args']
            data['args'] = [data['args'][0]]
            if 'callback' in data['kwargs']:
                del data['kwargs']['callback']
            data['extra'] = key
            return data
        
        return proc_before, None
    
    @classmethod
    def remove_event_detect(cls):
        def proc_after(result):
            return result
        return None, proc_after
        
    #output
    @classmethod
    def output(cls, channel, mode): pass
        
    @classmethod
    def cleanup(cls): pass
        
    #PWM
    @classmethod
    def PWM(cls, channel, frequency): pass
                
    @classmethod
    def start(cls, dc): pass
    
    @classmethod
    def ChangeFrequency(cls, freq): pass
        
    @classmethod
    def ChangeDutyCycle(cls, dc): pass
        
    @classmethod
    def stop(cls): pass
    
    #specially handle this    
    @classmethod
    def gpio_function(cls): pass
        