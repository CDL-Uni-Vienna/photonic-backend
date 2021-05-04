import ControlThorlabsMotors as ctrl
import local_settings as settings


#print(ctrl.to8_format('0x343'))
# print(ctrl.angle_tohexa(90.45))



bus = ctrl.open_serial(settings.com)
#ctrl.move_rel(bus, 1, 40)
print(ctrl.read_pos(bus, 1))
ctrl.move_abs(bus, 1, 50)
print(ctrl.read_pos(bus, 1))
ctrl.move_abs(bus, 1, 90)
print(ctrl.read_pos(bus, 1))
bus.close()
