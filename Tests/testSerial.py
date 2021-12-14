from ThorLabsMotors.RotationMount import move_abs, open_serial, get_info, write_to_device
import Settings.com_settings as com_settings
from time import sleep

bus = open_serial('COM4',  timeout=0.1)

print(0)
write_to_device(bus, 0, '0in')
print(3)
line = bus.readline()

print(line)

#get_info(bus, '1')

bus.close()