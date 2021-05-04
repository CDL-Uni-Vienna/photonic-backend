import serial
from pylab import floor

"**********************************************************************"
"************************ Background functions ************************"
"**********************************************************************"

def open_serial(com_port):
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
            timeout = None,
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
    Transforms input float number into hexa format required by Thorlabs motors

    Parameters
    ----------
    angle_degrees : Float number which specifies angle in degrees

    Returns
    -------
    angle_hexa : Hexa string type with exact length of 8 bits
    '''
    npulses_total = 143360 # equal to int('23000')
    theta_min = 360/npulses_total
    npulses = int(floor(angle_degrees/theta_min))
    angle_hexa = hex(npulses).upper()
    return angle_hexa # output in hexa, string format

def hexa_toangle(hexa_str):
    '''
    Retransforms input hexa string into float number

    Parameters
    ----------
    hexa_str : Hexa format as string type

    Returns
    -------
    angle_degree : Number in deegrees as float type
    '''
    npulses_total = 143360 # equal to int('23000')
    angle_degree = int(hexa_str, 16)/npulses_total*360
    angle_degree = round(angle_degree,3)
    return angle_degree # output in degrees, number format

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
        zeroes = '0'
        while True:
            zeroes += '0'
            if len(zeroes)>(8-len(reduced_hex))-1:
                break
        format8 = zeroes + reduced_hex
        return format8
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
    ???
    '''
    bus.write(command.encode()) # encode to default utf-8 encoding
    while True:
        line = bus.readline()
        if (str(address) in str(line)):
            break
        else:
            time.sleep(.05)

"******************************************************************"
"*********************** Reading functions  ***********************"
"******************************************************************"

def read_pos(bus, address): # reads current position of motor k-th
    '''Reading function under development'''
    bus.write((str(address)+'gp').encode())
    while True:
        line = bus.readline() # read and return one line from the stream
        print('-----')
        print(line)
        # leng = len(line)
        hex = line[6:11] # hexa format, string format
        angle = hexa_toangle(hex) # angle in number format
        print('-----')
        print(angle)
        if angle > 360:
            angle = line[6:11] # hexa format, string format
            angle = hexa_toangle(line_read) - hexa_toangle('FFFFF')
            angle = round(angle, 3)
        if (str(address) in str(line)):
            break
        else:
            time.sleep(.05)
    return angle

"*******************************************************************"
"*********************** Movement functions  ***********************"
"*******************************************************************"

def set_homeoff(motor, k, angle_degrees):# applies offset to homing k-motor
    print('set home offset '+string(k))
    write_to_device(motor, k, str(k)+'so'+to8_format(angle_tohexa(angle_degrees)))
    read_pos(motor,k)

def do_home(motor, k): # homes motor clockwise
    print('homing '+str(k))
    write_to_device(motor, k, str(k)+'ho1') # 'ho0' clockwise, 'ho1' counter clockwise
    read_pos(motor,k)

def move_rel(motor, k, angle_degrees):
    '''move relative positive angles'''
    write_to_device(motor, k, str(k)+'mr'+to8_format(angle_tohexa(angle_degrees)))

def move_abs(bus, address, angle_degrees):
    '''
    Move to an absolute positive angle

    Parameters
    ----------
    bus     : Serial port object which is returned from open_serial
    address : Positive integer which specifies the bus address of the device
    angle_degrees : Value for absolute positive angle
    '''
    print('move '+str(address)+' to: ', round(angle_degrees,2))
    command = str(address)+'ma'+to8_format(angle_tohexa(angle_degrees))
    write_to_device(bus, address, command)
    read_pos(bus, address)

def move_fw(motor, k, angle_degrees):
    '''moves forward'''
    print('move '+str(k)+' fw: ', round(angle_degrees,2))
    write_to_device(motor, k, str(k)+'sj'+to8_format(angle_tohexa(angle_degrees)))
    write_to_device(motor, k, str(k)+'fw')
    read_pos(motor, k)

def move_bw(motor, k, angle_degrees):
    '''moves backward'''
    print('move '+str(k)+' bw: ', round(angle_degrees,2))
    write_to_device(motor, k, str(k)+'sj'+to8_format(angle_tohexa(angle_degrees)))
    write_to_device(motor, k, str(k)+'bw')
    read_pos(motor, k)
