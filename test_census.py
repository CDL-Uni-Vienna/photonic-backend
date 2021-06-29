from ThorLabsMotors.RotationMount import move_abs, open_serial, get_info
from Settings.measurement_settings import setupDic
import Settings.com_settings as com_settings

devices_known = []

devices_unkno = []

for comPort in com_settings.com_list:

    bus = open_serial(comPort,  timeout=0.3)

    for motorAddress in com_settings.address_list:

        device_sn = get_info(bus, motorAddress)

        element = setupDic.get[device_sn]
        if element is None:
            devices_unkno.append(element)
            print(''.join(['Warning :: Element ', element, ' is not present in the setup dictionary (setupDic)' ]))
        else:
            devices_known.append(element)

    bus.close()

print(devices_known)

devices_known







# move_abs(bus, 0, 45)



'''
b'0IN0E1140050920201501016800023000\r\n'
b'1IN0E1140050820201501016800023000\r\n'
'''