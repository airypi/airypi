import airypi.monkey
airypi.monkey.patch_all()

from airypi.device import Device
from airypi.ui import Label, Button, SwitchButton
from airypi.server import setup

import RPi.GPIO as GPIO
import serial, smbus, spidev

@Device.register_for(Device.RPI)
class RPiHandler():
    def __init__(self):
        self.label = Label('Hey')
        self.button = Button("Hello")
        self.switch = SwitchButton('very long text')
        
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(12, GPIO.IN, initial=GPIO.HIGH)
        GPIO.setup(13, GPIO.IN)
        GPIO.add_event_detect(12, GPIO.RISING)
        def back(channel):
            print "hey from channel: " + str(channel)
        GPIO.add_event_callback(12, back)
        
        bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    def ui_elements(self):
        return [self.label, self.button, self.switch]

if __name__ == "__main__":
    setup(host = '0.0.0.0',
          port = 80,
          client_id = 'MjxW6U5HjKmdyzEQmwDDRk2LK9gGfWZBKoAQEC2P',
          client_secret = 'QATkoYLopBmUkJDjgL3AiqU9RqkVoDxWgK23BSVeDYdurA5kki',)