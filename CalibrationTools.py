import enum
from Settings.measurement_settings import setupDic, ttDic
from ControlTimetagger import Timetagger
from ControlPlatesArray import PlatesArray
from time import sleep
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utilFunc import quad
from numpy import arange, polyfit, poly1d
from operator import itemgetter
from json import dump, load
import os.path


class Calibration:
    '''
    Class for calibration
    '''

    def __init__(self):
        '''
        Initialize calibration procedure.Connecting to timetagger.

        '''
        msg = 'Calibration.init :: '

        print(msg + 'Initializing Calibration')

        self.tt = Timetagger()

        self.pa = PlatesArray(1)
        self.pa.init()

        for device in self.pa.devices:
            self.pa.setPlate(device[0], device[1], 0)
            sleep(0.2)

    # def measureAroundZero(self, path: int, order: int, detector):

    #     self.measureAround(path, order, detector, 0)

    # Finalize calibration
    def fina(self):

        self.tt.close()

        self.pa.fina()

    def allToZero(self):
        for device in self.pa.devices:
            self.pa.setPlate(device[0], device[1], 0)
            sleep(0.2)

    def minimizeCountsRep(self, plates: list, plates_angles: list, detector: list, rep: int):

        mssg = 'Calibration.minimizeCountsRep :: '

        min_ang_dataDic = {}

        for i in range(rep):
            kk = i
            min_ang_dataDic[kk] = self.minimizeCounts(
                plates, plates_angles, detector)
        print(min_ang_dataDic)

        cal_file = 'Calibration/cal' + str(plates) + '.json'

        if os.path.isfile(cal_file):
            print(mssg + "Loading previous calibration file")
            with open(cal_file, 'r') as json_file:
                old_dataDic = load(json_file)

            updated_data = list(old_dataDic.values()) + \
                list(min_ang_dataDic.values())

            for num, data in enumerate(updated_data):
                min_ang_dataDic[num] = data

        with open(cal_file, 'w') as outfile:
            dump(min_ang_dataDic, outfile)

    def minimizeCounts(self, plates: list, plates_angles: list, detector: list):

        mssg = 'Calibration.minimizeCounts :: '

        if len(plates) != len(plates_angles):
            print(mssg + "# Plates and angles provided must be the same number")
            return None

        for plate in plates:
            if len(plate) != 2:
                print(mssg + "Invalid plate identifier provided " +
                      str(plate) + " (Expected form: [path, order])")
                return None

        if len(plates) == 0:

            print(mssg + "No plates provided")

            return None

        if len(detector) != 2:
            print(mssg + "Invalid detector identifier provided " +
                  str(plate) + " (Expected form: [path, polarization])")
            return None

        det_path, det_pol = detector

        mssg = mssg + "Plates " + str(plates) + ", Detector " + str(detector)

        num_plates = len(plates)

        if num_plates == 1:

            print(mssg + "Minimizing with one plate")

            for num, plate in enumerate(plates):
                min_ang = self.measureAround(
                    plate[0], plate[1], detector, plates_angles[num])
                print(mssg + "Extreme found at " + str(min_ang) + "°")
                return min_ang
        elif num_plates > 1:

            print(mssg + "Minimizing with " + str(num_plates) + " plates")

            for num, plate in enumerate(plates):

                ang = plates_angles[num]

                min_ang = self.measureAround(
                    plate[0], plate[1], detector, ang)
                print(mssg + "Extreme found at " + str(min_ang) + "°")

                correction = min_ang - ang

                print(mssg + "Correcting [" + str(plate) +
                      "] plate by " + str(correction) + "°")
                self.pa.calibration_save(plate[0], plate[1], correction)

    def measureAround(self, path: int, order: int, detector: list, angle: float):
        '''
        Given the preliminary calibration angle of a waveplate (see Seetings) a scan of 10 degrees is done around a given angle while countrates are acquired at specified detector.
        The waveplate to move is identified by the path in which it is and its position given by the order parameter ( 0, 1, ... ).
        The detector from which countrates will be measured is specified by the detector input parameter. It is formated as [ path_id, polarization ]
        After angles vs countrates data is acquired a second order polynomial fit is done to obtain the extremal value

        Parameters
        ----------
        path: The path in which the waveplate to move is located
        order: Answers the question, in which position in the specified path is the waveplate placed? answers are given using index notation 0, 1, ...
        detector: Specify the detector to use for measurement using the notation [path, pol]
        angle: Specify the angle around which the waveplate rotates (+-5 degrees)

        Fixed parameters
        ----------
        radius: search radius used to measure (in angles)
        pointNum: number of points to measure
        '''

        mssg = 'Calibration.measureAround :: Plate ' + \
            str([path, order]) + ', Detector ' + str(detector) + ' '

        self.allToZero()

        pointNum = 32
        stp = 10.0/(pointNum - 1)

        angles_out = []
        countrates_out = []

        for i in range(pointNum):

            print(mssg + "Measuring at angle " +
                  str(i+1) + "/" + str(pointNum))

            angle_out = self.pa.setPlate(path, order, angle - 5 + i*stp)

            countrate_out = self.tt.countrate(detector[0], detector[1])
            countrate_out = countrate_out.tolist()[0]

            angles_out.append(angle_out)
            countrates_out.append(countrate_out)
            # sleep(0.6)
            # print([angle_out, countrate_out])

        tmp_angs = []
        for ang in angles_out:
            if ang > 180:
                tmp_angs.append(ang - 360)
            else:
                tmp_angs.append(ang)

        angles_out = tmp_angs
        # print([angles_out, countrates_out])

        # Plotting
        # Here we can add the type and position of the plate
        title = "Plate " + str([path, order]) + ", Detector " + str(detector)
        plt.title(title)
        plt.xlabel("Plate angle (°)")
        plt.ylabel("Countrate ")  # Here datector identifier needs to be added
        plt.plot(angles_out, countrates_out, "or")  # color="red")

        # Fitting
        fit = polyfit(angles_out, countrates_out, 2)
        cc, bb = itemgetter(0, 1)(fit)
        min_angle = -bb/(2*cc)
        print(min_angle)
        fit = poly1d(fit)

        # define a sequence of inputs between the smallest and largest known inputs
        x_line = arange(min(angles_out), max(angles_out), 1)
        # calculate the output for the range
        y_line = fit(x_line)
        # create a line plot for the mapping function
        plt.plot(x_line, y_line, '--', color='blue')

        # plt.show()
        # plt.savefig("Calibration/temp/" + title + ".svg", format="svg")
        plt.savefig("Calibration/temp/" + title + ".png", format="png")

        plt.clf()

        return min_angle

        def measureInterval(self, path: int, order: int, detector: list, angle_int: list, num_points: int):
            '''
            Given the preliminary calibration angle of a waveplate (see Seetings) a scan along an interval is done while countrates measured are acquired at specified channel.
            The waveplate to move is identified by the path in which it is and its position given by the order parameter ( 0, 1, ... ).
            The channel from which countrates will be measured is specified by the detector input parameter. It is formated as [ path_id, polarization ]

            Parameters
            ----------
            path: The path in which the waveplate to move is located
            order: Answers the question, in which position in the specified path is the waveplate placed? answers are given using index notation 0, 1, ...
            detector: Specify the detector to use for measurement using the notation [path, pol]
            angle_int: Specify the angle interval within which the waveplate rotates [ angle1, angle2]
            num_points: number of points to measure along the specified interval

            Fixed parameters
            ----------
            pointNum: number of points to measure
            '''

            mssg = 'Calibration.measureInterval :: Plate ' + \
                str([path, order]) + ', Detector ' + str(detector) + ' '

            if len(angle_int) != 2:
                print(
                    mssg + ' angle interval (angle_int) must be a list with len=2 (ERROR)')
                return None

            self.allToZero()

            angle1, angle2 = angle_int
            # angle1, angle2 = angle1 % 360, angle2 % 360
            # angle_int_temp = [angle1, angle2]
            # angle_int_temp = angle_int_temp.sort()
            # angle1, angle2 = angle_int_temp
            delta = angle2 - angle1
            stp = delta/(num_points - 1)

            angles_out = []
            countrates_out = []

            for i in range(num_points):

                print(mssg + "Measuring at angle " +
                      str(i+1) + "/" + str(num_points))

                angle_out = self.pa.setPlate(path, order, angle1 + i*stp)

                countrate_out = self.tt.countrate(detector[0], detector[1])
                countrate_out = countrate_out.tolist()[0]

                angles_out.append(angle_out)
                countrates_out.append(countrate_out)

            # Plotting
            # Here we can add the type and position of the plate
            title = "Plate " + str([path, order]) + \
                ", Detector " + str(detector)
            plt.title(title)
            plt.xlabel("Plate angle (°)")
            # Here datector identifier needs to be added
            plt.ylabel("Countrate ")
            plt.plot(angles_out, countrates_out, "or")  # color="red")
            plt.show()
