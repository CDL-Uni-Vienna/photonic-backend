from ControlRemoteExec import RemoteExec
import json
import os

exp_file = 'exp12.json'

d = os.getcwd()
d = os.path.join(d, 'Experiments', exp_file)

with open(d, "r") as read_file:
    test_json = json.load(read_file)

rex = RemoteExec(test_json, 1234567)

print(rex.res_json)
