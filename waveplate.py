from ControlThorlabsMotors import open_serial, move_abs
import local_settings as settings


class Waveplate:
    '''
    Class for high level operations on the waveplate which is mounted in the
    respective Thorlabs motor
    '''
    def __init__(self, address):
        '''
        Initializes the motors

        Parameters
        ----------
        address :   Integer value referring to the bus address
        offset  :   Float value referring to offset of waveplate in
                    absolute degrees
        '''
        self.address = address
        self.offset = settings.offset[address]

    def rotate(self, angle):
        '''
        Rotates the Rotation Mount

        Parameters
        ---------
        angle : Float value specifying the target position of the Rotation Mount
                in absolute degrees
        '''
        bus = open_serial(settings.com)
        move_abs(bus, self.address, angle + self.offset)
        bus.close()
