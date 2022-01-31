from os import listdir
# from os.path import join
from json import load
from statistics import mean, stdev

json_files = listdir("Calibration")

json_files = [k for k in json_files if ".json" in k]

for json in json_files:

    with open("Calibration/" + json, "r") as read_file:
        dataDic = load(read_file)

    mean_ang = mean(dataDic.values())
    std_ang = stdev(dataDic.values())

    print(json + " " + str([mean_ang - 45, mean_ang, std_ang]))
