import subprocess

mpcmdrun = subprocess.Popen(
    [
        "C:\\Program Files\\Windows Defender\\MpCmdRun.exe",
        "-Scan",
        "-ScanType",
        "3",
        f"-File \"{file}\"",
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
    print("Standard Output:")
    print(stdout)

if stderr:
    print("Standard Error:")
    print(stderr)
