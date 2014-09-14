class CallbackDict:
    def __init__(self):
        self.callbacks = {}
    
    def set_callback(self, key, callback):
        self.callbacks[key] = callback
    
    def do_callback(self, key, *args, **kwargs):
        self.callbacks[key](*args, **kwargs)
        
    def append_callback(self, key, callback):
        if key in self.callbacks:
            old_callback = self.callbacks[key]
            
            def appended(channel):
                old_callback(channel)
                callback(channel)
            
            self.callbacks[key] = appended
        else:
            self.callbacks[key] = callback