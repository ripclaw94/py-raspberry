from IoHelper import readFile,writeFile
import os.path
from os import path
import threading, time, datetime

class GPIO(object) :
    OUT = 0
    IN = 1
    LOW = 0
    HIGH = 1
    BOARD = 12
    WARNINGS = 13
    RISING=14
    FALLING=15
    BOTH=16


    @staticmethod
    def setup(Pin,value):
        print(f"setup : {Pin} = {value}")
    
    @staticmethod
    def input(Pin):
        if(not path.exists(f'pins/{Pin}.pin')):
            writeFile(f'pins/{Pin}.pin','0')
        value = int(readFile(f'pins/{Pin}.pin'))
        return value
    
    @staticmethod
    def output(Pin,value):
        writeFile(f'pins/{Pin}.pin',str(value))
        
    
    @staticmethod
    def setmode(value):
        print(f"setmode  = {value}")
    
    @staticmethod
    def setwarnings(value):
        print(f"setWarings  = {value}")
    
    @staticmethod
    def checkPinValue(Pin, event , callback, bouncetime):
        oldvalue = 0
        while(True):
            val = GPIO.input(Pin)
            if(val!=oldvalue and val == 1) :
                callback("mouvement")
            oldvalue = val
            time.sleep(1)
    
    @staticmethod
    def add_event_detect(Pin, event , callback, bouncetime):
        print(f"add_event_detect : {Pin} = {event}")
        thread = threading.Thread(target =GPIO.checkPinValue ,args=(Pin,event,callback,bouncetime))
        thread.daemon = True
        thread.start()
    
    @staticmethod
    def remove_event_detect(Pin):
        print(f"remove_event_detect  = {Pin}")

    