from RestCalls import rest_calls_prod, passwords
import json
import time
from ControlRunExperiment import RunExperiment


token = ""
for x in range(7):
    # returns {"detail":"Invalid token."} or {"detail":"Invalid token header. No credentials provided."} if no or wrong credentials
    # returns KeyError: 'experimentId' if no experiment is in Queue
    task = rest_calls_prod.getexp_fromqueue(
        token)
    # print(task)

    if "detail" not in task:
        print("Credentials are valid")
        # print(task["experimentId"])
        if "experimentId" in task:
            print("There is also a new experiment in the queue")
            print(task)
            experimentId = task["experimentId"]
            print("task id: " + experimentId)
            print("Running")
            rest_calls_prod.poststatus_running(
                token, experimentId)

            # For future: include test of setup/, calibration/validation
            # Here: execute task
            runx = RunExperiment(task, experimentId)
            print("Experiment performed")
            # Here: retrieve result

            # result = json.dumps(runx.results)
            result = json.dumps({
                "experiment": experimentId,
                # "startTime": "2021-12-21T17:16:19.304243Z",
                "totalCounts": 50000,
                "numberOfDetectors": 4,
                "singlePhotonRate": "1500.00",
                "totalTime": 3,
                "experimentData": runx.results
                # {
                #     "countratePerDetector": {
                #         "d1": 123,
                #         "d2": 123,
                #         "d3": 456,
                #         "d4": 123,
                #         "d5": 123,
                #         "d6": 456,
                #         "d7": 123,
                #         "d8": 123
                #     },
                #     "encodedQubitMeasurements": {
                #         "c00": 0.123,
                #         "c01": 0.56,
                #         "c10": 0.123,
                #         "c11": 0.34
                #     }
                # }
            })
            print("Results determined")
            rest_calls_prod.post_result(
                token, result)
            print("Results posted to API")
            rest_calls_prod.poststatus_done(
                token, experimentId)
            print("Status of " + experimentId + " updated")

        else:
            print("Empty queue")
    elif "detail" in task:
        print("Invalid credentials, generating new ...")
        credentials = rest_calls_prod.login(
            passwords.email, passwords.password)
        # print(credentials)
        token = credentials["token"]
        print("New token for you!")
        # print(token)
    else:
        pass
    time.sleep(5)
