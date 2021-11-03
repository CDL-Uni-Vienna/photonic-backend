from utilFunc import flatten, thphToPlatesAngles
import json
import os
from ControlPlatesArray import PlatesArray

class Experiment:
    
    def __init__(self, expeDic : dict):
        '''
        Initialize an experiment 

        Parameters
        ----------
        expeDic : Dictionary of the experiment
        '''

        self.circuitId = expeDic["circuitId"]
        self.circuitAngles = expeDic["circuitAngles"]
        self.encodedQubitMeasurements = expeDic["encodedQubitMeasurements"]
        print('Initializing experiment...\n\tcircuitId: ' + str(self.circuitId) )

        d = os.getcwd()
        #d = os.path.join(d, 'photonic-backend', 'CircuitLib','circuits4Dv004.json')
        d = os.path.join(d, 'CircuitLib','circuits4Dv004.json')

        with open(d, "r") as read_file:
            self.circuitLib = json.load(read_file)
            self.circuitLib = self.circuitLib[self.circuitId-1] #Load the lib

    def getPlatesAngles(self):
        '''
        gets the list of angles for each plate from the experiment conf.
        '''
        print('Calculating plates angles...')

        self.firstPlate = {
            "Linear Cluster": 22.5,
            "Greenberger–Horne–Zeilinger": 0
        }[self.circuitLib["csp_preset_settings_name"]]
 
        #Qubit computing angles
        if len(self.circuitAngles)>0:
            #print( [*map( lambda d: self.circuitLib['circuit_tag2path_dic'][d["circuitAngleName"]], self.circuitAngles)])
            self.circuitAnglesPaths = [*map( lambda d: self.circuitLib['circuit_tag2path_dic'][d["circuitAngleName"]], self.circuitAngles)]
            self.circuitAngles = [*map( lambda d: [45 , (180-2*d["circuitAngleValue"])/8], self.circuitAngles)]
        else:
            self.circuitAngles = []

        #Qubit measurements
        self.encodedQubitMeasurementsPaths = [*map( lambda d: self.circuitLib['circuit_tag2path_dic'][str(d["encodedQubitIndex"])], self.encodedQubitMeasurements)]
        self.encodedQubitMeasurements = [*map( lambda d: [ 
            d["theta"],d["phi"]
            ], self.encodedQubitMeasurements)]
        self.encodedQubitMeasurements = [*map( thphToPlatesAngles, self.encodedQubitMeasurements)]

        #Merging all angles
        self.platesAngles = flatten(flatten([
            [[self.firstPlate]],
            self.circuitAngles, 
            self.encodedQubitMeasurements
            ]))

        print(self.platesAngles)

    def rawExecute(self):
        '''
        Execute the experiment aligning the plates in the raw order the experiment dictates
        '''
        p_array1 = PlatesArray(1)

        p_array1.init()

        #Moving the plates to their angles
        p_array1.setAngles(self.platesAngles)

        p_array1.fina()