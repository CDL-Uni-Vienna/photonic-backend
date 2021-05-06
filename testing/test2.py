from . import ControlThorlabsMotors as ctrl
from . import local_settings as settings


#print(ctrl.to8_format('0x343'))
# print(ctrl.angle_tohexa(90.45))



bus = ctrl.open_serial(settings.com)
print(ctrl.get_position(bus, 0))
print(ctrl.get_position(bus, 1))
print('----')
print(ctrl.angle_tohexa(23))
print(ctrl.hexa_toangle('0X23C7'))
print('----')
print(ctrl.to8_format('0X23C7'))
print(ctrl.to8_format(ctrl.angle_tohexa(23)))
print('----')
bus.close()
