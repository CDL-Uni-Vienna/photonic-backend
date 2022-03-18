from ControlExperiment import Experiment
from ControlRemoteExec import RemoteExec
from utilFunc import formatDic


class RunExperiment:
    '''
    Class for running the full experiment.
    This imples:
        Setting waveplates using Experiment class
        Sending the instruction to the timetagger PC to measure coincidences
        Retrieve the result
    '''

    def __init__(self, expeDicI: dict, expId):
        '''
        Initialize an experiment 

        Parameters
        ----------
        expeDic : Dictionary of the experiment

        '''

        mssg = 'Experiment.RunExperiment :: '

        print(mssg + "Preparing to implement experiment with circuit ID: " + str(expId))
        expeDic = formatDic(expeDicI)

        self.exp = Experiment(expeDic)
        print(mssg + "Experiment initialized.")

        # getPlatesAngles calculates the angles to set the waveplates as a funtion of the circuit and measurement paramenters
        self.exp.getPlatesAngles()

        # setPlatesAngles rotates each waveplate to its corresponding angle
        self.exp.setPlatesAngles()
        print(mssg + "Experiment hardware on place. Ready to measure coincidences.")

        self.rex = RemoteExec(expeDic, expId)
        print(mssg + "Remote execution completed. Timetagger results retried.")

        self.results = self.rex.res_json
        print(mssg + 'Experiment results:')
        print(self.results)
