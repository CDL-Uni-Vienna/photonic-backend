from ControlTimetagger import Timetagger
from utilFunc import flatten, thphToPlatesAngles, alphaToPlatesAngles, had_corr
import json
import os
from ControlPlatesArray import PlatesArray


class Experiment:
    '''
    Class for controlling all waveplates according to the experiment dictonary requirements.
    '''

    def __init__(self, expeDic: dict):
        '''
        Initialize an experiment 

        Parameters
        ----------
        expeDic : Dictionary of the experiment
        '''
        mssg = 'Experiment.init :: '

        self.circuitId = expeDic["circuitId"]
        self.circuitAngles = expeDic["ComputeSettings"]["qubitComputing"]["circuitAngles"]
        self.platesAnglesDic = {}
        self.encodedQubitMeasurements = expeDic["ComputeSettings"]["encodedQubitMeasurements"]
        print(mssg + 'Initializing experiment with circuitId: ' + str(self.circuitId))

        d = os.getcwd()
        #d = os.path.join(d, 'photonic-backend', 'CircuitLib','circuits4Dv004.json')
        d = os.path.join(d, 'CircuitLib', 'circuits4Dv004.json')

        with open(d, "r") as read_file:
            self.circuitLib = json.load(read_file)
            # Load the lib. TODO: remove position usage to find circuitLib entry
            self.circuitLib = self.circuitLib[self.circuitId-1]
            print(mssg + "Circuit library (circuitLib) entry identified:")
            print(self.circuitLib)

    def getPlatesAngles(self):
        '''
        gets the list of angles for each plate from the experiment conf.
        '''
        mssg = 'Experiment.getPlatesAngles :: '

        print(mssg + 'Calculating plates angles...')

        # Cluster state preparation
        self.clusterStatePrepPaths = [0]

        prename = self.circuitLib["csp_preset_settings_name"]

        print(mssg + 'Preparing ' + prename + ' state')

        if prename == "Linear Cluster":
            self.clusterStatePrep = [[22.5]]
        # "Greenberger–Horne–Zeilinger":
        elif prename == 'Greenbergerâ€“Horneâ€“Zeilinger':
            self.clusterStatePrep = [[0]]
        else:
            print('not recognizible csp_preset_settings_name')

        # Qubit computing angles
        if len(self.circuitAngles) > 0:

            self.circuitAnglesPaths = [
                *map(lambda d: self.circuitLib['circuit_tag2path_dic'][d["circuitAngleName"]], self.circuitAngles)
            ]
            # print(mssg + "Optical paths to be used for rotations: " +
            #      str(self.circuitAnglesPaths))

            self.circuitAngles = [
                *map(lambda d: d["circuitAngleValue"], self.circuitAngles)
            ]
            print(mssg + 'Calculating waveplates angles to implement encoded circuit ' +
                  str(self.circuitId) + ' with rotation(s) parameters: ' + str(self.circuitAngles))

            print(mssg + "Optical paths to be used for rotations: " +
                  str(self.circuitAnglesPaths))

            if prename == "Linear Cluster":
                self.circuitAngles = [
                    *map(alphaToPlatesAngles, self.circuitAngles)
                ]
                print(mssg + "Raw waveplates angles for rotation(s): " +
                      str(self.circuitAngles))
            # "Greenberger–Horne–Zeilinger":
            elif prename == 'Greenbergerâ€“Horneâ€“Zeilinger':
                self.circuitAngles = [
                    *map(alphaToPlatesAngles, self.circuitAngles)
                ]
                print(mssg + "Raw waveplates angles for rotation(s): " +
                      str(self.circuitAngles))
        else:

            self.circuitAngles = []

        # Qubit measurements
        self.encodedQubitMeasurementsPaths = [
            *map(lambda d: self.circuitLib['circuit_tag2path_dic'][str(d["encodedQubitIndex"])], self.encodedQubitMeasurements)
        ]
        print(mssg + "Optical paths to be used for qubit measurements: " +
              str(self.encodedQubitMeasurementsPaths))

        self.encodedQubitMeasurements = [
            *map(lambda d: [
                d["theta"], d["phi"]
            ], self.encodedQubitMeasurements)
        ]
        print(mssg + "Qubit measurements parameters theta, phi: " +
              str(self.encodedQubitMeasurements))

        self.encodedQubitMeasurements = [
            *map(thphToPlatesAngles, self.encodedQubitMeasurements)]
        print(mssg + "Qubit measurements waveplates angles: " +
              str(self.encodedQubitMeasurements))

        # Loading both path and angle info in platesAnglesDic
        # Notice the Paths sufix at variables. It denotes a relation between the paths and angles variables (angles grouped by module)
        for num, pp in enumerate(self.clusterStatePrepPaths):
            self.platesAnglesDic[pp] = self.clusterStatePrep[num]

        # circuitAnglesPaths contains the information of which free rotation parameter of the encoded circuit corresponds to which physical qubit path.
        # If there are no rotations done using the one-way model, i.e. all physical qubits are encoded ones then circuitAnglesPahts = []
        if len(self.circuitAngles) > 0:
            for num, pp in enumerate(self.circuitAnglesPaths):
                self.platesAnglesDic[pp] = self.circuitAngles[num]

        for num, pp in enumerate(self.encodedQubitMeasurementsPaths):
            self.platesAnglesDic[pp] = self.encodedQubitMeasurements[num]

        dimension = self.circuitLib["csp_number_of_qubits"]
        # If a new cluster state is added, an update is needed here (below)
        if dimension == 3:
            self.platesAnglesDic[4] = [0.0, 0.0]
        elif dimension == 2:
            self.platesAnglesDic[3] = [0.0, 0.0]
            self.platesAnglesDic[4] = [0.0, 0.0]

        # Hadamard corrections are considered at qubits 1 and 4 for the Linear Cluster L4
        if prename == "Linear Cluster":
            print(
                mssg + "Absorbing H gate for qubits 1 and 4 needed for L4 cluster state.")
            self.platesAnglesDic[1] = had_corr(self.platesAnglesDic[1])
            self.platesAnglesDic[4] = had_corr(self.platesAnglesDic[4])

        print(mssg + "Full experiment plates angles dictionary: " +
              str(self.platesAnglesDic))

    def setPlatesAngles(self):
        '''
        move the plates to the angles calculated in getPlatesAngles
        '''
        mssg = 'Experiment.setPlatesAngles :: '
        print(mssg + 'using platesAnglesDic (loaded with getPlatesAngles) to set waveplates angles')

        p_array1 = PlatesArray(1)

        p_array1.init()

        for path in range(5):
            print(mssg + 'Setting up path ' + str(path) +
                  ' at angles ' + str(self.platesAnglesDic[path]))
            p_array1.setPath(path, self.platesAnglesDic[path])

        p_array1.fina()
        print(mssg + 'Done. All waveplates aligned.')
