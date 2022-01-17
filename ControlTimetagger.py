from Settings.measurement_settings import ttDic, computationParam
from TimeTagger import createTimeTagger, Countrate, Coincidences, CoincidenceTimestamp
# from utilFunc import flatten
# import numpy as np
# import Settings.com_settings as com_settings
# import time


class Timetagger:
    '''
    Class for high level operations on an array of waveplates
    '''

    def __init__(self):
        '''
        Initializes the PlatesArray class

        Parameters
        ----------
        tt:     timetagger
        '''
        self.tt = createTimeTagger()
        self.channels = [*ttDic]
        self.ttDicInv = {str(v): k for k, v in ttDic.items()}

    def countrates(self):

        mssg = 'Timetagger.countrates :: '

        ctr = Countrate(self.tt, self.channels)

        ctr.startFor(int(1e12))
        ctr.waitUntilFinished()
        ctrData = ctr.getData()
        detId = [*map(ttDic.get, self.channels)]

        self.ctrDataDic = {str(detId[i]): ctrData[i]
                           for i in range(len(detId))}

        print(mssg + "Countrates: " + str(ctrData))

        return ctrData

    def circuitOutput(self, circuitDic: dict):

        mssg = 'Timetagger.circuitOutput :: '

        self.compQubitNum = circuitDic.get("qc_encoded_qubits")
        self.compFreeParamNum = circuitDic.get("qc_free_param")

        encodedQubitPaths = []
        computationPaths = []

        ccChannelList = []

        for i in range(self.compQubitNum):
            encodedQubitPaths.append(circuitDic.get(
                "circuit_tag2path_dic").get(str(i+1)))

        for i in range(2**self.compQubitNum):

            pathEventList = []

            eventTypeList = [int(x) for x in bin(i)[2:]]
            for i in range(self.compQubitNum-len(eventTypeList)):
                eventTypeList.insert(0, 0)

            for num, event in enumerate(eventTypeList):
                pathEvent = [encodedQubitPaths[num], event]
                pathEventList.append(self.ttDicInv.get(str(pathEvent)))

            ccChannelList.append(pathEventList)

        print(mssg + "Channels for encoded measurements: " + str(ccChannelList))

        for i in range(self.compFreeParamNum):
            computationPaths.append(circuitDic.get(
                "circuit_tag2path_dic").get(computationParam[i]))

        ccChannelList = list(
            map(lambda x: [*x, *computationPaths], ccChannelList))

        print(mssg + "Recording coincidences between channels: " + str(ccChannelList))

        coinc = Coincidences(self.tt, ccChannelList, coincidenceWindow=10000,
                             timestamp=CoincidenceTimestamp.ListedFirst)
        coinc_chans = coinc.getChannels()

        rate = Countrate(self.tt, coinc_chans)
        rate.startFor(int(1e12), clear=True)
        rate.waitUntilFinished()

        compData = rate.getData()

        print(mssg + "Coincidences count rate:" + str(compData))
