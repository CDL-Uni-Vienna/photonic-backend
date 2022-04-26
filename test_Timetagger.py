from ControlTimetagger import Timetagger

tt = Timetagger()

cr = tt.countrate(4, 1)

cc = tt.coincidencerate([[4, 0], [4, 1]])
