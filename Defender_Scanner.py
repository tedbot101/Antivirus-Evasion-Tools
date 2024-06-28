import re
import subprocess
import os
import hashlib
 
# encoding GeeksforGeeks using md5 hash
# function 




# doc = https://learn.microsoft.com/en-us/defender-endpoint/command-line-arguments-microsoft-defender-antivirus

def denfender_scan(path):
    if not os.path.exists(path):
        raise Exception(f'No such file: {path}')
    
    exe = "C:\\Program Files\\Windows Defender\\MpCmdRun.exe"
    

    # command_to_execute = exe + " -Scan -ScanType 3 -File '{file}' -DisableRemediation -Trace -Level 0x10"    
    mpcmdrun = subprocess.Popen(
    [
        exe,
        "-Scan",
        "-ScanType",
        "3",
        f"-File",
        '"'+ path +'"',
        "-DisableRemediation",
        "-Trace",
        "-Level",
        "0x10",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    )
    stdout, stderr = mpcmdrun.communicate()
    if stdout:
        stdout = stdout.lower()

        if "no threats" in stdout:
            #print("The file '" + path +"' is clean")
            return

        else:
            threat = re.findall('\sthreat\s+:\s+(.*)', stdout)[0]
            #print(stdout)
            print('Threat: '+threat)
            split_sample(path)
            return threat

    if stderr:
        print("Standard Error:")
        print(stderr)

def split_sample(file_path):

    temp_folder = os.getcwd() + '\\' + 'temp\\'

    if not os.path.exists(temp_folder):
        os.mkdir('temp')

    file = open(file_path,'r')
    file = file.read()
    splited_sample= file.split()
    
    for sample in splited_sample:
        # using md5 to generate random hashes for file name
        name= hashlib.md5(sample.encode()).hexdigest()
        temp_file_path= temp_folder + str(name)
        #print(temp_file)
        with open(temp_file_path,'w') as temp_file:
            temp_file.write(sample)
            #denfender_scan(temp_file_path)
            temp_file.close()
    
    for file_to_delete in os.listdir(temp_folder):
        os.remove(file_to_delete)


denfender_scan('F:\\C2\\test-sample\\Invoke-Mimikatz.ps1')
denfender_scan('F:\\C2\\test-sample\\good_file.ps1')