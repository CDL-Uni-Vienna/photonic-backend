interpretGateDic = {
  "h(qreg_q[0])": ["HalfWaveplate"],
  "rz(pi/2, qreg_q[0])": ["HalfWaveplate"]
}

def interpretGate(str):
    return interpretGateDic[str]