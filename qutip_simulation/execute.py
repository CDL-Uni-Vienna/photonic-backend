from qutip_simulation.circuits import *
import numpy as np


def execute(circuitId, ComputeSettings):
    """
    Function parameters: 

        circuitId, ComputeSettings


        circuitId: 

            positive integer, identifying the circuit to be executed


        ComputeSettings: 

            JSON dict containing all relevant parameters for computation and
            (see ComputeSettings model in API specs 
            https://github.com/zilkf92/cdl-django-webservice/blob/master/cdl_rest_api/models.py)
            for details)

            All angles are retrieved as sting type 'str' and need conversion to float
    """

    id = circuitId

    # if circuit encodes 1 logical qubit we always retrieve
    # theta1, phi1
    if id in [5, 7, 11]:
        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta1 = float(theta1_str)*2*np.pi/360
        phi1 = float(phi1_str)*2*np.pi/360

        if id == 5:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            alpha = float(alpha_str)*2*np.pi/360
            res = circuit_5(alpha=alpha, theta1=theta1,
                            phi1=phi1)

        if id == 7:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
            alpha = float(alpha_str)*2*np.pi/360
            beta = float(beta_str)*2*np.pi/360
            res = circuit_7(alpha=alpha, beta=beta, theta1=theta1,
                            phi1=phi1)

        if id == 11:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
            gamma_str = ComputeSettings["qubitComputing"]["circuitAngles"][2]["circuitAngleValue"]
            alpha = float(alpha_str)*2*np.pi/360
            beta = float(beta_str)*2*np.pi/360
            gamma = float(gamma_str)*2*np.pi/360
            res = circuit_11(alpha=alpha, beta=beta, gamma=gamma, theta1=theta1,
                             phi1=phi1)

    # if circuit encodes 2 logical qubits we always retrieve
    # theta1, phi1, theta2, phi2
    if id in [2, 6, 8, 9, 12, 13, 14, 19]:
        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta2_str = ComputeSettings["encodedQubitMeasurements"][1]["theta"]
        phi2_str = ComputeSettings["encodedQubitMeasurements"][1]["phi"]
        theta1 = float(theta1_str)*2*np.pi/360
        phi1 = float(phi1_str)*2*np.pi/360
        theta2 = float(theta2_str)*2*np.pi/360
        phi2 = float(phi2_str)*2*np.pi/360

        if id in [2, 6]:

            if id == 2:
                res = circuit_2(theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2)

            if id == 6:
                res = circuit_6(theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2)

        if id in [8, 9]:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            alpha = float(alpha_str)*2*np.pi/360

            if id == 8:
                res = circuit_8(alpha=alpha, theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2)

            if id == 9:
                res = circuit_9(alpha=alpha, theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2)

        if id in [12, 13, 14, 19]:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
            alpha = float(alpha_str)*2*np.pi/360
            beta = float(beta_str)*2*np.pi/360

            if id == 12:
                res = circuit_12(alpha=alpha, beta=beta, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2)

            if id == 13:
                res = circuit_13(alpha=alpha, beta=beta, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2)

            if id == 14:
                res = circuit_14(alpha=alpha, beta=beta, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2)

            if id == 19:
                res = circuit_19(alpha=alpha, beta=beta, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2)

    # if circuit encodes 3 logical qubits we always retrieve
    # theta1, phi1, theta2, phi2, theta3, phi3
    if id in [3, 10, 15, 16, 17, 20, 21]:
        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta2_str = ComputeSettings["encodedQubitMeasurements"][1]["theta"]
        phi2_str = ComputeSettings["encodedQubitMeasurements"][1]["phi"]
        theta3_str = ComputeSettings["encodedQubitMeasurements"][2]["theta"]
        phi3_str = ComputeSettings["encodedQubitMeasurements"][2]["phi"]
        theta1 = float(theta1_str)*2*np.pi/360
        phi1 = float(phi1_str)*2*np.pi/360
        theta2 = float(theta2_str)*2*np.pi/360
        phi2 = float(phi2_str)*2*np.pi/360
        theta3 = float(theta3_str)*2*np.pi/360
        phi3 = float(phi3_str)*2*np.pi/360

        if id in [3, 10]:

            if id == 3:
                res = circuit_3(theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

            if id == 10:
                res = circuit_10(theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

        if id in [15, 16, 17, 20, 21]:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            alpha = float(alpha_str)*2*np.pi/360

            if id == 15:
                res = circuit_15(alpha=alpha, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

            if id == 16:
                res = circuit_16(alpha=alpha, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

            if id == 17:
                res = circuit_17(alpha=alpha, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

            if id == 20:
                res = circuit_20(alpha=alpha, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

            if id == 21:
                res = circuit_21(alpha=alpha, theta1=theta1,
                                 phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3)

    # if circuit encodes 4 logical qubits we always retrieve
    # theta1, phi1, theta2, phi2, theta3, phi3, theta4, phi4
    if id in [4, 18, 22]:
        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta2_str = ComputeSettings["encodedQubitMeasurements"][1]["theta"]
        phi2_str = ComputeSettings["encodedQubitMeasurements"][1]["phi"]
        theta3_str = ComputeSettings["encodedQubitMeasurements"][2]["theta"]
        phi3_str = ComputeSettings["encodedQubitMeasurements"][2]["phi"]
        theta4_str = ComputeSettings["encodedQubitMeasurements"][3]["theta"]
        phi4_str = ComputeSettings["encodedQubitMeasurements"][3]["phi"]
        theta1 = float(theta1_str)*2*np.pi/360
        phi1 = float(phi1_str)*2*np.pi/360
        theta2 = float(theta2_str)*2*np.pi/360
        phi2 = float(phi2_str)*2*np.pi/360
        theta3 = float(theta3_str)*2*np.pi/360
        phi3 = float(phi3_str)*2*np.pi/360
        theta4 = float(theta4_str)*2*np.pi/360
        phi4 = float(phi4_str)*2*np.pi/360

        if id == 4:
            res = circuit_4(theta1=theta1,
                            phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3, theta4=theta4, phi4=phi4)

        if id == 18:
            res = circuit_18(theta1=theta1,
                             phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3, theta4=theta4, phi4=phi4)

        if id == 22:
            res = circuit_22(theta1=theta1,
                             phi1=phi1, theta2=theta2, phi2=phi2, theta3=theta3, phi3=phi3, theta4=theta4, phi4=phi4)

    return res
