from ThorLabsMotors.RotationMount import move_abs, open_serial, get_info
from Settings.measurement_settings import setupDic
import Settings.com_settings as com_settings

devices_known = []

devices_unkno = []

for comPort in com_settings.com_list:

    bus = open_serial(comPort,  timeout=0.1)

    for motorAddress in com_settings.address_list:

        device_sn = get_info(bus, motorAddress)

        element = setupDic.get(device_sn)
        
        if element is None:
            devices_unkno.append(device_sn)
        else:
            devices_known.append(device_sn)

    bus.close()

try:
    while True:
        devices_unkno.remove(b'')
except ValueError:
    pass

print(devices_unkno)
print(devices_known)

devices_known

