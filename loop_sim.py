from unittest import result
from RestCalls import rest_calls_prod, passwords
import json
import time
from qutip_simulation.execute import execute


def Mainloop(on_time):

    mssg = 'Mainloop :: '

    print("Main loop will run for " + str(on_time) + " minutes.")

    token = ""

    current_time = time.time()

    end_time = current_time + 60*on_time

    print(end_time)

    ii = 0

    while current_time < end_time:

        ii += 1

        print("Iteration " + str(ii) +
              " (" + str(round((end_time-current_time)/60, 2)) + " minutes left)")

        # returns {"detail":"Invalid token."} or {"detail":"Invalid token header. No credentials provided."} if no or wrong credentials
        # returns KeyError: 'experimentId' if no experiment is in Queue
        task = rest_calls_prod.getexp_fromqueue(
            token)
        # print(task)
        print(task)
        if "detail" not in task:
            print(mssg + "Credentials are valid")
            # print(task["experimentId"])
            if "experimentId" in task:
                print(mssg + "There is also a new experiment in the queue")
                print(mssg + str(task))
                experimentId = task["experimentId"]
                print(mssg + "task id: " + experimentId)
                print(mssg + "Running")
                rest_calls_prod.poststatus_running(
                    token, experimentId)

                # For future: include test of setup/, calibration/validation
                # Here: execute task - pass circuitId and ComputeSettings
                # execute() returns experimental results from circuits
                result = execute(
                    circuitId=task["circuitId"], ComputeSettings=task["ComputeSettings"])

                print(mssg + "Experiment performed")
                print(mssg + str(result))

                result_data = json.dumps({
                    "experiment": experimentId,
                    "totalCounts": 50000,
                    "numberOfDetectors": 4,
                    "singlePhotonRate": "1500.00",
                    "totalTime": 3,
                    "experimentData": {
                        "countratePerDetector": {
                            # simulation with QuTip doesnt know single detector
                            # countrates, thus 1 is filled as placeholder since
                            # fields are validated against positive integer
                            "d1": 1,
                            "d2": 1,
                            "d3": 1,
                            "d4": 1,
                            "d5": 1,
                            "d6": 1,
                            "d7": 1,
                            "d8": 1
                        },
                        "coincidenceCounts": result
                    }
                })
                print(mssg + "Result data determined")
                # POST result_data back to API
                rest_calls_prod.post_result(
                    token, result_data)
                print(mssg + "Results posted to API")
                # update status of experiment
                rest_calls_prod.poststatus_done(
                    token, experimentId)
                print(mssg + "Status of " + experimentId + " updated")

            else:
                print(mssg + "Empty queue")
        elif "detail" in task:
            print(mssg + "Invalid credentials, generating new ...")
            credentials = rest_calls_prod.login(
                passwords.email, passwords.password)
            # print(credentials)
            token = credentials["token"]
            print(mssg + "New token for you!")
            # print(token)
        else:
            pass
        time.sleep(5)

        current_time = time.time()


if __name__ == '__main__':

    Mainloop(10)
