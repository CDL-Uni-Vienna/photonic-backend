from TimeTagger import *
from time import sleep

tt = createTimeTagger()
print("Enable test signal on channel 1 and 2.")
tt.setTestSignal(1, True)
tt.setTestSignal(2, True)
exposedChannels = [1, 2]
print('\nExposedChannels {}'.format(exposedChannels))
conn_mode = ConnectionMode.Control
tt.startServer(conn_mode, exposedChannels)
print ("Server is running - abort with STRG+C")
while(True):
    sleep(1)