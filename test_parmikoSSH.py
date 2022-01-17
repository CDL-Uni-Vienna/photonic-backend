import paramiko
import json

dicty = {
    '1': 'AA'
}

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('131.130.102.124',
               username='cd lab 3', password='6582')


# ftp_client = client.open_sftp()
# filetoopen = 'C:\\Users\\CD LAB 3\\Documents\\DEV\\qc-timetagger\\TempExperiments\\' + 'testX.json'
# with ftp_client.open(filetoopen, 'w') as outfile:
#     json.dump(dicty, outfile)


stdin, stdout, stderr = client.exec_command(
    #    '& C:\\Users\\CD LAB 3\\AppData\\Local\\Microsoft\\WindowsApps\\python3.7.exe C:\\Users\\CD LAB 3\\Documents\\DEV\\qc-timetagger\\experimentMeasurement.py \"x1234567.json\"')
    #    '& C:\\Users\\CD LAB 3\\AppData\\Local\\Microsoft\\WindowsApps\\python3.7.exe --version')
    #    '\"C:\\Users\\CD LAB 3\\AppData\\Local\\Microsoft\\WindowsApps\\python3.7.exe\" --version')
    'python3.7.exe --version')
#    'python --version')
#    'dir .\\Documents\\DEV\\qc-timetagger\\TempResults\\')

for line in stdout:
    print(line.strip('\n'))

print(stderr.readlines())


# response_list = stdout.readlines()
# response_list = response_list[5:-2]

# response_list = [
#     *map(lambda line: line.strip('\r\n').split(), response_list)]
# response_list = [
#     *map(lambda line_sp: line_sp[-1], response_list)]

# print(response_list)


# print(stdout)

# filepath = "C:\\Users\\CD LAB 3\\Documents\\DEV\\qc-timetagger\\CircuitLib\\circuits4Dv004.json"
# localpath = "C:\\Users\\CD LAB 2\\Documents\\DEV\\photonic-backend\\CircuitLib\\circuits4Dv004.json"

# ftp_client = client.open_sftp()
# ftp_client.put(localpath, filepath)
# ftp_client.close()

client.close()
