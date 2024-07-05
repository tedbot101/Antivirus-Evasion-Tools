import re
import subprocess
import os
import hashlib
from itertools import zip_longest
import concurrent.futures
 
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
            return False,'Clean',''

        else:
            threat = re.findall('\sthreat\s+:\s+(.*)', stdout)[0]
            #print(stdout)
            #print('Threat: '+threat)
            #split_sample(path)
            return True,threat,path

    if stderr:
        print("Standard Error:")
        print(stderr)

def split_sample(file_path):

    temp_folder = os.getcwd() + '\\' + 'temp\\'

    if not os.path.exists(temp_folder):
        os.mkdir('temp')

    file = open(file_path,'r')
    file = file.read()
    
    first_half_length = round(len(file) //2)
    print( first_half_length)
    # to save time splitting the file into 2 and scan the malicious part
    half_split = [file[:first_half_length],file[first_half_length:]]
    for part in half_split:
        name= hashlib.md5(part.encode()).hexdigest()
        temp_file_path= temp_folder + str(name)
        with open(temp_file_path,'w') as temp_file:
            temp_file.write(part)
            found, threat,path = denfender_scan(temp_file_path)
            if threat:
                print('Found threat in part' + half_split.index(part))
                part = file
                break

    # split the part into 2 again
    second_half_length = round(len(file) //2)
    half_split = [file[:second_half_length ],file[second_half_length:]]
    for part in half_split:
        name= hashlib.md5(part.encode()).hexdigest()
        temp_file_path= temp_folder + str(name)
        found, threat,path = denfender_scan(temp_file_path)
        if threat:
            part = file
            break

    # splitting the sample into 64 char size
    splited_sample = split_to_chunck(file,64)


    print(len(splited_sample))
    try:
        for sample in splited_sample:
            # using md5 to generate random hashes for file name
            name= hashlib.md5(sample.encode()).hexdigest()
            temp_file_path= temp_folder + str(name)
            #print(temp_file)
            with open(temp_file_path,'w') as temp_file:
                temp_file.write(sample)
                found, threat,path = denfender_scan(temp_file_path)
                if found:
                    print('Threat : ' + threat)
                    #print('Detected btyes : ' + sample)

                temp_file.close()
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            else:
                continue

    except Exception as err:
        print(err)

def fun(n, i, value=None):
    # size is chunk size
    # https://pythonguides.com/split-a-string-at-every-nth-character-in-python/
    args = [iter(i)] * n
    return zip_longest(fillvalue=value, *args)

def split_to_chunck(data,size):
    op_str = [''.join(l) for l in fun(size, data, '')]
    op = []
    for a in op_str:
        op.append(a)
    return op

def scan(file):
    found,threat,path=denfender_scan(file)
    if found:
        print('Threat Found : ' + threat)
        print('Spliting and scanning the sample...')
        split_sample(path)
    
bad_file='F:\\C2\\test-sample\\Invoke-Mimikatz.ps1'
bad_file='F:\\C2\\test-sample\\bad.ps1'
good_file='F:\\C2\\test-sample\\good_file.ps1'

scan(bad_file)
