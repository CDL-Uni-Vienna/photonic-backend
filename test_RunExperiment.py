from ControlRunExperiment import RunExperiment
import os
import json

exp_file = 'exp12.json'
res_file = "res" + exp_file

d = os.getcwd()
d = os.path.join(d, 'Experiments', exp_file)

with open(d, "r") as read_file:
    exp_json = json.load(read_file)

runx = RunExperiment(exp_json, "AAAA")


print("-------------------------------------------------R")
print(runx.results)
