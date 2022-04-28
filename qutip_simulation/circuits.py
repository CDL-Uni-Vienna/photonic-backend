from urllib import response
from matplotlib.pyplot import thetagrids
from qutip.qip.circuit import QubitCircuit, Gate, CircuitSimulator
from qutip.qip.qasm import read_qasm
from qutip import tensor, basis
from qutip.states import ket2dm
from qutip.measurement import measure, measurement_statistics
from qutip.operators import identity, sigmaz

import math
import cmath


def measure_one(state, theta1, phi1):
    state0 = basis(2, 0)
    state1 = basis(2, 1)

    z1 = complex(0, phi1)

    E1 = (
        math.cos(theta1 / 2) * state0 + cmath.exp(z1) *
        math.sin(theta1 / 2) * state1
    ).unit()
    E1_orth = (
        -math.cos(theta1 / 2) * state1 + cmath.exp(-z1) *
        math.sin(theta1 / 2) * state0
    ).unit()

    Projector0, Projector1 = ket2dm(E1), ket2dm(E1_orth)

    matrix = [Projector0, Projector1]

    results = {"0": 0, "1": 0}

    for _ in range(1000):
        value, new_state = measure(state, matrix)
        print(value)
        if value == 0:
            results["0"] += 1
        elif value == 1:
            results["1"] += 1
        else:
            print("Unexpected error.")

    return results


def measure_two(state, theta1, phi1, theta2, phi2):
    state0 = basis(2, 0)
    state1 = basis(2, 1)

    z1 = complex(0, phi1)

    E1 = (
        math.cos(theta1 / 2) * state0 + cmath.exp(z1) *
        math.sin(theta1 / 2) * state1
    ).unit()
    E1_orth = (
        -math.cos(theta1 / 2) * state1 + cmath.exp(-z1) *
        math.sin(theta1 / 2) * state0
    ).unit()

    z2 = complex(0, phi2)

    E2 = (
        math.cos(theta2 / 2) * state0 + cmath.exp(z2) *
        math.sin(theta2 / 2) * state1
    ).unit()
    E2_orth = (
        -math.cos(theta2 / 2) * state1 + cmath.exp(-z2) *
        math.sin(theta2 / 2) * state0
    ).unit()

    Projector00 = tensor(ket2dm(E1), ket2dm(E2))
    Projector01 = tensor(ket2dm(E1), ket2dm(E2_orth))
    Projector10 = tensor(ket2dm(E1_orth), ket2dm(E2))
    Projector11 = tensor(ket2dm(E1_orth), ket2dm(E2_orth))

    matrix = [Projector00, Projector01, Projector10, Projector11]

    results = {"00": 0, "01": 0, "10": 0, "11": 0}

    for _ in range(1000):
        value, new_state = measure(state, matrix)
        # print(value)
        if value == 0:
            results["00"] += 1
        elif value == 1:
            results["01"] += 1
        elif value == 2:
            results["10"] += 1
        elif value == 3:
            results["11"] += 1
        else:
            print("Unexpected error.")

    return results


def circuit_5(alpha, theta1, phi1):
    qc = QubitCircuit(N=1)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("SNOT", targets=[0])

    init_state = basis(2, 0)
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_one(state=result, theta1=theta1,
                          phi1=phi1)
    return results


def circuit_6(theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("CSIGN", targets=[1], controls=[0])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results


def circuit_7(alpha, beta, theta1, phi1):
    qc = QubitCircuit(N=1)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("RX", targets=[0], arg_value=-beta)

    init_state = basis(2, 0)
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_one(state=result, theta1=theta1,
                          phi1=phi1)
    return results


def circuit_8(alpha, theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("RZ", targets=[1], arg_value=-alpha)
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("CSIGN", targets=[1], controls=[0])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results


def circuit_9(alpha, theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("CSIGN", targets=[1], controls=[0])
    qc.add_gate("RZ", targets=[1], arg_value=-alpha)
    qc.add_gate("SNOT", targets=[1])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results


def circuit_11(alpha, beta, gamma, theta1, phi1):
    qc = QubitCircuit(N=1)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("RX", targets=[0], arg_value=-beta)
    qc.add_gate("RZ", targets=[0], arg_value=-gamma)
    qc.add_gate("SNOT", targets=[0])

    init_state = basis(2, 0)
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_one(state=result, theta1=theta1,
                          phi1=phi1)
    return results


def circuit_12(alpha, beta, theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("CSIGN", targets=[1], controls=[0])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("RZ", targets=[1], arg_value=-beta)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results


def circuit_13(alpha, beta, theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("RZ", targets=[1], arg_value=-beta)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("CSIGN", targets=[1], controls=[0])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results


def circuit_14(alpha, beta, theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("RZ", targets=[1], arg_value=-beta)
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("CSIGN", targets=[1], controls=[0])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("SNOT", targets=[0])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results


def circuit_19(alpha, beta, theta1, phi1, theta2, phi2):
    qc = QubitCircuit(N=2)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("SNOT", targets=[1])
    qc.add_gate("RZ", targets=[0], arg_value=-alpha)
    qc.add_gate("SNOT", targets=[0])
    qc.add_gate("CSIGN", targets=[1], controls=[0])
    qc.add_gate("RZ", targets=[0], arg_value=-beta)
    qc.add_gate("SNOT", targets=[0])

    init_state = tensor(basis(2, 0), basis(2, 0))
    print(init_state)
    result = qc.run(state=init_state)
    print(result)
    results = measure_two(state=result, theta1=theta1,
                          phi1=phi1, theta2=theta2, phi2=phi2)
    return results
