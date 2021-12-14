from ControlPlatesArray import PlatesArray

p_array1 = PlatesArray(1)

p_array1.init()

print(p_array1.devices_unkno)
print(p_array1.devices_known)

p_array1.setPath(0, [0])
p_array1.setPath(1, [2.2, 15])
p_array1.setPath(2, [0, 90])
p_array1.setPath(3, [180, 270])
p_array1.setPath(4, [0, 0])
#p_array1.setPath(5, [22, 5])
#p_array1.setAngles([ 45, 35, 40, 36, 180, 60, 90, 100, 10 ])
#p_array1.setAngles([10, 10, 40, 90, 90, 90, 90, 90, 90])
#p_array1.setAngles([45, 22.5, 40, 35.0, 180, 60, 90, 100, 10])
#p_array1.setAngles([225, 202.5, 220, 215.0, 0, 230, 90, 280, 190])
#p_array1.setAngles([90, 90, 90, 90, 90, 90, 90, 90, 90])
#p_array1.setAngles([ 0, 0, 0, 0, 0, 0, 0, 0, 0])
#p_array1.setAngles([180, 180, 180, 180, 180, 180, 180, 180, 180])
# print("1")
#p_array1.setAngles([ 90, 90 ])
# print("-1")
p_array1.fina()
