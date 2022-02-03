# Powermeter

# 0 for Watts, 1 for dBm
powerUnit = 0

# This parameter specifies the users wavelength in nanometer [nm]
wavelength = 930

# address of the computer where the timetagger is connected
address = '131.130.102.124'

# setupDic is a dictionary with the information of each motor serial number. #
# Each serial number has assigned information regarding its Path, Order, Type and ParametersDic. #
#   Path: Integer that identifies the photons path in which the motor is placed. #
#   Order: Integer identifying the order in which optical elements are placed in the photons' path. #
#   Type: HalfWaveplate, QuarterWaveplate, etc.(?) #
#   CalibrationAngle: Calibration angle of each waveplate #
setupDic = {
    b"11400349": {
        "Path": -4,
        "Order": 1,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 22.962
    },
    b"11400549": {
        "Path": -1,
        "Order": 1,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 44.712
    },
    b"11400172": {
        "Path": -2,
        "Order": 1,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 51.172
    },
    b"11400348": {
        "Path": -3,
        "Order": 1,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 49.143
    },
    b"11400548": {
        "Path": 0,
        "Order": 1,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 68.62
    },  # 'ParametersDic': {'offset': 0.0}},
    b"11400509": {
        "Path": 1,
        "Order": 1,
        "Type": "QuarterWaveplate",
        "CalibrationAngle": 9.8051
    },
    b"11400508": {
        "Path": 1,
        "Order": 2,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 79.7076
    },
    b"11400530": {
        "Path": 2,
        "Order": 1,
        "Type": "QuarterWaveplate",
        "CalibrationAngle": 31.0710
    },
    b"11400338": {
        "Path": 2,
        "Order": 2,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 42.0387
    },
    b"11400556": {
        "Path": 3,
        "Order": 1,
        "Type": "QuarterWaveplate",
        "CalibrationAngle": 97.9512
    },
    b"11400550": {
        "Path": 3,
        "Order": 2,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 33.5602
    },
    b"11400547": {
        "Path": 4,
        "Order": 1,
        "Type": "QuarterWaveplate",
        "CalibrationAngle": 93.44  # + 1
    },
    b"11400466": {
        "Path": 4,
        "Order": 2,
        "Type": "HalfWaveplate",
        "CalibrationAngle": 41.04
    },
}


# ttDic is a dictionary with the information of the time tagger channnel to detector+path+pol mapping
ttDic = {
    1: [1, 0],
    2: [2, 0],
    12: [3, 0],
    13: [4, 0],
    8: [1, 1],
    6: [2, 1],
    5: [3, 1],
    7: [4, 1],
}

# ttDic = {
#     1: [1, 0],
#     2: [2, 0],
#     5: [3, 0],
#     7: [4, 0],
#     6: [1, 1],
#     8: [2, 1],
#     12: [3, 1],
#     13: [4, 1],
# }

computationParam = ["alpha", "beta", "gamma"]
