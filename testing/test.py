from waveplate import Waveplate
import local_settings as settings

wp1 = Waveplate(0, settings.offset_0)
wp1.rotate(89.67454)
wp1 = Waveplate(1, settings.offset_1)
wp1.rotate(5.7)
