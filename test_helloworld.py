from airypi import monkey
monkey.patch_all()

from airypi.device import Device
from airypi.ui import Label, Button
from airypi.server import setup

@Device.register_for(Device.RPI)
class RPiHandler():
    def __init__(self):
        self.button = Button("Print Hello World!")
        
    def ui_elements(self):
        return [self.button]
    
    def ui_event(self, element):
        if element is self.button:
            print "Hello World"

if __name__ == "__main__":
    setup(host = '0.0.0.0',
          port = 80,
          client_id = 'MjxW6U5HjKmdyzEQmwDDRk2LK9gGfWZBKoAQEC2P',
          client_secret = 'QATkoYLopBmUkJDjgL3AiqU9RqkVoDxWgK23BSVeDYdurA5kki')