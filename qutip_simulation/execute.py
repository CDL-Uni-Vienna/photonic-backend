from qutip_simulation.circuits import *
from qutip_simulation.test import test


def execute(circuitId, ComputeSettings):
    """
    angles are retrieved as sting type 'str' and need conversion to float
    """
    id = circuitId
    if id in [12, 13, 14]:
        alpha_str = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
        beta_str = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]

        theta1_str = ComputeSettings["encodedQubitMeasurements"][0]["theta"]
        phi1_str = ComputeSettings["encodedQubitMeasurements"][0]["phi"]
        theta2_str = ComputeSettings["encodedQubitMeasurements"][1]["theta"]
        phi2_str = ComputeSettings["encodedQubitMeasurements"][1]["phi"]

        alpha = float(alpha_str)
        beta = float(beta_str)
        theta1 = float(theta1_str)
        phi1 = float(phi1_str)
        theta2 = float(theta2_str)
        phi2 = float(phi2_str)

        if id == 12:
            res = circuit_12(alpha=alpha, beta=beta, theta1=theta1,
                             phi1=phi1, theta2=theta2, phi2=phi2)
        if id == 13:
            res = circuit_13(alpha=alpha, beta=beta, theta1=theta1,
                             phi1=phi1, theta2=theta2, phi2=phi2)
        if id == 14:
            res = circuit_14(alpha=alpha, beta=beta, theta1=theta1,
                             phi1=phi1, theta2=theta2, phi2=phi2)
        return res
