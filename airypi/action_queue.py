from airypi.remote_obj import send_to_device

def multi():
    send_to_device({'type': 'transaction',
                    'func': 'begin'})

def execute():
    send_to_device({'type': 'transaction',
                    'func': 'execute'})

def sleep(duration):
    send_to_device({'type': 'transaction',
                    'func': 'sleep', 
                    'args': {'duration': duration}})