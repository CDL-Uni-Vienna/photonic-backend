# Powermeter

# 0 for Watts, 1 for dBm
powerUnit = 0

# This parameter specifies the users wavelength in nanometer [nm]
wavelength = 930

# setupDic is a dictionary with the information of each motor serial number. #
# Each serial number has assigned information regarding its Path, Order, Type and ParametersDic. #
#   Path: Integer that identifies the photons path in which the motor is placed. #
#   Order: Integer identifying the order in which optical elements are placed in the photons' path. #
#   Type: HalfWaveplate, QuarterWaveplate, etc.(?) #
#   ParametersDic: Dictionary containing parameter assoiated to each type of device e.g. offset #
setupDic = {
    b'11400548': {'Path': 0, 'Order': 1, 'Type': 'HalfWaveplate', 'CalibrationAngle': 0.0},#'ParametersDic': {'offset': 0.0}},
    b'11400509': {'Path': 1, 'Order': 1, 'Type': 'QuarterWaveplate', 'CalibrationAngle': 0.0},
    b'11400508': {'Path': 1, 'Order': 2, 'Type': 'HalfWaveplate', 'CalibrationAngle': 0.0},
    b'11400530': {'Path': 2, 'Order': 1, 'Type': 'QuarterWaveplate', 'CalibrationAngle': 0.},
    b'11400338': {'Path': 2, 'Order': 2, 'Type': 'HalfWaveplate', 'CalibrationAngle': 0.0},
    b'11400556': {'Path': 3, 'Order': 1, 'Type': 'QuarterWaveplate', 'CalibrationAngle': 0.0},
    b'11400550': {'Path': 3, 'Order': 2, 'Type': 'HalfWaveplate', 'CalibrationAngle': 0.0},
    b'11400547': {'Path': 4, 'Order': 1, 'Type': 'QuarterWaveplate', 'CalibrationAngle': 0.0},
    b'11400466': {'Path': 4, 'Order': 2, 'Type': 'HalfWaveplate', 'CalibrationAngle': 0.0}
}

# ttDic is a dictionary with the information of the time tagger channnel to detector+path+pol mapping
ttDic = {
    1: [1, 0],
    2: [2, 0],
    5: [3, 0],
    7: [4, 0],
    10: [1, 1],
    11: [2, 1],
    12: [3, 1],
    13: [4, 1]
}

computationParam = ["alpha", "beta", "gamma"]
