from airypi.remote_obj import RemoteObj, RemoteDescriptor

class SMBus(RemoteObj):
    module_name = 'smbus'
    
    pec = RemoteDescriptor('pec')
    
    def __init__(self, bus=-1):
        RemoteObj.__init__(self)
        
    def __del__(self):pass
    
    def close(self):pass
    def dealloc(self):pass
    def open(self, bus):pass
    def write_quick(self, addr):pass
    def read_byte(self, addr):pass
    def write_byte(self, addr, val):pass
    def read_byte_data(self, addr, cmd):pass
    def write_byte_data(self, addr, cmd, val):pass
    def read_word_data(self, addr, cmd):pass
    def write_word_data(self, addr, cmd, val):pass
    def process_call(self, addr, cmd, val):pass
    def read_block_data(self, addr, cmd):pass
    def write_block_data(self, addr, cmd, vals):pass
    def block_process_call(self, addr, cmd, vals):pass
    def read_i2c_block_data(self, addr, cmd, len=32):pass
    def write_i2c_block_data(self, addr, cmd, vals):pass
