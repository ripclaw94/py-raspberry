import curses
from myRaspberry import MyRaspberry
from raspberry import Raspberry
import threading, time, datetime
from IoHelper import checkIfPortRunning,Script

rasp = MyRaspberry()
rasp.setup()
rasp.BoutonChaudiere.deactivateEvents()
rasp.BoutonPresence.deactivateEvents()
rasp.initStates()

categories = ['inputs', 'servers', 'scripts']
global selectedCategorieIndex
selectedCategorieIndex = 0
global selectedActionIndex
selectedActionIndex = 0

global index
index = 0

inputPins = []
inputPins.append(rasp.BoutonPresence)
inputPins.append(rasp.BoutonChaudiere)
inputPins.append(rasp.PresenceDetecteur)
inputPins.append(rasp.RelaiAlarme)


outputPins = []
outputPins.append(rasp.PowerLed)
outputPins.append(rasp.ChaudiereLedOn)
outputPins.append(rasp.ChaudiereLedOff)
outputPins.append(rasp.PresenceLedOn)
outputPins.append(rasp.PresenceLedOff)
outputPins.append(rasp.BuzzerAlarme)

sondes = []
sondes.append(rasp.SondeTemperatureCave)
sondes.append(rasp.SondeTemperatureExterieur)
sondes.append(rasp.SondeTemperatureChaudiere)

scripts = []
scripts.append (Script ( '/bin/python3','/home/gilles/py-raspberry/main-rasp-app.py'))
scripts.append (Script ( '/bin/python3','/home/gilles/charlevoix/app2.py'))


def printSonde(stdscr,element:Raspberry.TemperatureSensor,x,y) :
    Name = element.Name
    Value = str(element.Value)+' °C'
    stdscr.addstr(y, x, Name)
    stdscr.addstr(y, x+30, Value)

def printElement(stdscr,element:Raspberry.Element,x,y, selected:bool) :
    
    Name = element.Name
    Value = str(element.Value)
    if selected:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x,Name)
            stdscr.addstr(y, x+20, Value)
            stdscr.attroff(curses.color_pair(1))
    else:
        stdscr.addstr(y, x, Name)
        stdscr.addstr(y, x+20, Value)

def printInputs(stdscr,selectedName):
    y = 5
    x = 2
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(y, x,"INPUTS")
    stdscr.attroff(curses.color_pair(2))
    y+=1
    for idx, element in enumerate(inputPins):
        printElement(stdscr,element,x,y,(selectedCategorieIndex==0 and selectedName==element.Name))
        y+=1

def printOutputs(stdscr,selectedName):
    y = 5
    x = 42
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(y, x,"OUTPUTS")
    stdscr.attroff(curses.color_pair(2))
    y+=1
    for idx, element in enumerate(outputPins):
        printElement(stdscr,element,x,y,False)
        y+=1

def printSondes(stdscr):
    y = 12
    x = 2
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(y, x,"SONDES TEMPERATURE")
    stdscr.attroff(curses.color_pair(2))
    y+=1
    for idx, sonde in enumerate(sondes):
        printSonde(stdscr,sonde,x,y)
        y+=1
def printServerStatus(stdscr):
    y = 18
    x = 2
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(y, x,"SERVERS")
    stdscr.attroff(curses.color_pair(2))
    y+=1
    stdscr.attron(curses.color_pair(0))
    stdscr.addstr(y, x,"FLASK SERVER (5000)")
    stdscr.addstr(y, x+20,checkIfPortRunning(5000))
    stdscr.attroff(curses.color_pair(0))
    y+=1
    stdscr.attron(curses.color_pair(0))
    stdscr.addstr(y, x,"APACHE SERVER (80)")
    stdscr.addstr(y, x+20,checkIfPortRunning(80))
    stdscr.attroff(curses.color_pair(0))

def printScriptStatus(stdscr,script:Script,x,y,selected:bool):
    
    stdscr.addstr(y, x,script.Filename)
    x+=45
    stdscr.addstr(y, x,str(script.StatusStr))
    x+=12
    for idx,action in enumerate(script.Actions) :
        if(selected ):
            selectedAction = script.Actions[selectedActionIndex]
            if(selectedAction == action):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x,action)
                stdscr.attroff(curses.color_pair(1))
            else :
                stdscr.attron(curses.color_pair(0))
                stdscr.addstr(y, x,action)
                stdscr.attroff(curses.color_pair(0))
        else :
            stdscr.attron(curses.color_pair(0))
            stdscr.addstr(y, x,action)
            stdscr.attroff(curses.color_pair(0))
        x+=10

