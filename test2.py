import ControlThorlabsMotors as ctrl
import local_settings as settings


#print(ctrl.to8_format('0x343'))
# print(ctrl.angle_tohexa(90.45))
# print(ctrl.angle_tohexa(45.088))
# print(ctrl.hexa_toangle(ctrl.angle_tohexa(45.088)))
# print(ctrl.to8_format(ctrl.angle_tohexa(45.088)))


bus = ctrl.open_serial(settings.com)
# ctrl.set_offset(bus, 0, 180)
# # bus.close()

# # bus = ctrl.open_serial(settings.com)
# # print(ctrl.get_offset(bus, 0))
# # bus.close()
# ctrl.move_abs(bus, 0, 45)
# print(ctrl.get_position(bus, 0))
# # print(ctrl.get_position(bus, 0))
# # print(ctrl.get_position(bus, 1))
# # print('----')
# # print(ctrl.angle_tohexa(23))
# # print(ctrl.hexa_toangle('0X23C7'))
# # print('----')
# # print(ctrl.to8_format('0X23C7'))
# # print(ctrl.to8_format(ctrl.angle_tohexa(23)))
# # print('----')
bus.close()
