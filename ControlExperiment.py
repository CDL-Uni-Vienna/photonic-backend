from utilFunc import flatten, thphToPlatesAngles, alphaToPlatesAngles, had_corr
import json
import os
from ControlPlatesArray import PlatesArray


class Experiment:
    """"""

    def __init__(self, expeDic: dict):
        '''
        Initialize an experiment 

        Parameters
        ----------
        expeDic : Dictionary of the experiment
        '''

        self.circuitId = expeDic["circuitId"]
        self.circuitAngles = expeDic["ComputeSettings"]["qubitComputing"]["circuitAngles"]
        self.platesAnglesDic = {}
        self.encodedQubitMeasurements = expeDic["ComputeSettings"]["encodedQubitMeasurements"]
        print('Initializing experiment...\n\tcircuitId: ' + str(self.circuitId))

        d = os.getcwd()
        #d = os.path.join(d, 'photonic-backend', 'CircuitLib','circuits4Dv004.json')
        d = os.path.join(d, 'CircuitLib', 'circuits4Dv004.json')

        with open(d, "r") as read_file:
            self.circuitLib = json.load(read_file)
            self.circuitLib = self.circuitLib[self.circuitId-1]  # Load the lib

    def getPlatesAngles(self):
        '''
        gets the list of angles for each plate from the experiment conf.
        '''
        print('Calculating plates angles...')

        # Cluster state preparation
        self.clusterStatePrepPaths = [0]
        prename = self.circuitLib["csp_preset_settings_name"]
        if prename == "Linear Cluster":
            self.clusterStatePrep = [[22.5]]
        elif prename == "Greenberger–Horne–Zeilinger":
            self.clusterStatePrep = [[0]]
        else:
            print('not recognizible csp_preset_settings_name')

        # Qubit computing angles
        if len(self.circuitAngles) > 0:
            #print( [*map( lambda d: self.circuitLib['circuit_tag2path_dic'][d["circuitAngleName"]], self.circuitAngles)])
            self.circuitAnglesPaths = [
                *map(lambda d: self.circuitLib['circuit_tag2path_dic'][d["circuitAngleName"]], self.circuitAngles)]
            self.circuitAngles = [
                *map(lambda d: d["circuitAngleValue"], self.circuitAngles)]
            if prename == "Linear Cluster":
                self.circuitAngles = [
                    *map(alphaToPlatesAngles, self.circuitAngles)]
            elif prename == "Greenberger–Horne–Zeilinger":
                self.circuitAngles = [
                    *map(alphaToPlatesAngles, self.circuitAngles)]
        else:
            self.circuitAngles = []

        # Qubit measurements
        self.encodedQubitMeasurementsPaths = [
            *map(lambda d: self.circuitLib['circuit_tag2path_dic'][str(d["encodedQubitIndex"])], self.encodedQubitMeasurements)]
        self.encodedQubitMeasurements = [*map(lambda d: [
            d["theta"], d["phi"]
        ], self.encodedQubitMeasurements)]
        self.encodedQubitMeasurements = [
            *map(thphToPlatesAngles, self.encodedQubitMeasurements)]

        # Merging all angles
        self.platesAngles = flatten(flatten([
            self.clusterStatePrep,
            self.circuitAngles,
            self.encodedQubitMeasurements
        ]))

        self.platesAngles = [*map(lambda ang: ang % 360, self.platesAngles)]

        print(self.platesAngles)

        # Loadnig both path and angle info in platesAnglesDic
        for num, pp in enumerate(self.clusterStatePrepPaths):
            self.platesAnglesDic[pp] = self.clusterStatePrep[num]

        for num, pp in enumerate(self.circuitAnglesPaths):
            self.platesAnglesDic[pp] = self.circuitAngles[num]

        for num, pp in enumerate(self.encodedQubitMeasurementsPaths):
            self.platesAnglesDic[pp] = self.encodedQubitMeasurements[num]

        # Hadamard corrections are considered at qubits 1 and 4 for the Linear Cluster L4
        if prename == "Linear Cluster":
            self.platesAnglesDic[1] = had_corr(self.platesAnglesDic[1])
            self.platesAnglesDic[4] = had_corr(self.platesAnglesDic[4])

        print(self.platesAnglesDic)

    def execute(self):
        '''
        Execute the experiment using path information
        '''
        p_array1 = PlatesArray(1)

        p_array1.init()

        for path in range(5):
            p_array1.setPath(path, self.platesAnglesDic[path])

        p_array1.fina()
