from raspberry import Raspberry
import threading, time, datetime

BOUTON_CHAUDIERE = 33
BOUTON_PRESENCE = 38
LED_POWER = 32
LED_PRESENCE_off = 40
LED_PRESENCE_on = 37
LED_CHAUDIERE_off= 31
LED_CHAUDIERE_on = 29
BUZZER = 35
RELAIS = 16
PIR_DETECTOR = 26
PIN_11 = 11

class MyRaspberry(Raspberry) :
    
    AlarmePresence = 0
    AlarmeChaudiere = 0
    

    
    # SireneAlarme = Raspberry.Sirene('/home/pi/poussoir/lancesirene.py','SIRENE_ALARME')
    SireneAlarme = Raspberry.Sirene('/home/gilles/charlevoix/lancesirene.py','SIRENE_ALARME')
    BoutonPresence = Raspberry.Button(BOUTON_PRESENCE,'BOUTON PRESENCE')
    BoutonChaudiere = Raspberry.Button(BOUTON_CHAUDIERE,'BOUTON CHAUDIERE')
    PowerLed = Raspberry.Led(LED_POWER,'POWER')
    ChaudiereLedOn = Raspberry.Led(LED_CHAUDIERE_on,'CHAUD GREEN LED')
    ChaudiereLedOff = Raspberry.Led(LED_CHAUDIERE_off,'CHAUD RED LED')
    PresenceLedOn = Raspberry.Led(LED_PRESENCE_on,'PRESENCE GREEN LED')
    PresenceLedOff = Raspberry.Led(LED_PRESENCE_off,'PRESENCE RED LED')
    RelaiAlarme = Raspberry.Relay(RELAIS,'RELAI ALARME')
    BuzzerAlarme = Raspberry.Buzzer(BUZZER,'BUZZER')
    PresenceDetecteur = Raspberry.PirDetector(PIR_DETECTOR,'DETECTEUR PRESENCE')
    SondeTemperatureExterieur = Raspberry.TemperatureSensor("/sys/bus/w1/devices/28-01191285ec0d/w1_slave",'TEMPERATURE EXTERIEUR')
    SondeTemperatureCave = Raspberry.TemperatureSensor("/sys/bus/w1/devices/28-01191286c32d/w1_slave",'TEMPERATURE CAVE')
    SondeTemperatureChaudiere = Raspberry.TemperatureSensor("/sys/bus/w1/devices/28-01191eda1932/w1_slave",'TEMPERATURE CHAUDIERE')

    def __init__(self):
        super().__init__()
        self.BoutonPresence.Events.onTurnedOn += self.onBoutonPresenceOn
        self.BoutonPresence.Events.onTurnedOff += self.onBoutonPresenceOff
        self.BoutonChaudiere.Events.onTurnedOn += self.onBoutonChaudiereOn
        self.BoutonChaudiere.Events.onTurnedOff += self.onBoutonChaudiereOff
    
    
    def setup(self):
        self.BoutonPresence.setup()
        self.BoutonChaudiere.setup()
        self.PowerLed.setup()
        self.ChaudiereLedOn.setup()
        self.ChaudiereLedOff.setup()
        self.PresenceLedOn.setup()
        self.PresenceLedOff.setup()
        self.RelaiAlarme.setup()
        self.BuzzerAlarme.setup()
        self.PresenceDetecteur.setup()
    
    def initStates(self):
        self.PowerLed.initState()
        self.ChaudiereLedOn.initState()
        self.ChaudiereLedOff.initState()
        self.PresenceLedOn.initState()
        self.PresenceLedOff.initState()
        self.RelaiAlarme.initState()
        self.BuzzerAlarme.initState()
        self.PresenceDetecteur.initState()
        self.BoutonPresence.initState()
        self.BoutonChaudiere.initState()
    
    def ActiverAlarmePresence(self):
        self.AlarmePresence = 1
        delayRELAIS1 = 15
        delayRELAIS2 = 10
        for x in range(1, delayRELAIS1):
            statusBoutonPresence = self.BoutonPresence.Value
            if statusBoutonPresence == 0:
                self.AlarmePresence = 0
                return
            self.BuzzerAlarme.turnOn()
            time.sleep(0.25)
            self.BuzzerAlarme.turnOff()
            time.sleep(0.25)
        for x in range(1, delayRELAIS2):
            statusBoutonPresence = self.BoutonPresence.Value
            
            if statusBoutonPresence == 0:
                self.AlarmePresence = 0
                return
            self.BuzzerAlarme.turnOn()
            time.sleep(0.125)
            self.BuzzerAlarme.turnOff()
            time.sleep(0.125)

    def onBoutonPresenceOn(self):
        # print("---------Bouton Presence ON----------")
        self.SireneAlarme.activated = False
        self.AlarmePresence = 1
        self.PresenceLedOn.turnOff()
        self.PresenceLedOff.turnOn()
        self.ActiverAlarmePresence()
        if self.AlarmePresence==1:
            self.PresenceDetecteur.addEventListner(self.ON_RISING_EVENT,self.F_pir,3000000)
    
    def onBoutonPresenceOff(self):
        # print("---------Bouton Presence OFF----------")
        self.BuzzerAlarme.turnOff()  
        if self.SireneAlarme.activated :
            self.SireneAlarme.stop()
        self.AlarmePresence = 0
        self.RelaiAlarme.deactivate()
        self.PresenceLedOn.turnOn()
        self.PresenceLedOff.turnOff()
        self.PresenceDetecteur.removeEventListner()
    
    def onBoutonChaudiereOn(self):
        # print("---------Bouton Presence ON----------")
        self.SireneAlarme.activated = False
        self.AlarmeChaudiere = 1
        self.ChaudiereLedOn.turnOff()
        self.ChaudiereLedOff.turnOn()
    
    def onBoutonChaudiereOff(self):
        # print("---------Bouton Presence ON----------")
        self.SireneAlarme.activated = False
        self.AlarmeChaudiere = 0
        self.ChaudiereLedOn.turnOn()
        self.ChaudiereLedOff.turnOff()
       
    
    def F_pir(self,channel):
        now = datetime.datetime.now()    
        timee=now.strftime("%Y-%m-%d %H:%M:%S")
        print ("----------------------f3 pir detect something-----------:" + timee +" alarmesirene:")
        self.SireneAlarme.start()
    
    def checkUpdate(self):
        self.AlarmePresence = self.BoutonPresence.Value
        self.AlarmeChaudiere = self.BoutonChaudiere.Value
        # print(f"AlarmePresence : {self.AlarmePresence}")
        # print(f"AlarmeChaudiere : {self.AlarmeChaudiere}")
        if(self.AlarmePresence) :
            print('----------Alarme Presence Activée')

        time.sleep(1)