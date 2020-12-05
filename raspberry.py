from GPIO import GPIO
from events import Events
from raspberryHelper import getTemperatureFromSonde,getTemperatureRaspberry
from subprocess import Popen, PIPE
import sys


class Raspberry(object):

    TEMPERATURE_RASP_FILENAME = '/sys/class/thermal/thermal_zone0/temp'
    
    
    ON_RISING_EVENT = GPIO.RISING
    ON_FALLING_EVENT = GPIO.FALLING
    ON_CHANGE_EVENT = GPIO.BOTH

    def __init__(self):
        self.Mode = GPIO.BOARD
        self.GPIO_Warning = False

    @property
    def Mode(self):
        return self.__Mode

    @Mode.setter
    def Mode(self, value):
        GPIO.setmode(value) 
        self.__Mode = value
    
    @property
    def GPIO_Warning(self):
        return self.__GPIO_Warning

    @GPIO_Warning.setter
    def GPIO_Warning(self, value):
        GPIO.setwarnings(False)
        self.__GPIO_Warning = value
    
    def getRaspTemperature(self):
        return getTemperatureRaspberry(self.TEMPERATURE_RASP_FILENAME,1000)
    
    def checkUpdate(self):
        pass

    class Element(object) :

        def __init__(self, pin,name):
            self.Pin = pin
            self.Name = name
            
        
        def initState(self) : 
            self.initValue()

        def initValue(self) :
            pass

        def addEventListner(self,event,func,delta):
            GPIO.add_event_detect(self.Pin, event , callback=func, bouncetime=delta)
        
        def removeEventListner(self):
            GPIO.remove_event_detect(self.Pin)
            
        @property
        def Pin(self):
            return self.__Pin

        @Pin.setter
        def Pin(self, Pin):
            self.__Pin = Pin
            
        @property
        def Name(self):
            return self.__Name

        @Name.setter
        def Name(self, name):
            self.__Name = name
        
        @property
        def Type(self):
            return self.__Type

        @Type.setter
        def Type(self, type):
            self.__Type = type
            
        
        def setup(self):
            GPIO.setup(self.Pin, self.Type)
            
        
        def output(self,value):
            if(self.Type==GPIO.OUT):
                GPIO.output(self.Pin, value)
        
        def input(self) :
            if(self.Type == GPIO.IN):
                return GPIO.input(self.Pin)
            else :
                return -1

    class OutputElement(Element) :
        def __init__(self, pin,name):
            self.Pin = pin
            self.Type = GPIO.OUT
            self.Name = name
            self.input()
        
        @property
        def Value(self):
            self.__Value =  GPIO.input(self.Pin)
            return self.__Value

        @Value.setter
        def Value(self, value):
            self.__Value = value

        def initValue(self) :
            self.__Value = self.input()

        def turnOn(self):
            self.output(GPIO.HIGH)
        
        def turnOff(self):
            self.output(GPIO.LOW)
        
        def output(self,value):
            if(self.Type==GPIO.OUT):
                self.Value = value
                GPIO.output(self.Pin, value)
        
        
            
        
    class InputElement(Element) :
        
        def __init__(self, pin,name):
            self.Pin = pin
            self.Type = GPIO.IN
            self.Name = name
            self.input()
            
        def initValue(self) :
            self.__Value = self.input()

        @property
        def Value(self):
            self.__Value =  self.input()
            return self.__Value
        
        def debugOutput(self,value):
                self.__Value = value
                GPIO.output(self.Pin, value)
        

    class Led(OutputElement):
        def __init__(self, pin,name):
            super().__init__(pin,name)

    class Buzzer(OutputElement):
        def __init__(self, pin,name):
            super().__init__(pin,name)
        
        def output(self,value):
            self.State = value
            if ( value ) :
                print("BEEP")
            else :
                print("----")
            GPIO.output(self.Pin, value)

    class Relay(InputElement):
        activated = False
        def __init__(self, pin,name):
            self.Pin = pin
            self.Type = GPIO.IN
            self.Name = name
        
        def activate(self):
            self.setup()
            activate = True
        
        def deactivate(self):
            self.setup()
            activate = False

    class Button(InputElement):

        def __init__(self, pin,name):
            self.Pin = pin
            self.Type = GPIO.IN
            self.Events = Events(('onTurnedOn', 'onTurnedOff'))
            self.__Value = 0
            self.throwEvents = True
            self.Name = name
            
        
        def initValue(self):
            val = self.input()
            print(f'value : {self.__Value} val : {val}')
            if (val!=self.__Value):
                print("val!=self.__Value")
                if(val) :
                    print("val = 1")
                    self.__Value = val
                    if(self.throwEvents):
                        print("launch onturnedOn")
                        self.Events.onTurnedOn()
                else :
                    print("val = 0")
                    self.__Value = val
                    if(self.throwEvents):
                        print("launch onturnedOff")
                        self.Events.onTurnedOff()
            self.__Value = val

        @property
        def Value(self):
            result =  self.input()
            if(result!=self.__Value):
                if(result) :
                    self.__Value = result
                    if(self.throwEvents):
                        self.Events.onTurnedOn()
                else :
                    self.__Value = result
                    if(self.throwEvents):
                        self.Events.onTurnedOff()
            self.__Value = result
            return self.__Value
        def deactivateEvents(self):
            self.throwEvents = False
        def activateEvents(self):
            self.throwEvents = True
    
    class PirDetector(InputElement):
        def __init__(self, pin,name):
            self.Pin = pin
            self.Type = GPIO.IN
            self.Name = name
    
    class Sensor(object):
        def __init__(self, _filename,name):
            self.Filename = _filename
            self.Name = name

        @property
        def Filename(self):
            return self.__Filename

        @Filename.setter
        def Filename(self, _filename):
            self.__Filename = _filename
        
    class TemperatureSensor(Sensor):
        def getValue(self):
            return getTemperatureFromSonde(self.Filename,1000)
        
        @property
        def Value(self):
            return  self.getValue()
    
    class Sirene(object) :
        proc = {}
        activated = False
        def __init__(self, _filename,name):
            self.Filename = _filename
            self.Name = name
        
        def start(self):
            self.activated = True
            self.proc = Popen([sys.executable,self.Filename], stdout=PIPE, bufsize=1)
            
        def stop(self):
            self.activated = False
            if(self.proc):
                Popen.kill(self.proc)


        