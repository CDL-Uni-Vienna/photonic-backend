import enum
from Settings.measurement_settings import setupDic, ttDic
from ControlTimetagger import Timetagger
from ControlPlatesArray import PlatesArray
from time import sleep
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utilFunc import flatten, quad
from numpy import arange, polyfit, poly1d
from operator import itemgetter
from json import dump, load
import os.path
from statistics import mean, stdev


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

        self.res = 0.01

        self.allToZero()  # Flag can be added not to do this twice

    def fina(self):

        self.tt.close()

        self.pa.fina()

    def allToZero(self):
        for device in self.pa.devices:
            self.pa.setPlate(device[0], device[1], 0)
            sleep(0.2)

    def tomoSingleDet(self, path: int, pol: int):

        stokes = []

        self.allToZero()

        crt = self.tt.countrate(path, pol)  # H
        stokes.append(crt)

        self.pa.setPlate(path, 1, 45)
        crt = self.tt.countrate(path, pol)  # V
        stokes.append(crt)

        self.pa.setPlate(path, 0, 45)
        self.pa.setPlate(path, 1, 22.5)
        crt = self.tt.countrate(path, pol)  # D
        stokes.append(crt)

        self.pa.setPlate(path, 1, -22.5)
        crt = self.tt.countrate(path, pol)  # A
        stokes.append(crt)

        self.pa.setPlate(path, 1, 0)
        crt = self.tt.countrate(path, pol)  # R
        stokes.append(crt)

        self.pa.setPlate(path, 0, -45)
        crt = self.tt.countrate(path, pol)  # L
        stokes.append(crt)

        stokes = [*map(lambda x: list(x)[0], stokes)]

        print(stokes)

        hh, vv, dd, aa, rr, ll = stokes

        hv = hh + vv
        da = dd + aa
        rl = rr + ll

        if pol == 0:
            stokes = [
                hh/hv,
                vv/hv,
                dd/da,
                aa/da,
                rr/rl,
                ll/rl
            ]
            print(stokes)
            return stokes
        elif pol == 1:
            stokes = [
                vv/hv,
                hh/hv,
                aa/da,
                dd/da,
                ll/rl,
                rr/rl
            ]
            print(stokes)
            return stokes

    def minimizeCounts(self, plates: list, plates_angles: list, detector: list):
        '''
        Minimize countrate of detector using plates at plates_angles

        Parameters
        ----------
        plates: list contatinig lists with two elements representing each plate [path order]
            path: The path in which the waveplate to move is located
            order: Answers the question, in which position in the specified path is the waveplate placed? answers are given using index notation 0, 1, ...
        plates_angles: angles from which to start the iteration
        detector: Specify the detector to use for measurement using the notation [path, pol]

        Fixed parameters
        ----------
        rep: Number of iterations to do until criteria is implemented
        '''

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
            print(mssg + "Invalid detector identifier provided for plate" +
                  str(plate) + " (Expected form: [path, polarization])")
            return None

        det_path, det_pol = detector

        num_plates = len(plates)

        if num_plates == 1:

            mssg = mssg + "Plate " + \
                str(plates[0]) + ", Detector " + str(detector) + " "

            print(
                mssg + "Minimizing with one plate. Iterating extreme location (measureAround).")

            # plates contains contains only one element. Nevertheless using for seems appropiate considering the case when not.
            for num, plate in enumerate(plates):

                plate_path = plate[0]
                plate_order = plate[1]

                # We fit a parabola once to get an idea where the extreme is
                input_angle = plates_angles[num]
                min_ang = self.measureAround(
                    plate_path, plate_order, detector, input_angle)
                min_ang = round(min_ang, 2)
                print(mssg + "Extreme found at first approximation " +
                      str(min_ang) + "°")

                print(plate[0])
                print(plate[1])
                print(detector)
                print([
                    min_ang-0.5, min_ang+0.5])

                result = self.measureInterval(plate[0], plate[1], detector, [
                                              min_ang-0.5, min_ang+0.5], 11)

                angles_out = result[0]
                countrates_out = result[1]

                plt.plot(angles_out, countrates_out, "o")

                plt.show()

                # for ii in range(max_rep):

                #     # The line below works only moving one plate beacuase measureAround has already setted all the others at zero degrees
                #     self.pa.setPlate(plate_path, plate_order, min_ang)

                #     min_crt = self.tt.countrate(det_path, det_pol)

                #     min_crt_list.append(min_crt)

                #     min_ang_mean = mean(min_ang_list)
                #     mean_list.append(min_ang_mean)

                #     if ii > 0:
                #         min_ang_stdv = stdev(min_ang_list)
                #         stdv_list.append(min_ang_stdv)

                #     print(
                #         "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

                #     # If the stdev drops below max_stdv after at least 3 iteratons -> Return calibration angle and its stdev
                #     if ii > 2 and min_ang_stdv < max_stdv:
                #         print(
                #             "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
                #         print(mssg + "Minimum counts angle found at " +
                #               str(min_ang_mean) + "(+-" + str(min_ang_stdv) + ")")

                #         print("AAA")
                #         # Below we plot how the mean angle with minimum countrates changed while we keep iterating
                #         title = "Plate " + \
                #             str([plate_path, plate_order]) + \
                #             ", Detector " + str(detector)
                #         plot_filename = "calM_p" + str(plate_path) + str(plate_order) + \
                #             "_d" + \
                #             str(detector[0]) + str(detector[1]) + \
                #             "_a" + str(int(input_angle))
                #         plt.title(title)
                #         plt.xlabel("Iteration")
                #         plt.ylabel("Angle (°)")
                #         plt.plot(range(1, len(mean_list) + 1), mean_list, "or")
                #         plt.savefig("Calibration/temp/" +
                #                     plot_filename + ".png", format="png")
                #         plt.clf()

        elif num_plates > 1:

            print(mssg + "Minimizing with " + str(num_plates) + " plates")

            mssg = mssg + "Plates " + \
                str(plates) + ", Detector " + str(detector) + " "

            # min_ang_list = []

            # for num, plate in enumerate(plates):

            #     self.pa.calibration_update()

            #     ang = plates_angles[num]

            #     min_ang = self.measureAround(
            #         plate[0], plate[1], detector, ang)
            #     print(mssg + "Extreme found at " + str(min_ang) + "°")

            #     correction = min_ang - ang

            #     print(mssg + "Correcting [" + str(plate) +
            #           "] plate by " + str(correction) + "°")
            #     self.pa.calibration_save(plate[0], plate[1], correction)

            #     min_ang_list.append(min_ang)

            # return min_ang_list

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

        pointNum = 8  # 32
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
        plot_filename = "p" + str(path) + str(order) + \
            "_d" + str(detector[0]) + str(detector[1]) + "_a" + str(int(angle))
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
        plt.savefig("Calibration/temp/" + plot_filename + ".png", format="png")

        plt.clf()

        return min_angle

    def measureInterval(self, path: int, order: int, detectors: list, angle_int: list, num_points: int):

        angles_out_perDet = {}
        countrates_out_perDet = {}

        title = "Plate " + str([path, order]) + ", Detector " + str(detectors)

        # flatten(detectors)

        # + str(detector[0]) + str(detector[1]) + "_a" + str(int(float))
        plot_filename = "p" + str(path) + str(order) + "_"

        plt.title(title)
        plt.xlabel("Plate angle (°)")
        plt.ylabel("Countrate ")

        for detector in detectors:

            plot_filename = plot_filename + "d" + \
                str(detector[0]) + str(detector[1])

            result = self.measureIntervalSingleDet(
                path, order, detector, angle_int, num_points)

            angles_out = result[0]
            countrates_out = result[1]

            plt.plot(angles_out, countrates_out, "o")

            angles_out_perDet[str(detector)] = angles_out
            countrates_out_perDet[str(detector)] = countrates_out

        plot_filename = plot_filename + "_a" + \
            str(angle_int[0]) + "to" + str(angle_int[1])

        plt.savefig("Calibration/temp/" + plot_filename + ".png", format="png")

        plt.clf()

        return angles_out_perDet, countrates_out_perDet

    def measureIntervalSingleDet(self, path: int, order: int, detector: list, angle_int: list, num_points: int):
        '''
        A scan along an interval is done while countrates measured are acquired at specified channel.
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

        return [angles_out, countrates_out]

        # # Plotting
        # # Here we can add the type and position of the plate
        # title = "Plate " + str([path, order]) + \
        #     ", Detector " + str(detector)
        # plt.title(title)
        # plt.xlabel("Plate angle (°)")
        # # Here datector identifier needs to be added
        # plt.ylabel("Countrate ")
        # plt.plot(angles_out, countrates_out, "or")  # color="red")
        # plt.show()
