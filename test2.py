import ControlThorlabsMotors as ctrl
import local_settings as settings


# print(ctrl.to8_format('0x343'))
# print(ctrl.angle_tohexa(90.45))


bus = ctrl.open_serial(settings.com)
ctrl.move_abs(bus, 0, 389)
#ctrl.move_bw(bus, 0, 9)
print(ctrl.read_pos(bus, 0))
bus.close()
