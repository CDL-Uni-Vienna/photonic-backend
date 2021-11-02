import json
import os
from ControlExperiment import Experiment

d = os.getcwd()
#d = os.path.join(d, 'photonic-backend', 'Experiments','exp11.json')
d = os.path.join(d, 'Experiments','exp11.json')

with open(d, "r") as read_file:
    exp11_json = json.load(read_file)

exp11 = Experiment(exp11_json)

exp11.getPlatesAngles()

exp11.rawExecute()
