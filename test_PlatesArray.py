from ControlPlatesArray import PlatesArray

p_array1 = PlatesArray(1)

p_array1.init()

print(p_array1.devices_unkno)
print(p_array1.devices_known)

#p_array1.setAngles([ 45, 22.5, 40, 35, 180, 60, 90, 100, 10 ])
p_array1.setAngles([ 90, 90, 90, 90, 90, 90, 90, 90, 90])
#p_array1.setAngles([ 0, 0, 0, 0, 0, 0, 0, 0, 0])

p_array1.fina()