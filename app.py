#!/usr/bin/env python3
from emailer import Emailer
import raspberryHelper
from myRaspberry import MyRaspberry
from raspberryHelper import getTemperatureFromSonde
from databaseHelper import DataBaseHelper
from flask import Flask, render_template,jsonify
import sys
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
import time
import os
import sqlite3
import subprocess
import platform

print (sys.path)

# GPIO INIT
import RPi.GPIO as GPIO

global btnChaudiereActif
btnChaudiereActif = 0

global btnPresenceActif
btnPresenceActif = 0

rasp = MyRaspberry()
rasp.BoutonChaudiere.deactivateEvents()
rasp.BoutonPresence.deactivateEvents()


global dbHelper
dbHelper = DataBaseHelper('/home/pi/ProjetGraphTemp/gpio.db')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})




def envoiemail () :
    now = datetime.datetime.now()
    timee=now.strftime("%d-%m-%Y %H:%M:%S")
    sender = Emailer() 
    sendTo = 'ma.charlevoix@gmail.com'
    emailSubject = "Avertir jerome ou loic, Reboot du raspberry a " + timee
    emailContent = "une ou des sondes ne repondent plus " + timee
    sender.sendmail(sendTo, emailSubject, emailContent)

def getTemp():
    try:
        temperature = rasp.SondeTemperatureCave.getValue()
        temperature2 = rasp.SondeTemperatureChaudiere.getValue()
        temperature3 = rasp.SondeTemperatureExterieur.getValue()
    except:
        envoiemail () 
        #subprocess.call(['sh', '/home/pi/crontab-alarm/reboot.sh'])
        time.sleep(10)
    return temperature


@app.route('/api/activerAlarme', methods=["POST"])
@cross_origin()
def activerAlarme():
    return "Alarme activée"

@app.route('/api/desactiverAlarme', methods=["POST"])
@cross_origin()
def desactiverAlarme():
    return "Alarme desactivée"

@app.route('/')
def index():
    btnChaudiereActif = rasp.BoutonChaudiere.Value
    btnPresenceActif = rasp.BoutonPresence.Value
    recordTemperatureChaud = dbHelper.getLastTemperaturesOfTable('temperatures_cave')
    
    return render_template('index.html', nomSite = 'Raspberry Loic',
        btnChaudiereActif=btnChaudiereActif,
        btnPresenceActif=btnPresenceActif,
        recordTemperatureChaud=recordTemperatureChaud)

@app.route("/getTemp")
def affTemp():
    return render_template('index.html', temp=getTemp())

@app.route("/graphTemp")
def graphTempToday():
    return graphTemp(None)

@app.route("/graphTempChaud")
def graphTempTodayChaud():
    return graphTempChaud(None)
    

@app.route("/graphTemp/<date>")
def graphTemp(date):
    curTemp = dbHelper.getLastTemperaturesOfTable('temperatures_cave')
    if date is None:
        d = datetime.now()
        titre = f"Temperature cave actuelle : {curTemp}" 
    else:
        d = datetime.strptime(date, '%Y%m%d')
        titre = f"Statistiques du {d.strftime('%d/%m/%Y')}" 

    temps = dbHelper.getTemperatureMinMaxCurrent(d)
    
    points = dbHelper.getTemperaturesOfDate(d)
    
    nextDate = d + timedelta(days=1)
    prevDate = d - timedelta(days=1)
    # On retourne tout a la page graphTemp.html
    return render_template(
        'graphTemp.html',
        d = d.strftime("%Y-%m-%d"),
        titre = titre,
        temp = curTemp,
        points = points,
        tempMax = temps['maxCave'],
        tempMin = temps['minCave'],
        tempMoy = temps['moyCave'],
        tempMax2 = temps['maxExt'],
        tempMin2 = temps['minCave'],
        tempMoy2 = temps['moyCave'],
        prevDate = prevDate.strftime("%Y%m%d"),
        nextDate = nextDate.strftime("%Y%m%d")
    )


@app.route("/graphTempChaud/<date>")
def graphTempChaud(date):
    curTemp = dbHelper.getLastTemperaturesOfTable('temperatures_chaudiere')
    if date is None:
        d = datetime.now()
        titre = f"Temperature Chaudiere actuelle : {curTemp}" 
    else:
        d = datetime.strptime(date, '%Y%m%d')
        titre = f"Statistiques du {d.strftime('%d/%m/%Y')}" 
    points = dbHelper.getTemperaturesCaveAndRaspOfDate(d)
    temps = dbHelper.getTemperatureMinMaxCurrent(d)
    nextDate = d + timedelta(days=1)
    prevDate = d - timedelta(days=1)
    
    
    return render_template(
        'graphTempChaud.html',
        d = d.strftime("%Y-%m-%d"),
        titre = titre,
        temp = curTemp,
        points = points,
        tempMax = temps['maxChaud'],
        tempMin = temps['minChaud'],
        tempMoy = temps['moyChaud'],
        prevDate = prevDate.strftime("%Y%m%d"),
        nextDate = nextDate.strftime("%Y%m%d")
    )
