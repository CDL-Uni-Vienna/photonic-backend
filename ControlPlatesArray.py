from ThorLabsMotors.RotationMount import move_abs, open_serial, get_info
from Settings.measurement_settings import setupDic
import Settings.com_settings as com_settings

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
        self.devices_known_bus = []

        self.devices_unkno = []
        self.census()

    def census(self):
        '''
        Performs a census of all connected motors. Scans serial ports and addresses
        '''
        for comPort in com_settings.com_list:

            bus = open_serial(comPort,  timeout=0.1)

            for motorAddress in com_settings.address_list:

                device_sn = get_info(bus, motorAddress)

                element = setupDic.get(device_sn)
                
                if element is None:
                    self.devices_unkno.append(device_sn)
                else:
                    self.devices_known.append(device_sn)
                    self.devices_known_ports.append(comPort)
                    self.devices_known_address.append(motorAddress)

        bus.close()

        try:
            while True:
                self.devices_unkno.remove(b'')
        except ValueError:
            pass

        return [self.devices_known, self.devices_known]

    def init(self):
        '''
        Initialize serial ports
        '''
        for device_port in self.devices_known_ports:
            bus = open_serial(device_port)
            self.devices_known_bus.append(bus)

    def fina(self):
        '''
        Close serial ports
        '''
        for device_port in self.devices_known_bus:
            device_port.close()

    def setAngles(self, angles_list):
        '''
        Set plates in a particular set of angles specified by angles_list (ordered)
        '''
        for num, angle in enumerate(angles_list):
            move_abs(self.devices_known_bus[num], self.devices_known_bus[num], angle ) # TODO: add offset from setupDic #