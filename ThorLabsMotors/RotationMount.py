"""
Control library for ThorLabs Rotation Mount with Resonant Piezoelectric Motors
based on serial commands and the pySerial module
"""

from math import floor
import serial
import time
from random import uniform


def open_serial(com_port, timeout=None):
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
        port=com_port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=timeout,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
        write_timeout=None,
        inter_byte_timeout=None,
        exclusive=True
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
    npulses_total = 143360  # equal to int('23000')
    theta_min = 360/npulses_total
    npulses = int(floor(angle_degrees/theta_min))
    angle_hexa = hex(npulses).upper()  # e.g. 0X23C7
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
    # print('---')
    # print(hexa_str)
    if hexa_str != b'\n':
        npulses_total = 143360  # equal to int('23000')
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
    reduced_hex = in_str[2:len(in_str)]  # cut first two digits
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
    bus.write(command.encode())  # encode to default utf-8 encoding


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
    line = bus.readline()  # read and return one line from the stream
    # e.g. b'0PO00008B7B\r\n', line terminator b'\n' is for binary files
    # print('---')
    # print(line)
    hex = line[4:11]  # hexa format, string type, e.g. b'08B7B'
    # print('---')
    # print(hex)
    angle = hexa_toangle(hex)
    print(angle)
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
    line = bus.readline()  # read and return one line from the stream
    if line != b'':
        print(line)
        # e.g. b'0PO00008B7B\r\n', line terminator b'\n' is for binary files
    serialdev = line[5:13]  # hexa format, string type, e.g. b'08B7B'

    return serialdev


def get_status(bus, address):
    '''
    Read the status from the respective Thorlabs Rotation Motor
    connected to address on bus

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device

    Returns
    -------
    status : Status of the device
    '''
    command = str(address) + 'gs'
    write_to_device(bus, address, command)
    line = bus.readline()  # read and return one line from the stream
    # e.g. b'0PO00008B7B\r\n', line terminator b'\n' is for binary files
    # print('---') #
    print(line)
    status = line  # [5:13] # hexa format, string type, e.g. b'08B7B'
    # print('---') #
    # print(status) #
    return status


def home(bus, address):
    '''
    Read the status from the respective Thorlabs Rotation Motor
    connected to address on bus

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device

    Returns
    -------
    status : Status of the device
    '''
    command = str(address) + 'ho0'
    write_to_device(bus, address, command)
    line = bus.readline()  # read and return one line from the stream
    # e.g. b'0PO00008B7B\r\n', line terminator b'\n' is for binary files
    # print('---') #
    # print(line)
    status = line  # [5:13] # hexa format, string type, e.g. b'08B7B'
    # print('---') #
    # print(status) #
    return status


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


def move_abs_n_hear(bus, address, angle_degrees_in, iterations):
    '''
    Move to an absolute positive angle

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Value for absolute positive angle
    iterations: Carry the number of iterations tried (used to avoid inf self calling loop)
    '''
    wtime = 2.0
    max_iterations = 10
    tolerance = 0.02
    angle_degrees = angle_degrees_in % 360

    iterations = iterations + 1
    # print('move ' + str(address) + ' to:', round(angle_degrees, 2))
    command = str(address) + 'ma' + to8_format(angle_tohexa(angle_degrees))
    write_to_device(bus, address, command)

    time.sleep(0.1)

    line = bus.readline()

    time.sleep(0.1)

    line = line.decode('utf-8')

    reply_type = line[1:3]

    mssg = 'RotationMount.move_abs_n_hear :: Device in address ' + \
        str(address) + ' '
    mssgappend = ' [ Iteration: ' + str(iterations) + ' ]'

    if iterations >= max_iterations:
        print(mssg + 'failed to converge after maximum number of attemps' +
              mssgappend + ' ERROR')
        return None
    elif reply_type == 'PO':
        hex = line[4:11]
        angle = hexa_toangle(hex)
        angle = angle % 360
        print(mssg + 'moved to ' + str(angle) +
              '° (' + line[:-2] + ')' + mssgappend)
        if abs(angle_degrees-angle) > tolerance:
            print(mssg + 'did not converge to the angle within the tolerance (' +
                  str(abs(angle_degrees-angle)) + '>' + str(tolerance) + '°)' + mssgappend)
            print(mssg + 'is trying a two steps approach' + mssgappend)
            time.sleep(wtime)
            move_abs(bus, address, (angle_degrees +
                     uniform(0.001, tolerance)) % 360)
            #move_abs(bus, address, uniform(10, 350))
            time.sleep(wtime)
            move_abs_n_hear(bus, address, angle_degrees, iterations)
    elif reply_type == 'GS':
        print(mssg + 'replied error: ' + line[:-2] + mssgappend)
        print(mssg + 'is trying a two steps approach' + mssgappend)
        time.sleep(wtime)
        #move_abs(bus, address, (angle_degrees + uniform(0.5 , 2.0)) % 360 )
        move_abs(bus, address, (angle_degrees +
                 uniform(0.001, tolerance)) % 360)
        #move_abs(bus, address, uniform(10, 350))
        time.sleep(wtime)
        move_abs_n_hear(bus, address, angle_degrees, iterations)
    elif reply_type == '':
        print(mssg + 'did not reply' + mssgappend)
        time.sleep(wtime)
        print(mssg + 'is trying a two steps approach' + mssgappend)
        move_abs(bus, address, (angle_degrees +
                 uniform(0.001, tolerance)) % 360)
        #move_abs(bus, address, uniform(10, 350))
        time.sleep(wtime)
        move_abs_n_hear(bus, address, angle_degrees, iterations)
    else:
        time.sleep(wtime)
        print(mssg + 'replied unknown message: ' + reply_type + mssgappend)


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
    line = bus.readline()  # e.g b'0HO00001755\r\n'
    hex = line[4:11]
    angle = hexa_toangle(hex)
    return angle


def goto_offset(bus, address):  # homes motor clockwise
    '''
    Moves respective Thorlabs Motor to home position

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Value for absolute positive angle
    '''
    print('homing ' + str(address))
    command = str(address) + 'ho1'
    write_to_device(bus, address, command)  # 'ho0' clockwise, 'ho1' counter
