from ControlExperiment import Experiment
from ControlRemoteExec import RemoteExec
from utilFunc import formatDic


class RunExperiment:
    """"""

    def __init__(self, expeDicI: dict, expId):
        '''
        Initialize an experiment 

        Parameters
        ----------
        expeDic : Dictionary of the experiment

        '''

        expeDic = formatDic(expeDicI)

        self.exp = Experiment(expeDic)

        # getPlatesAngles calculates the angles to set the waveplates as a funtion of the circuit and measurement paramenters
        self.exp.getPlatesAngles()

        print("--------------------------------------------------A")
        # setPlatesAngles rotates each waveplate to its corresponding angle
        self.exp.setPlatesAngles()
        print("--------------------------------------------------B")

        self.rex = RemoteExec(expeDic, expId)
        print("--------------------------------------------------C")
        self.results = self.rex.res_json
        print(self.results)
