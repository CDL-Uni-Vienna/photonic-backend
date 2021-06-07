import rest
import Settings.local_settings as settings
# from ControlWaveplate import Waveplate
from ControlPowermeter import open_powermeter, close_powermeter, measure_row

id = 2
data = rest.get_job_snek(id)
# print("-----")
# print("Request data in JSON:")
# print(data)
# print("-----")
# print(data["experiment"][0])
# print(data["experiment"][0]["qubits"])
# print(data["experiment"][1])
# print(data["experiment"][2])

qwp = settings.waveplates["mode" + str(data["experiment"][0]["qubits"]) + "/quarter"]
hwp = settings.waveplates["mode" + str(data["experiment"][0]["qubits"]) + "/half"]
pm = open_powermeter(settings.serialnumber)

# print("shots:")
# print(data["shots"])

measurement_no = []
raw_data = []
i = 0
#for run in range(1): #range(0, data["shots"]+1):
for command in data["experiment"]:
    if command["name"] == "QWP":
        # command["params"] is string type
        print('Move QWP to ' + str(command["params"]))
        qwp.rotate(float(command["params"]))
    elif command["name"] == "HWP":
        hwp.rotate(float(command["params"]))
        print('Move HWP to ' + str(command["params"]))
    elif command["name"] == "measure":
        m = measure_row(pm, int(float(command["params"])))
        print('Measurement ' + str(i), m)
        measurement_no.append('measurement ' + str(i))
        raw_data.append(m)
        i = i + 1
        
# print(measurement_no)
# print(raw_data)          

zip_iterator = zip(measurement_no, raw_data)
dictionary = dict(zip_iterator)
print(dictionary)

rest.post_result_snek(str(dictionary), id)

close_powermeter(pm)
