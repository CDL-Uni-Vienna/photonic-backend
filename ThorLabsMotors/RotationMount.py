"""
Control library for ThorLabs Rotation Mount with Resonant Piezoelectric Motors
based on serial commands and the pySerial module

This library is Copyright © 2020-2021, Juan C Loredo, Felix Zilk
"""

from math import floor
import serial


def open_serial(com_port, timeout = None):
    '''
    Opens serial port

    Parameters
    ----------
    com_port : Target COM port of serial connection as string type

    Returns
    -------
    ser : Serial port object
    '''
    ser = serial.Serial(
            port = com_port,
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = timeout,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False,
            write_timeout = None,
            inter_byte_timeout = None,
            exclusive = True
            )
    return ser

def angle_tohexa(angle_degrees):
    '''
    Transforms float number into hexa format required by Thorlabs motors

    Parameters
    ----------
    angle_degrees : Float number which specifies angle in degrees

    Returns
    -------
    angle_hexa : Hexa string type with length up to 8 bits
    '''
    npulses_total = 143360 # equal to int('23000')
    theta_min = 360/npulses_total
    npulses = int(floor(angle_degrees/theta_min))
    angle_hexa = hex(npulses).upper() # e.g. 0X23C7
    return angle_hexa

def hexa_toangle(hexa_str):
    '''
    Retransforms hexa string into float number

    Parameters
    ----------
    hexa_str : Hexa format as string type

    Returns
    -------
    angle_degree : Number in deegrees as float type
    '''
    print('---')
    print(hexa_str)
    if hexa_str != b'\n':
        npulses_total = 143360 # equal to int('23000')
        angle_degree = int(hexa_str, 16)/npulses_total*360
        angle_degree = round(angle_degree, 3)
    else:
        angle_degree = 0.0
    return angle_degree

def to8_format(in_str):
    '''
    Transforms input string from hexa format into 8 bit representation required
    for Thorlabs motors

    Parameters
    ----------
    inn_str : Hexa string with maximum length of 8 bits

    Returns
    -------
    format8 : Hexa string with exact length of 8 bits
    '''
    reduced_hex = in_str[2:len(in_str)] # cut first two digits
    if len(reduced_hex) < 7:
        return reduced_hex.zfill(8)
    else:
        raise ValueError('to8_format Error: input too long')
        return '00000000'

def write_to_device(bus, address, command):
    '''
    Uses pySerial to write bytes to the port

    Parameters
    ----------
    bus     :   Returned serial port object from open_serial function
    address :   Positive integer which specifies the bus address of the device
    command :   Data to send to the port in the format required by Thorlabs
                Motors: e.g. "0ma00005D55". This is passed in from move_abs.

    Returns
    -------
    Number of bytes written.
    '''
    bus.write(command.encode()) # encode to default utf-8 encoding

def get_position(bus, address):
    '''
    Read the current position from the respective Thorlabs Rotation Motor
    connected to address on bus

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device

    Returns
    -------
    angle : Angle of position in degrees as calculated by hexa_toangle()
    '''
    command = str(address) + 'gp'
    write_to_device(bus, address, command)
    line = bus.readline() # read and return one line from the stream
    # e.g. b'0PO00008B7B\r\n', line terminator b'\n' is for binary files
    print('---')
    print(line)
    hex = line[4:11] # hexa format, string type, e.g. b'08B7B'
    print('---')
    print(hex)
    angle = hexa_toangle(hex)
    return angle

def get_info(bus, address):
    '''
    Read the information from the respective Thorlabs Rotation Motor
    connected to address on bus

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device

    Returns
    -------
    serial : Serial number of the device
    '''
    command = str(address) + 'in'
    write_to_device(bus, address, command)
    line = bus.readline() # read and return one line from the stream
    # e.g. b'0PO00008B7B\r\n', line terminator b'\n' is for binary files
    print('---')
    print(line)
    serialdev = line[5:13] # hexa format, string type, e.g. b'08B7B'
    print('---')
    print(serialdev)
    return serialdev

def move_abs(bus, address, angle_degrees):
    '''
    Move to an absolute positive angle

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Value for absolute positive angle
    '''
    # print('move ' + str(address) + ' to:', round(angle_degrees, 2))
    command = str(address) + 'ma' + to8_format(angle_tohexa(angle_degrees))
    write_to_device(bus, address, command)

def move_fw(bus, address, angle_degrees):
    '''
    Rotate in forward direction to a relative angle

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Positive integer value for relative angle (fw)
    '''
    print('move ' + str(address) + ' fw: ', round(angle_degrees, 2))
    command = str(address) + 'sj' + to8_format(angle_tohexa(angle_degrees))
    write_to_device(bus, address, command)
    write_to_device(bus, address, str(address) + 'fw')

def move_bw(bus, address, angle_degrees):
    '''
    Rotate in forward direction to a relative angle

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Positive integer value for relative angle (bw)
    '''
    print('move ' + str(address) + ' bw: ', round(angle_degrees, 2))
    command = str(address) + 'sj' + to8_format(angle_tohexa(angle_degrees))
    write_to_device(bus, address, command)
    write_to_device(bus, address, str(address) + 'bw')

def set_offset(bus, address, angle_degrees):
    '''
    Set home angle for respective Thorlabs Motor connected to address on bus

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Value for absolute positive angle

    Returns
    -------
    ???
    '''
    print('set home offset ' + str(address) + ' to ' + str(angle_degrees))
    command = str(address) + 'so' + to8_format(angle_tohexa(angle_degrees))
    write_to_device(bus, address, command)

def get_offset(bus, address):
    '''
    Read the offset setting from the respective Thorlabs Rotation Motor
    connected to address on bus

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device

    Returns
    -------
    angle : Angle of position in degrees as calculated by hexa_toangle()
    '''
    command = str(address) + 'go'
    write_to_device(bus, address, command)
    line = bus.readline() # e.g b'0HO00001755\r\n'
    hex = line[4:11]
    angle = hexa_toangle(hex)
    return angle

def goto_offset(bus, address): # homes motor clockwise
    '''
    Moves respective Thorlabs Motor to home position

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Value for absolute positive angle
    '''
    print('homing '+ str(address))
    command = str(address) + 'ho1'
    write_to_device(bus, address, command) # 'ho0' clockwise, 'ho1' counter
