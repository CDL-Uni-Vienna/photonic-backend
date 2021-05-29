import rest
import Settings.local_settings as settings


print("Request data in JSON:")
data = rest.get(3)
print(data)
print("-----")
print(data["experiment"][0])


for shot in range(0, data["shots"]):
    for command in data["experiment"]:
        if command["name"] == "QWP":
            
        if command["name"] == "HWP":

        if command["name"] == "measure":

