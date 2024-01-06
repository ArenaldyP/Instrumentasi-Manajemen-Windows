import win32evtlog
import xml.etree.ElementTree as ET

# Server lokal yang digunakan untuk mengambil log
server = "localhost"
# Jenis log yang diinginkan, dalam hal ini Microsoft-Windows-WMI-Activity/Trace
logtype = "Microsoft-Windows-WMI-Activity/Trace"
# Mengatur arah query ke depan
flags = win32evtlog.EvtQueryForwardDirection
# Kriteria query untuk mencari event dengan EventID 23
query = "*[System[EventID=23]]"

# Fungsi untuk mendapatkan log event
def GetEventLogs():
    q = win32evtlog.EvtQuery(logtype, flags, query)
    events = ()
    while True:
        e = win32evtlog.EvtNext(q, 100, -1, 0)
        if e:
            events = events + e
        else:
            break
    return events

# Fungsi untuk mem-parsing event log dan mengekstrak informasi yang diinginkan
def ParseEvents(events):
    for event in events:
        # Mendapatkan representasi XML dari event log
        xml = win32evtlog.EvtRender(event, 1)
        # Mengubah string XML menjadi struktur pohon elemen
        root = ET.fromstring(xml)
        # Menentukan path XPath untuk mencari informasi tentang proses yang diluncurkan
        path = "./{*}UserData/{*}ProcessCreate/{*}"
        # Mendapatkan command line dan PID dari XML
        name = root.findall(path+'Commandline')[0].text
        pid = root.findall(path+'CreatedProcessId')[0].text
        print(f"Proses {name} diluncurkan dengan PID {pid}")

# Mendapatkan log event
events = GetEventLogs()
# Mem-parsing dan mencetak informasi yang diinginkan dari log event
ParseEvents(events)
