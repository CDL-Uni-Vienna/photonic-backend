from matplotlib import pyplot as plt
import numpy as np
from time import sleep

import TimeTagger

#tagger = TimeTagger.createTimeTagger()
tagger = TimeTagger.createTimeTaggerNetwork('127.0.0.1')
#tagger = TimeTagger.createTimeTaggerNetwork('131.130.102.124')
print("A")
sleep(0.5)
print("B")
# binwidth (int) – bin width in ps
counter = TimeTagger.Counter(tagger=tagger, channels=[
    7], binwidth=int(1e11), n_values=50)
# print(counter)

print("C")

data = counter.getData()
print(data)
print("D")
# picks row from detector data matrix
# channel refers to the row of the matrix


def pick_channel(list, channel):
    channel_data = list[channel]
    print(channel_data)
    return channel_data


def pop_zeros(array):
    indices = np.where(array == 0)
    clean_array = np.delete(array, indices)
    print("----------")
    print(clean_array)
    print("----------")
    return clean_array


# choose first column of detector data
channel_data = pick_channel(data, 0)
print(channel_data)

pop_zeros(channel_data)
print(channel_data)
# print(data[0])
