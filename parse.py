import ast

import rest
import local_settings as settings

wp_assignment = {
    "Lamda2": 0,
    "Lamda4": 1
}

def parse(experiment): # experiment field from JSON
    print("-------")
    print(experiment)
    experiment = ast.literal_eval(experiment)
    for command in experiment:
        print("-------")
        print(command)
        address = wp_assignment[command[0]] + 2*command[2] # calculate address
        settings.waveplates[address].rotate(command[1])

print("Request data in JSON:")
data = rest.get(10)
print("Parsing:")
parse(data['experiment'])
