from CalibrationTools import Calibration

cali = Calibration()

# cali.minimizeCounts([[-1, 0]], [45], [1, 0])
# cali.minimizeCounts([[-2, 0]], [45], [2, 0])

# cali.minimizeCounts([[1, 0], [1, 1]], [45, 45], [1, 0])

# cali.minimizeCountsRep([[-1, 0]], [45], [1, 0], 5)
# cali.minimizeCountsRep([[-2, 0]], [45], [2, 0], 5)
# cali.minimizeCountsRep([[-3, 0]], [45], [3, 0], 5)
# cali.minimizeCountsRep([[-4, 0]], [45], [4, 0], 5)

# cali.measureInterval(-4, 0, [4, 0], [0, 90], 32)

# cali.measureAround(1, 1, [1, 0], 45)
cali.measureAround(1, 0, [1, 1], 0)

# cali.measureAround(-1, 0, [1, 0], 45)
# cali.measureAround(-2, 0, [2, 0], 45)
# cali.measureAround(-3, 0, [3, 0], 45)
# cali.measureAround(-4, 0, [4, 0], 45)

# cali.measureAround(0, 0, [4, 0], 45)

# cali.measureAround(1, 0, [1, 0], 45)
# cali.measureAround(2, 0, [2, 0], 45)
# cali.measureAround(3, 0, [3, 0], 45)
# cali.measureAround(4, 0, [4, 0], 45)

# cali.measureAround(1, 1, [1, 0], 45)
# cali.measureAround(2, 1, [2, 0], 45)
# cali.measureAround(3, 1, [3, 0], 45)
# cali.measureAround(4, 1, [4, 0], 45)

cali.fina()
# cali.measureAround(1, 1, [1, 0], 45)
# cali.measureAround(1, 1, [1, 0], 45)

# tt = Timetagger()

# tt.countrate(1, 0)
# from Settings.measurement_settings import setupDic, ttDic
# from TimeTagger import *

# address = '131.130.102.124'

# ttn = createTimeTaggerNetwork(address)

# cr = Countrate(ttn, [1, 2, 5, 7])
# cr.startFor(1e12)
# cr.waitUntilFinished()
# # Print the resulting data
# print(cr.getData())
# # Close the connection to the server
# freeTimeTagger(ttn)
