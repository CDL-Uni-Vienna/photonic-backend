import ctypes
import time

from ThorLabsMotors import PowerMeter
import Settings.measurement_settings as settings


def open_powermeter(serialnumber):
    '''
    Functionality: Open the powermeter (PM)

    Parameters: serialnumber of the PM string type

    Returns: powermeter : ThorLabsMotors.PowerMeter.TLPM object
    '''
    powermeter = PowerMeter.TLPM()
    deviceCount = ctypes.c_uint32()
    powermeter.findRsrc(ctypes.byref(deviceCount))
    # returns (0, <cparam 'P' (00000161BE6D5A88)>)
    for i in range (0, deviceCount.value):
        # deviceCount.value = no. of powermeters, is 1 if one powermeter is connected
        resourceName = powermeter.getRsrcName(i, resourceName=ctypes.create_string_buffer(1024))[1]
        # getRsrcName for each instance returns tuple (0, <ctypes.c_char_Array_1024 object at 0x00000161B8FAD8C0>)
        # resourceName is e.g. <ctypes.c_char_Array_1024 object at 0x00000161B8FAD8C0>
        if serialnumber in str(ctypes.c_char_p(resourceName.raw).value):
            # ctypes.c_char_p(resourceName.raw).value is e.g. b'USB0::0x1313::0x8072::1909736::INSTR'
            powermeter.open(resourceName, IDQuery=ctypes.c_bool(False), resetDevice=ctypes.c_bool(False))
            # powermeter object <ThorLabsMotors.PowerMeter.TLPM object at 0x0000027A391360A0>
            return powermeter

def close_powermeter(powermeter):
    '''
    Description: Closes the powermeter.

    Parameters: powermeter object
    '''
    powermeter.close()
    print('Powermeter closed')

def measure_row(powermeter, counts):
    powermeter.setPowerUnit(settings.powerUnit)
    powermeter.setWavelength(settings.wavelength)
    power_measurements = []
    for i in range(counts):
        power = powermeter.measPower()[1]
        # returned value is already c_double().value
        power_measurements.append(power)
        # print('-----')
        # print(power)
        # print(i)
        time.sleep(0.5) # do I need this? for 600 values this takes 300 secs
    return power_measurements