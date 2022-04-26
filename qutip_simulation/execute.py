from circuits import *


def execute(circuitId, ComputeSettings):
    id = circuitId
    if id in [12, 13, 14]:
        alpha = ComputeSettings["qubitComputing"]["circuitAngles"][0]["circuitAngleValue"]
        beta = ComputeSettings["qubitComputing"]["circuitAngles"][1]["circuitAngleValue"]
        theta1 = ComputeSettings["qubitComputing"]["encodedQubitMeasurements"][0]["theta"]
        phi1 = ComputeSettings["qubitComputing"]["encodedQubitMeasurements"][0]["phi"]
        theta2 = ComputeSettings["qubitComputing"]["encodedQubitMeasurements"][1]["theta"]
        phi2 = ComputeSettings["qubitComputing"]["encodedQubitMeasurements"][1]["phi"]
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
