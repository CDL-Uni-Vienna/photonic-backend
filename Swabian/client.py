from TimeTagger import *
"""Connect to the server and run Countrate measurement"""
ttn = createTimeTaggerNetwork('127.0.0.1')
ctr = Countrate(ttn, [1,2])
ctr.startFor(int(1e12))
ctr.waitUntilFinished()
print(ctr.getData())