def printScriptsStatus(stdscr):
    selected = False
    y = 22
    x = 2
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(y, x,"SCRIPT STATUS")
    stdscr.attroff(curses.color_pair(2))
    y+=1
    for idx, script in enumerate(scripts):
        printScriptStatus(stdscr,script,x,y,(selectedCategorieIndex == 2 and idx ==index))
        y+=1


def printHeader(stdscr):
    y = 1
    x = 2
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(y, x,"RASPBERRY DASHBOARD v1.0")
    stdscr.attroff(curses.color_pair(3))
    stdscr.attron(curses.color_pair(0))
    stdscr.addstr(y, x+63,"(Q to EXIT)")
    stdscr.attroff(curses.color_pair(0))
    y+=2
    s = stdscr.subwin(30, 79, 0, 0)
    s.box()
    s.hline(2, 1, curses.ACS_HLINE, 77)
    s.hline(17, 1, curses.ACS_HLINE, 77)
    s.refresh()
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(y, x,"ALARME PRESENCE")
    stdscr.addstr(y, x+20,str(rasp.BoutonPresence.Value))
    stdscr.attroff(curses.color_pair(4))
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(y, x+40,"ALARME CHAUDIERE")
    stdscr.addstr(y, x+60,str(rasp.BoutonChaudiere.Value))
    stdscr.attroff(curses.color_pair(4))

def print_menu(stdscr, selectedIndex):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    printHeader(stdscr)
    printInputs(stdscr,inputPins[selectedIndex].Name)
    printOutputs(stdscr,'')
    printSondes(stdscr)
    printServerStatus(stdscr)
    printScriptsStatus(stdscr)
    stdscr.refresh()

def getMax():
    if(selectedCategorieIndex == 0 ):
         return len(inputPins)
    elif selectedCategorieIndex == 2 :
        return len(scripts)
    else :
        return 1

def executeAction(index,actionIndex):
    script = scripts[index]
    action = script.Actions[actionIndex]
    if(action == "STOP"):
        script.stop()
    elif(action == "START"):
        script.start()
    elif (action == "RESTART"):
        script.restart()

def main(stdscr):
    global selectedCategorieIndex
    global index
    global selectedAction
    global selectedActionIndex 

    curses.halfdelay(5)           # How many tenths of a second are waited, from 1 to 255
    curses.noecho()
    # turn off cursor blinking
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    selectedCategorieIndex = 0
    index = 0
    selectedActionIndex = 0
    # print the menu
    print_menu(stdscr, index)
    

    max = 0
    while 1:
        key = stdscr.getch()
        max = getMax()
        if key == curses.KEY_UP and index > 0:
            selectedActionIndex = 0
            index -= 1
        elif key == curses.KEY_DOWN and index < max-1:
            selectedActionIndex = 0
            index += 1
        elif key == ord('0') and selectedCategorieIndex==0:
            inputPins[index].debugOutput('0')
        elif key == ord('1') and selectedCategorieIndex==0 :
            inputPins[index].debugOutput('1')
        elif key == ord('q') or  key == ord('Q'):
            break
        elif key == ord('\t'):
            selectedCategorieIndex+=1
            index = 0
            selectedActionIndex = 0
            if selectedCategorieIndex >len(categories)-1 :
                selectedCategorieIndex = 0
        elif key == curses.KEY_RIGHT and selectedCategorieIndex==2 :
            selectedActionIndex+=1
            if(selectedActionIndex > len(scripts[index].Actions)-1):
                selectedActionIndex = len(scripts[index].Actions)-1
        elif key == curses.KEY_LEFT and selectedCategorieIndex==2 :
            selectedActionIndex-=1
            if(selectedActionIndex < 0 ):
                selectedActionIndex = 0
        elif (key == curses.KEY_ENTER or key == 10 ) and selectedCategorieIndex ==2 :
            executeAction(index,selectedActionIndex)
            selectedActionIndex = 0
            
            
            
       
        print_menu(stdscr, index)
        

curses.wrapper(main)