import rest
import Settings.local_settings as settings


<<<<<<< HEAD
=======
def h_gate(qubit):
    """

    """
    

>>>>>>> 4649ab8889cab87daf81d04fa0312af6f60e3d1c
print("Request data in JSON:")
data = rest.get(4)
print(data)
print("-----")
print(data["experiment"][0])


<<<<<<< HEAD
for shot in range(0, data["shots"]):
    for command in data["experiment"]:
        if command["name"] == "QWP":
            
        if command["name"] == "HWP":

        if command["name"] == "measure":

=======
# for shot in range(0, data["shots"]):
#     for command in data["experiment"]:
#         if command["name"] == "H":
>>>>>>> 4649ab8889cab87daf81d04fa0312af6f60e3d1c
