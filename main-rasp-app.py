#!/usr/bin/env python3
from myRaspberry import MyRaspberry
from time import sleep     # this lets us have a time delay (see line 12)  
import threading, time, datetime
import raspberryHelper
import threading 
import os, signal
import datetime
import sys
import subprocess

from IoHelper import checkIfPortRunning,Script

delayRELAIS =10
alarmesirene = 0
alarme =0

rasp = MyRaspberry()

def init():
    rasp.setup()
    #rasp.initStates()
    rasp.BoutonPresence.Events.onTurnedOn += onBoutonPresenceOn
    rasp.BoutonPresence.Events.onTurnedOff += onBoutonPresenceOff
    rasp.BoutonChaudiere.Events.onTurnedOn += onBoutonChaudiereOn
    rasp.BoutonChaudiere.Events.onTurnedOff += onBoutonChaudiereOff
    rasp.PowerLed.turnOn()
    rasp.PresenceLedOff.turnOff()
    rasp.PresenceLedOn.turnOn()
    rasp.BuzzerAlarme.turnOff()


def onBoutonPresenceOn():
    # print("---------Bouton Presence ON----------")
    rasp.SireneAlarme.activated = False
    rasp.AlarmePresence = 1
    rasp.PresenceLedOn.turnOff()
    rasp.PresenceLedOff.turnOn()
    rasp.ActiverAlarmePresence()
    if rasp.AlarmePresence==1:
        rasp.PresenceDetecteur.addEventListner(rasp.ON_RISING_EVENT,F_pir,3000000)

def onBoutonPresenceOff():
    # print("---------Bouton Presence OFF----------")
    rasp.BuzzerAlarme.turnOff()  
    if rasp.SireneAlarme.activated :
        rasp.SireneAlarme.stop()
    rasp.AlarmePresence = 0
    rasp.RelaiAlarme.deactivate()
    rasp.PresenceLedOn.turnOn()
    rasp.PresenceLedOff.turnOff()
    rasp.PresenceDetecteur.removeEventListner()

def F_pir(channel):
    now = datetime.datetime.now()    
    timee=now.strftime("%Y-%m-%d %H:%M:%S")
    print ("----------------------f3 pir detect something-----------:" + timee +" alarmesirene:")
    rasp.SireneAlarme.start()

def onBoutonChaudiereOn():
    print("---------Bouton CHAUDIERE ON----------")
    rasp.temperatures.clear()
    rasp.AlarmeChaudiere = 1
    rasp.ChaudiereLedOn.turnOff()
    rasp.ChaudiereLedOff.turnOn()

def onBoutonChaudiereOff():
    print("---------Bouton CHAUDIERE OFF----------")
    if(rasp.SireneAlarme.activated):
        print("---------DESACTIVATION SIRENE----------")
        rasp.SireneAlarme.stop()
    rasp.temperatures.clear()
    rasp.AlarmeChaudiere = 0
    rasp.ChaudiereLedOn.turnOn()
    rasp.ChaudiereLedOff.turnOff()

def checkTemperatureChaudiere():
    rasp.temperatures.insert(0, rasp.SondeTemperatureChaudiere.Value)
    print(rasp.temperatures)
    if(len(rasp.temperatures)>10):
        rasp.temperatures.pop()
    if(rasp.EmailChaudiereEnvoye and max(rasp.temperatures)<rasp.MaxTemperatureChaudiereEmail ) :
        rasp.EmailChaudiereEnvoye = rasp
    if(rasp.EmailChaudiereEnvoye!=rasp and rasp.temperatures[0] > rasp.MaxTemperatureChaudiereEmail):
        rasp.sendEmailAlarmeChaudiere()
    if(rasp.SireneAlarme.activated!=True and rasp.temperatures[0] > rasp.MaxTemperatureChaudiereSirene ):
        print('----------Activation SIRENE--------')
        rasp.SireneAlarme.start()
        
    def sendEmailAlarmeChaudiere():
        print('----------Envoi mail Chaudiere')
        rasp.EmailChaudiereEnvoye = True

init()
# script = Script ( '/bin/python3','/home/gilles/charlevoix/app2.py')
# script.start()
# time.sleep(5)
while True:
    rasp.AlarmePresence = rasp.BoutonPresence.Value
    rasp.AlarmeChaudiere = rasp.BoutonChaudiere.Value
    if(rasp.AlarmePresence) :
        print('----------Alarme Presence Activée')
    if(rasp.AlarmeChaudiere) :
        print('----------Alarme Chaudiere Activée')
        checkTemperatureChaudiere()
    time.sleep(1)
    # rasp.checkUpdate()
    


