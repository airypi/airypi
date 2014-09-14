from airypi import monkey
monkey.patch_all()

from airypi.device import Device
from airypi.ui import Label, Button, SwitchButton
from airypi.server import setup


@Device.register_for(Device.RPI)
class RPiHandler():
    def __init__(self):
        self.label = Label('Hey')
        self.button = Button("Hello")
        self.switch = SwitchButton('very long text')
    
    def loop(self):
        pass
    
    def ui_event(self, ui_element):        
        if ui_element is self.button:
            self.label.text = "switch turned off"
            self.switch.activated = False
            self.switch.text = "you should probably turn me on"
        elif ui_element is self.switch:
            if ui_element.activated:
                self.label.text = "switch turned on"
                self.button.text = "push me to turn the switch off"
    
    def ui_elements(self):
        return [self.label, self.button, self.switch]

if __name__ == "__main__":
    setup(host = '0.0.0.0',
          port = 80,
          client_id = 'MjxW6U5HjKmdyzEQmwDDRk2LK9gGfWZBKoAQEC2P',
          client_secret = 'QATkoYLopBmUkJDjgL3AiqU9RqkVoDxWgK23BSVeDYdurA5kki',)