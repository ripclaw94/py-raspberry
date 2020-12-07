
import socket
import psutil
import sys
from subprocess import Popen,PIPE,STDOUT
from enum import Enum 
import threading, time

class Status(Enum):
    STARTED = 1
    STOPPED = 2
    ERROR = 3
    

class Script(object):
    Interpreter = None
    Filename = None
    Process = None
    StartedActions = ['RESTART','STOP']
    StoppedActions = ['START']

    def __init__(self,interpreter,filename):
        self.Filename = filename
        self.Interpreter = interpreter
        self.__Status = self.checkIfScriptIsRunning()
    
    @property
    def Actions(self):
        if self.__Status == Status.STARTED :
            return  self.StartedActions
        elif self.__Status == Status.STOPPED :
            return self.StoppedActions
        else :
            return []

    @property
    def Status(self):
        self.__Status = self.checkIfScriptIsRunning()
        return  self.__Status

    @property
    def StatusStr(self):
        v = self.Status
        if(v==Status.STARTED):
            return "STARTED"
        elif (v==Status.STOPPED):
            return "STOPPED"
        else :
            return  "ERROR"

    def checkIfScriptIsRunning(self):
        if(self.Interpreter is not None and self.Filename is not None) :
            for process in psutil.process_iter():
                try:
                    if len(process.cmdline())>=2 and self.Interpreter in process.cmdline()[0] and self.Filename in process.cmdline()[1]:
                        self.Process = process
                        return Status.STARTED
                except Exception as identifier:
                    s = Status.ERROR
            return Status.STOPPED
        else :
            return Status.ERROR
    
    def stop(self):
        if(self.Process != None) :
                Popen.kill(self.Process)
    
    def start(self):
         self.Process = Popen([self.Interpreter, self.Filename], stdout=PIPE, stderr=STDOUT)
        #  time.sleep(10)

    def restart(self):
        if(self.Process != None ) : 
            self.stop()
            self.start()

def readFile(filename ):
    contenu =''
    f=None
    try:
        f = open(filename,"r", encoding = 'utf-8')
        contenu = f.read()
    except Exception as ex:
        print(ex)
        contenu = ''
    finally:
        
        if(f!=None):
            f.close()
    return contenu

def writeFile(filename, value):
    success = True
    f=None
    try:
        f = open(filename,"w+", encoding = 'utf-8')
        f.write(value)
    except:
        success=False
    finally:
        if(f!=None):
            f.close()
    return success

def checkIfPortRunning(port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    if result_of_check == 0:
        return 'ONLINE'
    else:
        return 'OFFLINE'



    