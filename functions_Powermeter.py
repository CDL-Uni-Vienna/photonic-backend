import ctypes
from ThorLabs import TLPM as ThorLib
import pylab

def open_powermeter(serialnumber):
    """
    Description
    -----------
          Open the powermeter.

    Parameters
    ----------
    serialnumber : str
        Serial number of the powermeter

    Returns
    -------
    powermeter : class
        Python object of the powermeter

    """
    powermeter = ThorLib.TLPM()
    powermeter.findRsrc()
    i = 0
    while True:
        resourceName = powermeter.getRsrcName(i)[1]
        i += 1
        if bytes(serialnumber, "utf8") in ctypes.c_char_p(resourceName.raw).value:
            powermeter.open(resourceName)
            return powermeter



def close_powermeter(powermeter):
    """
    Description
    -----------
          Close the powermeter.

    Parameters
    ----------
    powermeter : class
        Python object of the powermeter
    """
    powermeter.close()



def read_power(powermeter, unit = 0, wavelenght = 930):
    """
    Read the power in a certain unit and in a definite wavelenght.

    Parameters
    ----------
    powermeter : class
        Python object of the powermeter.
    unit : int
        0 - power measured in Watt
        1 - power measured in dBm
    wavelenght : float
        Wavelenght to use to compute the power from the detected current in nm.

    Returns
    -------
    power : float
        Power read from the powermeter in uW.

    """
    powermeter.setPowerUnit(unit)
    powermeter.setWavelength(wavelenght)
    power = powermeter.measPower()[1] * 1e6

    return round(power, 4)



def makefigure_wpscan(positions, powers):
    """
    Plots the power vs. positions of the data acquired from the waveplate.

    Parameters
    ----------
    positions : list
        list of positions of the wave plate
    powers : list
        list of the corresponding powers

    Returns
    -------
    None.

    """
    pylab.figure()
    pylab.plot(positions, powers, '.-', label='wp scan ')
    pylab.legend()
    # title('Uses PM100USB')
    pylab.xlabel('Angle (degrees)')
    pylab.ylabel('Power (uW)')
    pylab.tight_layout()
    pylab.tight_layout()
    pylab.show()
