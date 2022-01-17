import paramiko
import json
import time
from Settings.remote_settings import ttPcDic


class RemoteExec:
    """"""

    def __init__(self, expeDic: dict, expId: int):
        '''
        Execute a measurement with the timetagger remotely  

        Parameters
        ----------
        expeDic : Dictionary of the experiment
        expId: Id of the experiment run
        '''
        mssg = 'RemoteExec.init :: '

        adr = ttPcDic['address']
        usr = ttPcDic['username']
        psw = ttPcDic['password']

        # SSH connection to timetagger PC using paramiko
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(adr, username=usr, password=psw)

        exp_filename = 'x' + str(expId) + '.json'
        exp_file = ttPcDic['experiment_folder'] + 'x' + str(expId) + '.json'

        res_filename = 'r' + str(expId) + '.json'

        ftp_client = self.client.open_sftp()

        # Loading experiment JSON to timetagger PC
        with ftp_client.open(exp_file, 'w') as outfile:
            json.dump(expeDic, outfile)

        ftp_client.close()

        time.sleep(1)

        # Checking for the result in the timetagger PC
        totaltime = 1  # in minutes
        curtime = time.time()

        timeout = curtime + 60*totaltime

        print(mssg + 'Starting loop at ' + str(curtime) + ' til ' +
              str(timeout) + '( ' + str(totaltime) + ' minutes)')

        iter = 1

        while True:

            print(mssg + 'Iteration: ' + str(iter))
            print(mssg + 'Time: ' + str(time.time()))

            test = 0

            stdin, stdout, stderr = self.client.exec_command(
                'dir .\\Documents\\DEV\\qc-timetagger\\TempResults\\')

            response_list = stdout.readlines()
            response_list = response_list[5:-2]

            response_list = [
                *map(lambda line: line.strip('\r\n').split(), response_list)]
            response_list = [
                *map(lambda line_sp: line_sp[-1], response_list)]
            response_list.remove('.')
            response_list.remove('..')

            print(response_list)

            res_file = ttPcDic['results_folder']

            if response_list.count(res_filename) > 0:
                ftp_client = self.client.open_sftp()
                filetoopen = res_file + res_filename
                with ftp_client.open(filetoopen, 'r') as infile:
                    self.res_json = json.load(infile)
                    print(self.res_json)
                    break

            if test == 5 or time.time() > timeout:
                break

            test = test - 1

            iter = iter + 1

            time.sleep(5)

        # stdin, stdout, stderr = self.client.exec_command(script_cmd)

        # # response_list = stdout.readlines()

        # for line in stdout:
        #     print(line.strip('\n'))

        # error = stderr.readlines()

        # print(error)

        # print(stdout)
