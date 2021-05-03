from ControlThorlabsMotors import open_serial, move_topos
import local_settings as settings


class Waveplate:
    '''
    Class of Rotation Mount with Waveplate which is connected via
    bus and Thorlabs hardware module
    '''
    def __init__(self, address, offset):
        '''
        Initializes the motors

        Parameters
        ----------
        address :   Integer value referring to the bus address
        offset  :   Float value referring to offset of waveplate in
                    absolute degrees
        '''
        self.address = address
        self.offset = offset

    def rotate(self, angle):
        '''
        Rotates the Rotation Mount

        Parameters
        ---------
        angle : Float value specifying the target position of the Rotation Mount
                in absolute degrees
        '''
        bus = open_serial(settings.com)
        move_topos(bus, self.address, angle + self.offset)
        bus.close()
