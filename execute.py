import rest
import Settings.local_settings as settings
from ControlWaveplate import Waveplate
from ControlPowermeter import open_powermeter, close_powermeter, measure_row


data = rest.get(7)
print("-----")
print("Request data in JSON:")
print(data)
print("-----")
print(data["experiment"][0])
print(data["experiment"][0]["qubits"])
print(data["experiment"][1])
print(data["experiment"][2])

qwp = settings.waveplates["mode" + str(data["experiment"][0]["qubits"]) + "/quarter"]
hwp = settings.waveplates["mode" + str(data["experiment"][0]["qubits"]) + "/half"]
pm = open_powermeter(settings.serialnumber)

print("shots:")
print(data["shots"])

for run in range(0, data["shots"]):
    for command in data["experiment"]:
        print(type(command["params"]))
        if command["name"] == "QWP":
            qwp.rotate(float(command["params"]))
        elif command["name"] == "HWP":
            hwp.rotate(float(command["params"]))
        elif command["name"] == "measure":
            measure_row(pm, int(float(command["params"])))

close_powermeter(pm)
