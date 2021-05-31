import ThorLabsMotors.RotationMount as ctrl
import Settings.com_settings as settings
import time
import ControlPowermeter


# print(ctrl.to8_format('0x343'))
# print(ctrl.angle_tohexa(90.45))
# print(ctrl.angle_tohexa(45.088))
# print(ctrl.hexa_toangle(ctrl.angle_tohexa(45.088)))
# print(ctrl.to8_format(ctrl.angle_tohexa(45.088)))

pm = ControlPowermeter.open_powermeter('1909736')
bus = ctrl.open_serial(settings.com1)
angles = []
power = []
for i in range(180):
    angle = i
    print(angle)
    angles.append(angle)
    ctrl.move_abs(bus, 0, angle)
    time.sleep(1)
    p = ControlPowermeter.measure_row(pm, 1)
    print(p)
    power.append(p)
    time.sleep(1)
# print(ctrl.get_position(bus, 0))
# print(ctrl.get_position(bus, 0))
# # print(ctrl.get_position(bus, 1))
# # print('----')
# # print(ctrl.angle_tohexa(23))
# # print(ctrl.hexa_toangle('0X23C7'))
# # print('----')
# # print(ctrl.to8_format('0X23C7'))
# # print(ctrl.to8_format(ctrl.angle_tohexa(23)))
# # print('----')
print(angles)
print(power)
ControlPowermeter.close_powermeter(pm)
bus.close()
