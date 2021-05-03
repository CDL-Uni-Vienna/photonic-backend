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
    com_port : str
        Target COM port of serial connection

    Returns
    -------
    ser : ???

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

def angle_tohexa(angle_degrees): # input degrees
    npulses_total = 143360 # equal to int('23000')
    theta_min = 360/npulses_total
    npulses = int(floor(angle_degrees/theta_min))
    angle_hexa = hex(npulses).upper()
    return angle_hexa # output in hexa, string format

def hexa_toangle(in_str): # input in hexa, string format
    npulses_total = 143360 # equal to int('23000')
    angle_degree = int(in_str, 16)/npulses_total*360
    angle_degree = round(angle_degree,3)
    return angle_degree # output in degrees, number format

def to8format(inn_str):
    '''
    Transforms input from hexa format into byte representation required for
    Thorlabs motors
    '''
    reduced_hex = inn_str[2:len(inn_str)] # cut first two digits
    if len(reduced_hex) < 7:
        zeroes = '0'
        while True:
            zeroes += '0'
            if len(zeroes)>(8-len(reduced_hex))-1:
                break
        format8 = zeroes + reduced_hex
        return format8
    else:
        print('to8format Error: input too long')
        return '00000000'

def write_to_motor(bus, address, command): # simplified command for action
    bus.write(command.encode())
    while True:
        line = bus.readline()
        if (str(address) in str(line)):
            break
        else:
            time.sleep(.05)

"******************************************************************"
"*********************** Reading functions  ***********************"
"******************************************************************"

def get_pos(motor, k):# reads current position of motor k-th
    motor.write((str(k)+'gp').encode())
    while(1):
        line = motor.readline()
        # leng = len(line)
        line_red = line[6:11]# hexa format, string format
        line_red = hexa_toangle(line_red)# angle in number format
        if line_red > 360:
            line_red = line[6:11]# hexa format, string format
            line_red = hexa_toangle(line_red) - hexa_toangle('FFFFF')
            line_red = round(line_red,3)
        print('end pos '+str(k)+': ',line_red,'\r\n')
        if (str(k) in str(line)):
            break
        else:
            time.sleep(.05)

def read_pos(motor, k):# reads current position of motor k-th
    motor.write((str(k)+'gp').encode())
    while(1):
        line = motor.readline()
        # leng = len(line)
        line_red = line[6:11]# hexa format, string format
        line_red = hexa_toangle(line_red)# angle in number format
        if line_red > 360:
            line_red = line[6:11]# hexa format, string format
            line_red = hexa_toangle(line_red) - hexa_toangle('FFFFF')
            line_red = round(line_red,3)
        if (str(k) in str(line)):
            break
        else:
            time.sleep(.05)
    return line_red

"*******************************************************************"
"*********************** Movement functions  ***********************"
"*******************************************************************"

def set_homeoff(motor, k, angle_degrees):# applies offset to homing k-motor
    print('set home offset '+string(k))
    write_to_motor(motor, k, str(k)+'so'+to8format(angle_tohexa(angle_degrees)))
    read_pos(motor,k)

def do_home(motor, k):# homes motor clockwise
    print('homing '+str(k))
    write_to_motor(motor, k, str(k)+'ho1')# 'ho0' clockwise, 'ho1' counter clockwise
    read_pos(motor,k)

def do_mr(motor, k, angle_degrees):# move relative positive angles
    write_to_motor(motor, k, str(k)+'mr'+to8format(angle_tohexa(angle_degrees)))

def move_topos(bus, address, angle_degrees):
    '''
    Move to an absolute positive angle

    Parameters
    ----------
    bus : ???
        Return value from open_serial
    address :
    angle_degrees : ???
        Value for absolute positive angle
    '''
    print('move '+str(address)+' to: ', round(angle_degrees,2))
    command = str(address)+'ma'+to8format(angle_tohexa(angle_degrees))
    write_to_motor(bus, address, command)
    read_pos(bus, address)

def move_fw(motor, k, angle_degrees):# moves forward
    print('move '+str(k)+' fw: ', round(angle_degrees,2))
    write_to_motor(motor, k, str(k)+'sj'+to8format(angle_tohexa(angle_degrees)))
    write_to_motor(motor, k, str(k)+'fw')
    read_pos(motor, k)

def move_bw(motor, k, angle_degrees):# moves backward
    print('move '+str(k)+' bw: ', round(angle_degrees,2))
    write_to_motor(motor, k, str(k)+'sj'+to8format(angle_tohexa(angle_degrees)))
    write_to_motor(motor, k, str(k)+'bw')
    read_pos(motor, k)
