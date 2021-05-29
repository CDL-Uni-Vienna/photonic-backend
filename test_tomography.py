from ControlPowermeter import measure_row
from ControlWaveplate import Waveplate
from ControlPowermeter import open_powermeter, close_powermeter, measure_row, measure_power
import Settings.local_settings as settings

QWP = Waveplate(0)
HWP = Waveplate(1)
ControlPowermeter.open_powermeter(settings.serialnumber)

# measure in H
QWP.rotate(0)
HWP.rotate(0)
measure_row(5)

# measure in V
QWP.rotate(0)
HWP.rotate(45)
measure_row(5)

# measure in D
QWP.rotate(45)
HWP.rotate(22,5)
measure_row(5)

# measure in A
QWP.rotate(45)
HWP.rotate(67,5)
measure_row(5)

# measure in R
QWP.rotate(45)
HWP.rotate(45)
measure_row(5)

# measure in L
QWP.rotate(45)
HWP.rotate(0)
measure_row(5)