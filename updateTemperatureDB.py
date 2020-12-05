#!/usr/bin/env python3
from databaseHelper import DataBaseHelper
from IoHelper import readFile
from datetime import datetime, timedelta 
import time
import os
import sqlite3
import socket
import subprocess

import RPi.GPIO as GPIO
from myRaspberry import MyRaspberry

rasp = MyRaspberry()

update_time = 300

rasp.BoutonPresence.deactivateEvents()
rasp.BoutonChaudiere.deactivateEvents()

dbHelper = DataBaseHelper('/home/pi/ProjetGraphTemp/gpio.db')
app = Flask(__name__)

def updateBoutonStatus():
    btnChaudiereActif = rasp.BoutonChaudiere.Value
    btnPresenceActif = rasp.BoutonPresence.Value
    dbHelper.executeQuery('update config set bouton_chaudiere = ?,bouton_presence=?',(btnChaudiereActif,btnPresenceActif))
    
def checkDdns():
    ligne_config = dbHelper.fetchOneQuery('select * from config')
    ddns_name = ligne_config[3]
    ddns_ip_old = ligne_config[4]
    try:
        ddns_ip_new = socket.gethostbyname_ex(ddns_name)[2][0]
        if ddns_ip_new != ddns_ip_old:
            dbHelper.updateDns(ddns_ip_new)
            subprocess.call(['sh', '/home/pi/crontab-alarm/restart-firewall.sh'])
    except Exception as error:
        print('error : '+error)

    cursor.close()
    conn.close()

def saveTemperatures():
    error =0
    try:
        temperature = rasp.SondeTemperatureCave.getValue()
        temperature2 = rasp.SondeTemperatureChaudiere.getValue()
        temperature3 = rasp.SondeTemperatureExterieur.getValue()
        temperature4 = rasp.getRaspTemperature()
        enregistrementDB(temperature,temperature2,temperature3,temperature4)
    except:
        error = 1
    return error
    
def enregistrementDB(temperature_cave,temperature_exterieur,temperature_chaudiere,temperature_rasp):
    d = datetime.now()
    dbHelper.insertTemperature("temperatures_chaudiere",temperature_chaudiere,d)
    dbHelper.insertTemperature("temperatures_cave",temperature_cave,d)
    dbHelper.insertTemperature("temperatures_exterieur",temperature_exterieur,d)
    dbHelper.insertTemperature("temperatures_rasp",temperature_rasp,d)

while True :
    updateBoutonStatus()
    saveTemperatures()
    checkDdns()
    time.sleep(update_time)
 

    