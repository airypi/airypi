from airypi import monkey
monkey.patch_all()

from airypi.device import Device
from airypi.ui import Label, Button, SwitchButton
from airypi.server import setup


@Device.register_for(Device.RPI)
class RPiHandler():
    pass

if __name__ == "__main__":
    setup(host = '0.0.0.0',
          client_id = 'MjxW6U5HjKmdyzEQmwDDRk2LK9gGfWZBKoAQEC2P',
          client_secret = 'QATkoYLopBmUkJDjgL3AiqU9RqkVoDxWgK23BSVeDYdurA5kki',)