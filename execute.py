import json

import rest
import Settings.local_settings as settings

wp_assignment = {
    "Lamda2": 0,
    "Lamda4": 1
}



print("Request data in JSON:")
data = rest.get(3)
#data = json.loads(data)
print(data["experiment"][0])
