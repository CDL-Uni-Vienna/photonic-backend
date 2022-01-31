from TimeTagger import *
from time import sleep

"""Connect to the server and run Countrate measurement"""
# ttn = createTimeTaggerNetwork('127.0.0.1')
ttn = createTimeTagger()
# ttn = createTimeTaggerNetwork('131.130.102.124')
print("A")
sleep(0.5)
print("B")
ctr = Counter(
    tagger=ttn, channels=[1, 2, 5, 7, 10, 11, 12, 13], binwidth=int(1e11), n_values=50
)
print("C")
ctr.startFor(int(1e12))
print("D")
ctr.waitUntilFinished()
print("E")
print(ctr.getData())
# print(ttn.getChannelList())
