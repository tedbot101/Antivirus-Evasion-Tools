# var mpcmdrun = new ProcessStartInfo(@"C:\Program Files\Windows Defender\MpCmdRun.exe")
#         {
#             Arguments=$"-Scan -ScanType 3 -File \"{file}\" -DisableRemediation -Trace -Level 0x10",
#             CreateNoWindow = true,
#             ErrorDialog = false,
#             UseShellExecute = false,
#             RedirectStandardOutput = true,
#             WindowStyle = ProcessWindowStyle.Hidden
#         };
# public enum ScanResult
# {
#     [Description("No threat found")]
#     NoThreatFound,
#     [Description("Threat found")]
#     ThreatFound,
#     [Description("The file could not be found")]
#     FileNotFound,
#     [Description("Timeout")]
#     Timeout,
#     [Description("Error")]
#     Error
# }
import re
import subprocess
import os

def denfender_scan(file):
    if not os.path.exists(file):
        raise Exception(f'No such file: {file}')
    
    exe = "C:\\Program Files\\Windows Defender\\MpCmdRun.exe"
    # command_to_execute = exe + " -Scan -ScanType 3 -File '{file}' -DisableRemediation -Trace -Level 0x10"
    # run = subprocess.run(command_to_execute, capture_output=True)


    mpcmdrun = subprocess.Popen(
    [
        exe,
        "-Scan",
        "-ScanType",
        "3",
        f"-File",
        '"'+file+'"',
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
             print("The file '" +file+"' is clean")

        else:
            threat = re.findall('\sthreat\s+:\s+(.*)', stdout)[0]
            #print(stdout)
            print('Threat: '+threat)

    if stderr:
        print("Standard Error:")
        print(stderr)

denfender_scan('F:\\C2\\test-sample\\Invoke-Mimikatz.ps1')
denfender_scan('F:\\C2\\test-sample\\good_file.ps1')