import subprocess
import wmi

def WMIProcessCreation(name):
    # Menggunakan modul wmi untuk membuat proses menggunakan Windows Management Instrumentation (WMI)
    c = wmi.WMI()
    processID, returnValue = c.Win32_Process.Create(CommandLine=name)
    print(f"Proses {name} dibuat dengan PID {processID}")

def PSProcessCreation(name):
    # Menggunakan PowerShell untuk membuat proses dan mendapatkan PID-nya
    command = ["powershell","& { invoke-wmimethod win32_process -name create -argumentlist notepad.exe | select ProcessId | % { $_.ProcessId } | Write-Host}"]
    p = subprocess.run(command, shell=True, capture_output=True)
    if p.returncode == 0:
        print(f"Proses {name} dibuat dengan PowerShell, PID {p.stdout.decode('utf-8')}")

# Contoh penggunaan:
command = "notepad.exe"
WMIProcessCreation(command)
PSProcessCreation(command)
