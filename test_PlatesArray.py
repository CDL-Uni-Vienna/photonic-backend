from ControlPlatesArray import PlatesArray

# from quiskit syntaxis we need to extract the gates applied #
blueprint_example = ['h(qreg_q[0])', 'rz(pi, qreg_q[0])']

p_array1 = PlatesArray(1)

p_array1.init()

print('av')
p_array1.setAngles([22.5, 0.0])
print('ap')

p_array1.fina()


'''
# Open serial ports #
p_array1.init

# From the gates we should use a function feasibility_test to check that the gates can be implemented #
# An interpreter function should be used returning the angles for each waveplate #
# for two plates, Q and H the example results in #
# in angles [22.5, 0.0] #
if p_array1.feasibilityQ(blueprint_example):
    p_array1.set(blueprint_example)  # set plates at corresponding angles #
    # p_array1.setNmeasurePow(blueprint_example) # # set plates, then measure with powermeter#
    # p_array1.setNmeasureAPD(blueprint_example) # # set plates, then measure with APDs#
    # p_array1.setNmeasurePow_sequence(blueprint_example) # # set plates, then powermeter meas. (sequence) #
    # p_array1.setNmeasureAPD_sequence(blueprint_example) # # set plates, then APD measurement (sequence) #
else:
    print('Error :: blueprints for plates array not feasible to implement')

'''