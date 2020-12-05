from IoHelper import readFile
import platform
import re
import psutil


class SystemHelper :
    memory = {}
    cpuInfo ={}
    osInfo = {}
    processes = []
    upTime = {}
    temperatures = {}
    currentProcess = {}

    def __init__(self) :
        self.getCpuInfo()
        self.getMemoryUsage()
        self.getOsInfos()
        self.getProcesses()
        self.getUptime()

    def getMemoryUsage(self):
        self.memory = {}
        contenu = readFile('/proc/meminfo')
        self.memory['total'] = float(re.search('MemTotal:(.*)kB', contenu).group(1).strip())/1000
        self.memory['free'] = float(re.search('MemFree:(.*)kB', contenu).group(1).strip())/1000
        self.memory['used'] =self.memory['total'] -self.memory['free']
        output = f"""Memory infos\n
total={self.memory['total']} MB\n
used={self.memory['used']} MB\n
free={self.memory['free']} MB\n"""
        return output

    def getCpuInfo(self):
        self.cpuInfo = {}
        contenu =readFile('/proc/cpuinfo')
        # print(contenu)
        lignes = contenu.split('\n')
        self.cpuInfo['model'] = re.search(':(.*)', lignes[4]).group(1).strip()
        self.cpuInfo['cores'] = re.search(':(.*)', lignes[12]).group(1).strip()
        return self.cpuInfo

    def getOsInfos(self):
        self.osInfos = {}
        # Architecture
        self.osInfos["Architecture"] =   platform.architecture()
        self.osInfos["Machine"] =   platform.machine()
        self.osInfos["Node"] =   platform.node()
        self.osInfos["System"] =   platform.system()
        contenu = readFile('/etc/lsb-release')
        self.osInfos["distrib"]=re.search('DISTRIB_ID=(.*)\n', contenu).group(1).strip()
        self.osInfos["distrib_release"]=re.search('DISTRIB_RELEASE=(.*)\n', contenu).group(1).strip()
        self.osInfos["distrib_codename"]=re.search('DISTRIB_CODENAME=(.*)\n', contenu).group(1).strip()
        self.osInfos["distrib_description"]=re.search('DISTRIB_DESCRIPTION=(.*)\n', contenu).group(1).strip()
        output = f"""Architecture: {self.osInfos["Architecture"]}\n
Machine:{self.osInfos["Machine"]}\n
Node:{self.osInfos["Node"]}\n
System:{self.osInfos["System"]}\n
distrib:{self.osInfos["distrib"]}\n
distrib_release:{self.osInfos["distrib_release"]}\n
distrib_codename:{self.osInfos["distrib_codename"]}\n
distrib_description:{self.osInfos["distrib_description"]}\n
"""
        return output

    def getUptime(self):
        self.upTime = {}
        contenu = readFile("/proc/uptime")
        uptime_text = contenu.split(" ")[0].strip()
        uptime_int = int(float(uptime_text))
        uptime_hours = uptime_int // 3600
        uptime_minutes = (uptime_int % 3600) // 60
        self.upTime["hour"] = uptime_hours
        self.upTime["minute"] = uptime_minutes
        return self.upTime

        
    def getProcesses(self):
        self.processes = []
        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                # processName = proc.name()
                # processID = proc.pid
                # print(proc.as_dict())
                # print(proc.as_dict().keys())
                # print('###################')
                self.processes.append(proc.as_dict(attrs=['pid', 'name', 'username','cmdline']))
                # print(processName , ' ::: ', processID)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return self.processes

    def getTemperatures(self):
        self.temperatures =  psutil.sensors_temperatures()
        return temps

    def getProc(self) :
        self.currentProcess = psutil.Process().as_dict(attrs=['pid', 'name', 'username','cmdline'])
        return self.currentProcess
