from ControlTimetagger import Timetagger
from ControlPlatesArray import PlatesArray

from matplotlib import pyplot
from scipy import optimize
import numpy as np


def fit(x, a, b):
    return a*(np.sin((b*x)))


angle = float(0)
data = []
x = []

p_array1 = PlatesArray(1)

p_array1.init()

while angle < 180:
    # p_array1 = PlatesArray(1)
    x.append(float(angle))
    # p_array1.init()
    # path 1, Quarter, Half
    p_array1.setPath(1, [0, angle])
    angle = angle + 10
    # p_array1.fina()

    timetagger = Timetagger()

    res = timetagger.countrates()
    count = res[0]
    print("-----")
    print(count)
    data.append(float(count))

p_array1.fina()

print("X")
print(x)
print("DATA")
print(data)

params, params_covariance = optimize.curve_fit(fit, x, data)
print("PARAMS")
print(params)
pyplot.scatter(x, data, label="raw")
# pyplot.plot(x, fit(x, params[0], params[1]),
#            label='fit')
pyplot.show()
