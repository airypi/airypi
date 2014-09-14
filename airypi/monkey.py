def patch_all():
    from gevent import monkey
    monkey.patch_all()
    
    import device.gpio
    import device.serial
    import device.smbus
    import device.spidev
    
    import sys
    
    sys.modules['RPi'] = device.gpio
    sys.modules['RPi.GPIO'] = device.gpio.GPIO
    sys.modules['serial'] = device.serial.PySerial
    sys.modules['smbus'] = device.smbus
    sys.modules['spidev'] = device.spidev