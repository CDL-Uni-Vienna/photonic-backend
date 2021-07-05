interpretGateReqDic = {
  'h(qreg_q[0])': ["HalfWaveplate"],
  'rz(pi/2, qreg_q[0])': ["QuarterWaveplate"]
}

def interpretGateReq(str):
    return interpretGateReqDic[str]