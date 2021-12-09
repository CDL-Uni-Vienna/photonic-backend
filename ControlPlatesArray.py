from ThorLabsMotors.RotationMount import get_position, get_status, move_abs, move_abs_n_hear, open_serial, get_info
from Settings.measurement_settings import setupDic
from utilFunc import flatten
import numpy as np
import Settings.com_settings as com_settings
import time


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
        self.devices_known_type = []
        self.devices_known_path = []
        self.devices_known_order = []

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
                    self.devices_known_type.append(element['Type'])
                    self.devices_known_path.append(element['Path'])
                    self.devices_known_order.append(element['Order'])

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

        self.devices_known_ll = [self.devices_known_path, self.devices_known_order,
                                 self.devices_known_ports, self.devices_known_address]
        self.devices_known_array = np.array(self.devices_known_ll)
        self.devices_known_array = self.devices_known_array.T
        self.devices_known_ll = self.devices_known_array.tolist()

        for path in range(5):

            temp_device_list = []

            for device in self.devices_known_ll:

                if str(path) == device[0]:
                    temp_device_list.append(device[1:])

            temp_device_list = sorted(temp_device_list, key=lambda dd: dd[0])

            self.devicesDic[path] = temp_device_list

        # print(self.devicesDic)

        return [self.devices_known, self.devices_unkno]

    def init(self):
        '''
        Initialize serial ports
        '''
        for device_port in self.ports_nonDup:
            bus = open_serial(device_port,  timeout=10)
            self.portsToBusDic[device_port] = bus
        # let's home here

    def fina(self):
        '''
        Close serial ports
        '''
        for device_port in self.ports_nonDup:
            bus = self.portsToBusDic[device_port]
            bus.close()

    def setAngles(self, angles_list):
        '''
        Set plates in a particular set of angles specified by angles_list (ordered)
        '''
        for num, angle in enumerate(angles_list):
            move_abs_n_hear(
                self.portsToBusDic[self.devices_known_ports[num]], self.devices_known_address[num], angle, 0)
            time.sleep(0.1)

    def setPath(self, path_id, angles_list):
        '''
        Set path's plates in a particular set of angles specified by angles_list (ordered)
        '''

        msg = 'PlatesArray.setPath :: '

        if len(angles_list) == len(self.devicesDic[path_id]):

            print(
                msg + 'setting path: '+str(path_id))

            for num, device in enumerate(self.devicesDic[path_id]):

                move_abs_n_hear(
                    self.portsToBusDic[device[1]], device[2], angles_list[num], 0)
                time.sleep(0.1)

        else:
            print(
                msg + 'angles_list do not match the Path number of elements (ERROR)')
