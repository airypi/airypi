from airypi.remote_obj import RemoteObj, RemoteConstant, RemoteDescriptor, ApiWrapper

class MetaPySerial(ApiWrapper):
    PARITY_NONE = RemoteConstant('PARITY_NONE')
    PARITY_EVEN = RemoteConstant('PARITY_EVEN')
    PARITY_ODD = RemoteConstant('PARITY_ODD')
    PARITY_MARK = RemoteConstant('PARITY_MARK')
    PARITY_SPACE = RemoteConstant('PARITY_SPACE')
    
    STOPBITS_ONE = RemoteConstant('STOPBITS_ONE')
    STOPBITS_ONE_POINT_FIVE = RemoteConstant('STOPBITS_ONE_POINT_FIVE')
    STOPBITS_TWO = RemoteConstant('STOPBITS_TWO')
    
    FIVEBITS = RemoteConstant('FIVEBITS')
    SIXBITS = RemoteConstant('SIXBITS')
    EIGHTBITS = RemoteConstant('EIGHTBITS')
    EIGHTBITS = RemoteConstant('EIGHTBITS')
    
    XON = RemoteConstant('XON')
    XOFF = RemoteConstant('XOFF')
    
    VERSION = RemoteConstant('VERSION')

class _PySerial(RemoteObj):
    __metaclass__ = MetaPySerial
    
    module_name = 'serial'
    module_wrapper_class = True

class Serial(RemoteObj):
    module_name = 'serial'
    
    name = RemoteConstant('name')
    port = RemoteDescriptor('port')
    baudrate = RemoteDescriptor('baudrate')
    bytesize = RemoteDescriptor('bytesize')
    parity = RemoteDescriptor('parity')
    stopbits = RemoteDescriptor('stopbits')
    timeout = RemoteDescriptor('timeout')
    writeTimeout = RemoteDescriptor('writeTimeout')
    xonxoff = RemoteDescriptor('xonxoff')
    rtscts = RemoteDescriptor('rtscts')
    dsrdtr = RemoteDescriptor('dsrdtr')
    interCharTimeout = RemoteDescriptor('interCharTimeout')
    BAUDRATES = RemoteConstant('BAUDRATES')
    BYTESIZES = RemoteConstant('BYTESIZES')
    PARITIES = RemoteConstant('PARITIES')
    STOPBITS = RemoteConstant('STOPBITS')
    
    def __init__(self,
             port=None, 
             baudrate=9600, 
             bytesize=None, 
             parity=None, 
             stopbits=None, 
             timeout=None, 
             xonxoff=False, 
             rtscts=False, 
             writeTimeout=None, 
             dsrdtr=False, 
             interCharTimeout=None):
        if bytesize is None:
            bytesize =_PySerial.EIGHTBITS
        if parity is None:
            parity = _PySerial.PARITY_NONE
        if stopbits is None:
            stopbits = _PySerial.STOPBITS_ONE
        RemoteObj.__init__(self)
        
    def open(self):pass
    def close(self):pass
    
    def __del__(self):
        self.close()
        
    def read(self, size = 1):pass
    def write(self, data):pass
    def inWaiting(self):pass        
    def flush(self):pass    
    def flushInput(self):pass        
    def flushOutput(self):pass       
    def sendBreak(self, duration=0.25):pass 
    def setBreak(self, level=True):pass
    def setRTS(self, level=True):pass
    def setDTR(self, level=True):pass
    def getCTS(self):pass
    def getDSR(self):pass        
    def getRI(self):pass
    def getCD(self):pass
        
    def readable(self):pass
    def writable(self):pass
    def seekable(self):pass
    
    def readinto(self, b):
        def proc_after(result):
            n = result.length
            b[:n] = result
            return n
        return proc_after, None
            
    def getSettingsDict(self):pass
    def applySettingsDict(self, d=True):pass
    def outWaiting(self):pass
    def nonblocking(self):pass
    def fileno(self):pass
    def setXON(self, level=True):pass
    def flowControlOut(self, level=True):pass

class PySerial(_PySerial):
    module_name = 'serial'
    module_wrapper_class = True
    Serial = Serial