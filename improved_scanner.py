import re
import subprocess
import os
import hashlib
from itertools import zip_longest

def defender_scan(path):
    """
    Scan a file using Windows Defender (MpCmdRun.exe) and return threat information if found.

    Args:
    - path (str): Path to the file to be scanned.

    Returns:
    - tuple: (found (bool), threat (str), path (str))
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f'File not found: {path}')

    exe = r"C:\Program Files\Windows Defender\MpCmdRun.exe"

    cmd = [
        exe,
        "-Scan",
        "-ScanType", "3",
        "-File", f'"{path}"',
        "-DisableRemediation",
        "-Trace",
        "-Level", "0x10"
    ]

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()

        if stdout:
            stdout = stdout.lower()
            if "no threats" in stdout:
                return False, 'Clean', path
            else:
                threat = re.findall(r'\s+threat\s+:\s+(.*)', stdout)[0]
                return True, threat, path

        if stderr:
            print("Standard Error:")
            print(stderr)
            return False, '', path

    except Exception as e:
        print(f"Error scanning {path}: {str(e)}")
        return False, '', path

def split_sample(file_path):
    """
    Split the file into chunks and scan each chunk for threats.

    Args:
    - file_path (str): Path to the file to be split and scanned.
    """
    temp_folder = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

    print('Splitting the sample into 2')
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        first_half_length = round(len(file_content) //2)
        half_split = [file_content[:first_half_length],file_content[first_half_length:]]
        counter = 0
        for part in half_split:
            name= hashlib.md5(part.encode()).hexdigest()
            temp_file_path= temp_folder + str(name)
            with open(temp_file_path,'w') as temp_file:
                temp_file.write(part)
                found, threat,path = defender_scan(temp_file_path)
                if threat:
                    print('Found threat in part' + str(counter+1))
                    part = file

            os.remove(temp_file_path)
            counter += counter

    file.close()
    

def split_to_chunks(data, size):
    """
    Split a string into chunks of specified size.

    Args:
    - data (str): Input string to be split.
    - size (int): Size of each chunk.

    Returns:
    - list: List of string chunks.
    """
    return [data[i:i + size] for i in range(0, len(data), size)]

def scan(file):
    """
    Scan a file for threats using Windows Defender and perform additional actions if threat is found.

    Args:
    - file (str): Path to the file to be scanned.
    """
    found, threat, path = defender_scan(file)
    if found:
        print(f'Threat Found: {threat}')
        print('Splitting and scanning the sample...')
        split_sample(path)

# Example usage:
bad_file = r'F:\\C2\test-sample\\Invoke-Mimikatz.ps1'
good_file = r'F:\\C2\test-sample\\good_file.ps1'

scan(bad_file)
