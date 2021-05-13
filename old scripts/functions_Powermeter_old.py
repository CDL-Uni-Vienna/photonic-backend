# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:52:54 2020

@author: juanl
"""

# Requires installation of libraries for ThorlabsPM100, and pyvisa

from ThorlabsPM100 import ThorlabsPM100 # library to deal with module-based powermeter
import pylablib.aux_libs.devices.Thorlabs as thor
import pyvisa # also install pyvisa-py
from pylab import *

# rm = pyvisa.ResourceManager() # following 2 lines to recognise device
# print(rm.list_resources())

# example of output: ('USB0::4883::32882::1907988::0::INSTR',)
# need place ('...') with hexa number format


def open_powermeter(serialnumber, pm_type):# input serial number, string format
    if (pm_type==1):
        out = thor.PM100D("USB0::0x1313::0x807B::"+serialnumber+"::INSTR")#input taken from rm.list_resources()
        return out
    else:
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource("USB0::0x1313::0x8072::"+serialnumber+"::INSTR")#input taken from rm.list_resources()
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        inst.timeout = 1000
        out = ThorlabsPM100(inst=inst)
        return out

def close_powermeter(powermeter, pm_type):
    if (pm_type==1):
        powermeter.close()
    else:
        pyvisa.ResourceManager().close()
    
def read_power(powermeter, pm_type):
    if (pm_type==1):
        reading = powermeter.get_power()
        return round(reading * 1e6, 5)  #(output in uW)
    
    else:
        reading = powermeter.read
        reading = round(reading*1e9,5)# 1e9 returns units in nano amperes
        # nAtouW = 2.086/116.8# 'arbitrarily' defined, here callibrates nA to uW
        nAtouW = 21.4/1015.# 'arbitrarily' defined, here callibrates nA to uW    
        reading = round(reading*nAtouW,5)
        return reading

def makefigure_wpscan(positions, powers):
    figure()
    plot(positions, powers, '.-', label='wp scan ')
    legend()
    title('Uses PM100USB')
    xlabel('Angle (degrees)')
    ylabel('Power (uW)')
    tight_layout()
    tight_layout()
    show()