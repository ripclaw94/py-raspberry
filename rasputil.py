import sys
from myRaspberry import MyRaspberry
from databaseHelper import DataBaseHelper
from datetime import datetime, timedelta
import time

print("RapsBerry Util v1.0 2020 ")

dbHelper = DataBaseHelper('gpio.db')
rasp = MyRaspberry()
rasp.setup()
rasp.BoutonChaudiere.deactivateEvents()
rasp.BoutonPresence.deactivateEvents()

global option
global param

try:
    option =  sys.argv[1]
except :
    option = None
try:
    param =  sys.argv[2]
except :
    param = None


def status(val):
    if(val) :
        return "ON"
    else :
        return "OFF"

def help():
    print("Liste des commandes disponibles")

def temperatureRasp():
    print(f"t = {rasp.getRaspTemperature()} °C")

def temperatureCave():
    if(param is None):
        print(f"t = {rasp.SondeTemperatureCave.getValue()} °C")
    else :
        try:
            d = datetime.strptime(param, '%Y%m%d')
            temps = dbHelper.getTemperaturesOfDate(d)
            print(f"temperatures du {d.strftime('%d/%m/%Y')}")
            print(temps)
        except :
            print("Erreur dans le format de la date ( YYYYmmdd )")

def printStatus():
    print("-------------------------------------------------")
    print(f"BOUTON CHAUDIERE : {status(rasp.BoutonChaudiere.Value)}")
    print(f"BOUTON PRESENCE : {status(rasp.BoutonChaudiere.Value)}")
    print(f"BOUTON PRESENCE : {status(rasp.BoutonChaudiere.Value)}")
    print(f"BOUTON PRESENCE : {status(rasp.BoutonChaudiere.Value)}")
    print(f"BOUTON PRESENCE : {status(rasp.BoutonChaudiere.Value)}")
    print(f"BOUTON PRESENCE : {status(rasp.BoutonChaudiere.Value)}")
    print(f"BOUTON PRESENCE : {status(rasp.BoutonChaudiere.Value)}")
    print("-------------------------------------------------")
    print(f"T CAVE : {rasp.SondeTemperatureCave.getValue()} °C")
    print(f"T CHAUDIERE : {rasp.SondeTemperatureChaudiere.getValue()} °C")
    print(f"T EXTERIEUR : {rasp.SondeTemperatureExterieur.getValue()} °C")
    print("-------------------------------------------------")


if(option == 'help'):
    help()
elif(option == 't'):
    temperatureRasp()
elif(option == 't-cave'):
    temperatureCave()
elif (option == 'status'):
    printStatus()

else :
    help()