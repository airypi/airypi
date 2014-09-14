import device
import Queue

PREFIX = "noclientdonttouch:"

def queue_key(device_id = None):
    if device_id is None:
        return PREFIX + 'device:' + device.Device.id()
    return PREFIX + 'device:' + device_id

class MessageQueue(object):
    def __init__(self, key = None, device_id = None, max_size = 20):
        if key is not None:
            self.queue_key = key
        else:
            self.queue_key = queue_key(device_id = device_id)

        self.max_size = max_size

    def push(self, data):
        pass

    #really only one process should be handling each queue
    def pop(self):
        pass

    def clear(self):
        pass

class DebugMQ(MessageQueue):
    queue_dict = {}
    
    def __init__(self, *args, **kwargs):
        super(DebugMQ, self).__init__(*args, **kwargs)
        DebugMQ.queue_dict[self.queue_key] = Queue.Queue()
    
    def push(self, data):
        print "pushing: " + str(data)
        DebugMQ.queue_dict[self.queue_key].put(data)
    
    def pop(self):
        queue = DebugMQ.queue_dict[self.queue_key]
        
        if not queue.empty():
            data = DebugMQ.queue_dict[self.queue_key].get(block = False)
            print "popping: " + str(data)
            return data
        return None
    
    def clear(self):
        DebugMQ.queue_dict[self.queue_key] = Queue.Queue()