@app.route("/reboot")
def reboot():
    subprocess.call(['sh', '/home/pi/crontab-alarm/reboot.sh'])
    return 'Reboot en cours'
    
@app.route("/stopf")
def stopf():
    subprocess.call(['sh', '/home/pi/crontab-alarm/stop-firewall.sh'])
    return 'firewall stop'

@app.route("/startf")
def startf():
    subprocess.call(['sh', '/home/pi/crontab-alarm/start-firewall.sh'])
    return 'firewall start'
    
@app.route("/api/reboot", methods=["POST"])
@cross_origin()
def api_reboot():
    subprocess.call(['sh', '/home/pi/crontab-alarm/reboot.sh'])
    return 'Reboot en cours'
    
@app.route("/api/stopFirewall", methods=["POST"])
@cross_origin()
def api_stopf():
    subprocess.call(['sh', '/home/pi/crontab-alarm/stop-firewall.sh'])
    return 'firewall stop'

@app.route("/api/startFirewall", methods=["POST"])
@cross_origin()
def api_startf():
    subprocess.call(['sh', '/home/pi/crontab-alarm/start-firewall.sh'])
    return 'firewall start'

@app.route("/api/temperatures/<date>", methods=["GET"])
@cross_origin()  
def api_graphTemp(date):
    curTemp = dbHelper.getLastTemperaturesOfTable('temperatures_cave')
    if date is None:
        d = datetime.now()
        titre = "Temperature cave actuelle : "  +curTemp
    else:
        d = datetime.strptime(date, '%Y%m%d')
        titre = f"Statistiques du {d.strftime('%%d/%m/%Y')}" 

    temps = dbHelper.getTemperatureMinMaxCurrent(d)
    points = dbHelper.getTemperaturesOfDate(d)
    nextDate = d + timedelta(days=1)
    prevDate = d - timedelta(days=1)
    return jsonify(
        
        points = points,
        temps = temps
        
    )
    
@app.route("/api/checkPassword/<password>", methods=["GET"])
@cross_origin()  
def api_checkPassword(password):
    auth = dbHelper.getPasswordAuthentification(password)
    return jsonify(
        
        authorized = auth
        
    )
    
@app.route("/api/currentTemp", methods=["GET"])
@cross_origin()  
def currentTemp():
    temperature = 0.0
    temperature2 = 0.0
    temperature3 = 0.0
    try:
        temperature = rasp.SondeTemperatureCave.getValue()
        temperature2 = rasp.SondeTemperatureChaudiere.getValue()
        temperature3 = rasp.SondeTemperatureExterieur.getValue()
    except:
        envoiemail () 
        subprocess.call(['sh', '/home/pi/crontab-alarm/reboot.sh'])
        time.sleep(10)
    return jsonify(
        tempExterieur = temperature2,
        tempCave = temperature,
        tempChaudiere = temperature3
    )
    


def cpu_generic_details():
    try:
        items = [s.split('\t: ') for s in subprocess.check_output(["cat /proc/cpuinfo  | grep 'model name\|Hardware\|Serial' | uniq "], shell=True).splitlines()]
    except Exception as ex:
        print (ex)
    finally:
        return items

def disk_usage_list():
    try:
        items = [s.split() for s in subprocess.check_output(['df', '-h'], universal_newlines=True).splitlines()]
    except Exception as ex:
        print (ex)
    finally:
        return items[1:]

def running_process_list():
    try:
        items = [s.split() for s in subprocess.check_output(["ps -Ao user,pid,pcpu,pmem,comm,lstart --sort=-pcpu"], shell=True).splitlines()]
    except Exception as ex:
        print (ex)
    finally:
        return items[1:]

@app.route('/home')
def index1():
    sys_data = {"current_time": '',"machine_name": ''}
    try:
        sys_data['current_time'] = datetime.now().strftime("%d-%b-%Y , %I : %M : %S %p")
        sys_data['machine_name'] =  platform.node()
        cpu_genric_info = cpu_generic_details()
        disk_usage_info = disk_usage_list()
        running_process_info = running_process_list()
    except Exception as ex:
        print (ex)
    finally:
        return render_template("index1.html", title='Raspberry Pi - System Information',
                               sys_data = sys_data,
                               cpu_genric_info = cpu_genric_info,
                               disk_usage_info= disk_usage_info,
                               running_process_info = running_process_info)


app.run(debug=True, host='0.0.0.0', port=5000)