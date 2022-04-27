from qutip_simulation.circuits import *


def execute(circuitId, ComputeSettings):
    """
    angles are retrieved as sting type 'str' and need conversion to float
    """
    id = circuitId
    # if circuit encodes 1 logical qubit we always retrieve
    # theta1, phi1
    if id in [5, 7, 11]:
        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta1 = float(theta1_str)
        phi1 = float(phi1_str)

        if id == 5:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            alpha = float(alpha_str)
            res = circuit_5(alpha=alpha, theta1=theta1,
                            phi1=phi1, theta2=theta2, phi2=phi2)

        if id == 7:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
            alpha = float(alpha_str)
            beta = float(beta_str)
            res = circuit_7(alpha=alpha, beta=beta, theta1=theta1,
                            phi1=phi1, theta2=theta2, phi2=phi2)

        if id == 11:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
            gamma_str = ComputeSettings["qubitComputing"]["circuitAngles"][2]["circuitAngleValue"]
            alpha = float(alpha_str)
            beta = float(beta_str)
            gamma = float(gamma_str)
            res = circuit_11(alpha=alpha, beta=beta, gamma=gamma, theta1=theta1,
                             phi1=phi1, theta2=theta2, phi2=phi2)

    # if circuit encodes 2 logical qubits we always retrieve
    # theta1, phi1, theta2, phi2
    if id in [6, 8, 9, 12, 13, 14, 19]:
        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta2_str = ComputeSettings["encodedQubitMeasurements"][1]["theta"]
        phi2_str = ComputeSettings["encodedQubitMeasurements"][1]["phi"]
        theta1 = float(theta1_str)
        phi1 = float(phi1_str)
        theta2 = float(theta2_str)
        phi2 = float(phi2_str)

        if id == 6:
            res = circuit_6(theta1=theta1,
                            phi1=phi1, theta2=theta2, phi2=phi2)

        if id in [8, 9]:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            alpha = float(alpha_str)

            if id == 8:
                res = circuit_8(alpha=alpha, theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2)
            if id == 9:
                res = circuit_9(alpha=alpha, theta1=theta1,
                                phi1=phi1, theta2=theta2, phi2=phi2)

        if id in [12, 13, 14, 19]:
            alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
            beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
            alpha = float(alpha_str)
            beta = float(beta_str)

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
    return res
