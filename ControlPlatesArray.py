from ThorLabsMotors.RotationMount import home, move_abs_n_hear, open_serial, get_info
from Settings.measurement_settings import setupDic
from utilFunc import flatten
import numpy as np
import Settings.com_settings as com_settings
import time
import json
import os.path


class PlatesArray:
    '''
    Class for high level operations on an array of waveplates
    '''

    def __init__(self, pathID):
        '''
        Initializes the PlatesArray class

        Parameters
        ----------
        pathID :            ID used to identify optical path segments
        devices_known:      List of known devices i.e. those present in the setup dictionary (setupDic)
        devices_unkno:      List of unknown devices i.e. those present in the setup dictionary (setupDic)
        '''
        self.pathID = pathID

        self.devices_known = []
        self.devices_known_ports = []
        self.devices_known_address = []

        self.devices_known_path = []
        self.devices_known_order = []
        self.devices_known_type = []
        self.devices_known_calAng = []

        self.devicesDic = dict()

        self.ports_nonDup = []

        self.portsToBusDic = {}

        self.devices_unkno = []
        self.census()

    def census(self):
        '''
        Performs a census of all connected motors. Scans serial ports and addresses
        '''
        print('PlatesArray.census :: Scanning ports ' +
              str(com_settings.com_list)+' looking for devices')

        for comPort in com_settings.com_list:

            bus = open_serial(comPort,  timeout=0.3)

            for motorAddress in com_settings.address_list:

                device_sn = get_info(bus, motorAddress)

                element = setupDic.get(device_sn)

                if element is None:
                    if device_sn != b'':
                        print('PlatesArray.census :: Device ' + str(device_sn) +
                              ' found at port ' + comPort + ' address ' + motorAddress + ' (Unknown)')
                    self.devices_unkno.append(device_sn)
                else:
                    print('PlatesArray.census :: Device ' + str(device_sn) +
                          ' found at port ' + comPort + ' address ' + motorAddress + ' (Known)')
                    self.devices_known.append(device_sn)
                    self.devices_known_ports.append(comPort)
                    self.devices_known_address.append(motorAddress)

                    self.devices_known_path.append(element['Path'])
                    self.devices_known_order.append(element['Order'])
                    self.devices_known_type.append(element['Type'])
                    self.devices_known_calAng.append(
                        element['CalibrationAngle'])

        bus.close()

        try:
            while True:
                self.devices_unkno.remove(b'')
        except ValueError:
            pass

        self.ports_nonDup = list(dict.fromkeys(self.devices_known_ports))

        print('PlatesArray.census :: ' + str(len(self.devices_known)) +
              ' known devices found ' + str(self.devices_known))
        print('PlatesArray.census :: ' + str(len(self.devices_unkno)) +
              ' unknown devices found ' + str(self.devices_unkno))

        # DO NOT alter the order of this lits
        self.devices_known_ll = [self.devices_known_path, self.devices_known_order,
                                 self.devices_known_ports, self.devices_known_address, self.devices_known_calAng]
        self.devices_known_array = np.array(self.devices_known_ll)
        self.devices_known_array = self.devices_known_array.T
        self.devices_known_ll = self.devices_known_array.tolist()

        self.nondup_paths = list(dict.fromkeys(self.devices_known_path))
        self.devices = []

        for path in self.nondup_paths:

            temp_device_list = []

            i = 0
            for device in self.devices_known_ll:

                if str(path) == device[0]:

                    self.devices.append([path, i])
                    i = i + 1

                    temp_device_list.append(device[1:])

            temp_device_list = sorted(temp_device_list, key=lambda dd: dd[0])

            self.devicesDic[path] = temp_device_list
        # print(self.devicesDic)
        with open("Settings/devicesDicIn.json", "w") as dic_file:
            json.dump(self.devicesDic, dic_file)

        # print(self.devicesDic)
        # print(self.devices)
        # print(len(self.devices))
        # print(9999)
        # print(self.portsToBusDic)

        self.calibration_update_active = False

        return [self.devices_known, self.devices_unkno]

    def calibration_update(self):

        msg = 'PlatesArray.calibration_update :: '

        cal_file = "Settings/devicesDicTemp.json"

        if os.path.isfile(cal_file):
            print(msg + "Updating devicesDic from " + cal_file)
            with open(cal_file, "r") as dic_file:
                self.devicesDic = json.load(dic_file)

                tempDic = {}

                for key, value in self.devicesDic.items():
                    tempDic[int(key)] = value

                self.devicesDic = tempDic

    def calibration_save(self, path: int, order: int, correction: float):

        msg = 'PlatesArray.calibration_save :: '

        cal_file = "Settings/devicesDicTemp.json"

        self.calibration_update_active = True

        new_device_item = self.devicesDic[path]

        old_zero = new_device_item[order][3]
        new_zero = float(old_zero) + correction

        new_device_item[order][3] = new_zero
        # It's 3 because is the index where the calibration angle is located

        self.devicesDic[path] = new_device_item

        print(msg + "Saving devicesDic at " + cal_file)
        with open(cal_file, "w") as dic_file:
            json.dump(self.devicesDic, dic_file)

    def init(self):
        '''
        Initialize serial ports
        '''

        msg = 'PlatesArray.init :: '

        for device_port in self.ports_nonDup:
            bus = open_serial(device_port,  timeout=10)
            self.portsToBusDic[device_port] = bus
        # let's home here
        for key, values in self.devicesDic.items():
            # print(values)
            print(msg + 'Homing path ' + str(key))
            for device in values:
                home(self.portsToBusDic[device[1]], device[2])

    def fina(self):
        '''
        Close serial ports
        '''

        msg = 'PlatesArray.fina :: '

        for device_port in self.ports_nonDup:
            print(msg + 'Closing ' + device_port + ' port')
            bus = self.portsToBusDic[device_port]
            bus.close()

    # Deprecated
    # def setAngles(self, angles_list):
    #     '''
    #     Set plates in a particular set of angles specified by angles_list (ordered)
    #     '''
    #     for num, angle in enumerate(angles_list):
    #         move_abs_n_hear(
    #             self.portsToBusDic[self.devices_known_ports[num]], self.devices_known_address[num], angle, 0)
    #         time.sleep(0.1)

    def setPath(self, path_id, angles_list):
        '''
        Set path's plates in a particular set of angles specified by angles_list (ordered)
        '''

        msg = 'PlatesArray.setPath :: '

        # if self.calibration_update_active:
        #     self.calibration_update()

        if len(angles_list) == len(self.devicesDic[path_id]):

            print(
                msg + 'Setting path: '+str(path_id))

            for num, device in enumerate(self.devicesDic[path_id]):
                # home(self.portsToBusDic[device[1]], device[2])
                move_abs_n_hear(
                    self.portsToBusDic[device[1]], device[2], float(device[3]) + angles_list[num], 0)
                time.sleep(0.1)

        else:
            print(
                msg + 'angles_list do not match the Path number of elements (ERROR)')

    def setPlate(self, path_id: int, order: int, angle: float):
        '''
        Set a plates in a particular angle
        '''

        msg = 'PlatesArray.setPlate :: '

        # if self.calibration_update_active:
        #     self.calibration_update()

        # + str(self.devicesDic[path_id][order]))
        print(msg + 'Setting ' +
              str([path_id, order]) + ' plate at ' + str(angle) + '°')

        # print(self.devicesDic)
        device = self.devicesDic[path_id][order]

        # home(self.portsToBusDic[device[1]], device[2])
        calAng = float(device[3])
        angle_out = move_abs_n_hear(
            self.portsToBusDic[device[1]], device[2], calAng + angle, 0)
        # self.portsToBusDic[device[1]], device[2], angle, 0)
        time.sleep(0.1)

        angle_out = float(angle_out) - calAng

        return angle_out
