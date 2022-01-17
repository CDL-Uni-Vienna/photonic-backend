import json
import os
from ControlExperiment import Experiment

exp_file = 'exp12.json'
res_file = "res" + exp_file

d = os.getcwd()
d = os.path.join(d, 'Experiments', exp_file)

# with open(d, 'r') as file:
#     exp = file.read()
#     exp11_json = json.loads(exp)

with open(d, "r") as read_file:
    exp11_json = json.load(read_file)

exp11 = Experiment(exp11_json)

exp11.getPlatesAngles()

exp11.setPlatesAngles()

# exp11.rawMeasure()
