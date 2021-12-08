from math import sqrt


def flatten(t):
    return [item for sublist in t for item in sublist]

def thphToPlatesAngles(thph):
    import numpy as np

    th = thph[0]
    ph = thph[1]

    tanTh = np.tan(th)
    tanTh2 = tanTh**2
    cosPh = np.cos(ph)
    cosPh2 = cosPh**2
    cosPh3 = cosPh**3
    secTh = 1/cosPh
    secTh2 =secTh**2
    sinPh = np.sin(ph)
    sinPh2 = sinPh**2
    sin2Ph = np.sin(2*ph)
    sqrtPhTh = np.sqrt(1+cosPh2*tanTh2)
    
    return [
        np.rad2deg(np.arctan2(
            tanTh,
            secTh)/2),
        np.rad2deg(np.arctan2(
           tanTh*(cosPh*(1+sinPh2)+cosPh3*(secTh2+tanTh2)-2*sinPh*sqrtPhTh),
           1+sinPh2+cosPh2*(secTh2+tanTh2)+sin2Ph*tanTh2*sqrtPhTh)/4)
    ]

def alphaToPlatesAngles(alpha):
       
    return [45, (180-2*alpha)/8]