from airypi.remote_obj import RemoteObj, RemoteDescriptor

class SpiDev(RemoteObj):
    module_name = 'spidev'
    
    bits_per_word = RemoteDescriptor('bits_per_word')
    cshigh = RemoteDescriptor('cshigh')
    loop = RemoteDescriptor('loop')
    lsbfirst = RemoteDescriptor('lsbfirst')
    max_speed_hz = RemoteDescriptor('max_speed_hz')
    mode = RemoteDescriptor('mode')
    threewire = RemoteDescriptor('threewire')

    def __init__(self):
        RemoteObj.__init__(self)
    
    def __del__(self):pass
    
    def open(self, bus, device):pass
    def close(self):pass
    def dealloc(self):pass
    def readbytes(self, len):pass
    def writebytes(self, values):pass
    def xfer(self, values):pass
    def xfer2(self, values):pass
    