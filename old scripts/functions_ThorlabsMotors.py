# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:28:59 2020

@author: juanl
"""
import serial # be aware that you need to install ALSO "pyserial" which is an extension of the standard package "serial" provided by default in anaconda installation
from pylab import *
# import math
## in, gs, us, i1, f, b, s, c;  hox   some useful comands

"**********************************************************************"
"************************ Background functions ************************"
"**********************************************************************"

def open_serial(dev):
    ser=serial.Serial(dev,9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False)
    return ser

def todeci(in_str):# input in hexa, string format
    deciout = int(in_str,16)
    return deciout# output in decimal, integer format 

def tohexa(inn):# input in decimals, output, e.g., '0x4F5'
    hexaout = hex(inn).upper()
    return hexaout# output in hexa, string format 

def angle_tohexa(angle_degrees):# input degrees
    npulses_total = 143360# equal to todeci('23000')
    theta_min = 360/npulses_total
    npulses = int(floor(angle_degrees/theta_min))
    angle_hexa = tohexa(npulses)
    return angle_hexa# output in hexa, string format

def hexa_toangle(in_str):# input in hexa, string format
    npulses_total = 143360# equal to todeci('23000')
    angle_degree = todeci(in_str)/npulses_total*360
    angle_degree = round(angle_degree,3)
    return angle_degree# output in degrees, number format



def mm_tohexa(distance_mm):# input in mm
    npulses_total = 61440# equal to todeci('F000')
    distance_min = 60/npulses_total
    npulses = int(floor(distance_mm/distance_min))
    distance_hexa = tohexa(npulses)
    return distance_hexa# output in hexa, string format

def hexa_tomm(in_str):# input in hexa, string format
    npulses_total = 61440# equal to todeci('F000')
    dist_mm = todeci(in_str)/npulses_total*60
    dist_mm = round(dist_mm,3)
    return dist_mm# output in mm, number format



def to8format(inn_str):# input in hexa format, e.g., 0xAF012
    reduced_hex = inn_str[2:len(inn_str)]
    leng = len(reduced_hex)
    zeroes = '0'
    while True:
        zeroes += '0'
        if len(zeroes)>(8-leng)-1:
            break
    format8 = zeroes+reduced_hex
    return format8# outputs 8bit format required for Thorlabs motors

def docmd(motor, k, cmdd):# command reading motor in default hex format
    print('cmd: ',cmdd)
    motor.write(cmdd.encode())
    while(1):
        line=motor.readline()
        print('read:',line,'\r\n')#'\r\n'
        if (str(k) in str(line)):
            break
        else:
            time.sleep(.05)
            
def docmd2(motors, k, cmdd):# simplified command for action
    motors.write(cmdd.encode())
    while(1):
        line=motors.readline()
        if (str(k) in str(line)):
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

def readlin_pos(motor, k):# reads current position of motor k-th
    motor.write((str(k)+'gp').encode())
    while(1):
        line = motor.readline()
        # leng = len(line)
        line_red = line[7:11]# hexa format, string format
        line_red = hexa_tomm(line_red)# position in number format
        if line_red > 60:
            line_red = line[7:11]# hexa format, string format
            line_red = hexa_tomm(line_red) - hexa_tomm('FFFF')
            line_red = round(line_red,3)
        print('endlin pos '+str(k)+': ',line_red,'\r\n')
        if (str(k) in str(line)):
            break
        else:
            time.sleep(.05)
            
def getlin_pos(motor, k):# reads current position of motor k-th
    motor.write((str(k)+'gp').encode())
    while(1):
        line = motor.readline()
        # leng = len(line)
        line_red = line[7:11]# hexa format, string format
        line_red = hexa_tomm(line_red)# position in number format
        if line_red > 60:
            line_red = line[7:11]# hexa format, string format
            line_red = hexa_tomm(line_red) - hexa_tomm('FFFF')
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
    docmd2(motor, k, str(k)+'so'+to8format(angle_tohexa(angle_degrees)))
    read_pos(motor,k)

def do_home(motor, k):# homes motor clockwise
    print('homing '+str(k))
    docmd2(motor, k, str(k)+'ho1')# 'ho0' clockwise, 'ho1' counter clockwise
    read_pos(motor,k)

def do_mr(motor, k, angle_degrees):# move relative positive angles
    docmd(motor, k, str(k)+'mr'+to8format(angle_tohexa(angle_degrees)))    
    
    
    
def move_topos(motor, k, angle_degrees):# move to an absolute positive angle
    print('move '+str(k)+' to: ', round(angle_degrees,2))
    docmd2(motor, k, str(k)+'ma'+to8format(angle_tohexa(angle_degrees)))
    read_pos(motor,k)    
    
def move_fw(motor, k, angle_degrees):# moves forward
    print('move '+str(k)+' fw: ', round(angle_degrees,2))
    docmd2(motor, k, str(k)+'sj'+to8format(angle_tohexa(angle_degrees)))
    docmd2(motor, k, str(k)+'fw')
    read_pos(motor, k)    
    
def move_bw(motor, k, angle_degrees):# moves backward 
    print('move '+str(k)+' bw: ', round(angle_degrees,2))
    docmd2(motor, k, str(k)+'sj'+to8format(angle_tohexa(angle_degrees)))
    docmd2(motor, k, str(k)+'bw')
    read_pos(motor, k)    
    
    
    
def movelin_topos(motor, k, dist_mm):# move to an absolute positive position
    print('movelin '+str(k)+' to: ', round(dist_mm,2))
    docmd2(motor, k, str(k)+'ma'+to8format(mm_tohexa(dist_mm)))
    readlin_pos(motor,k)     
    
def movelin_fw(motor, k, dist_mm):# moves forward
    print('movelin '+str(k)+' fw: ', round(dist_mm,2))
    docmd2(motor, k, str(k)+'sj'+to8format(mm_tohexa(dist_mm)))
    docmd2(motor, k, str(k)+'fw')
    readlin_pos(motor, k)
  
def movelin_bw(motor, k, dist_mm):# moves backward 
    print('movelin '+str(k)+' bw: ', round(dist_mm,2))
    docmd2(motor, k, str(k)+'sj'+to8format(mm_tohexa(dist_mm)))
    docmd2(motor, k, str(k)+'bw')
    readlin_pos(motor, k)    
    


    
    
    