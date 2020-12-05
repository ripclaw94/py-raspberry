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

delayRELAIS =10
alarmesirene = 0
alarme =0

rasp = MyRaspberry()
rasp.setup()
rasp.PowerLed.turnOn()
rasp.PresenceLedOff.turnOff()
rasp.PresenceLedOn.turnOn()
rasp.BuzzerAlarme.turnOff()
 
while True:
    rasp.checkUpdate()
    


