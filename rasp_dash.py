import curses
from myRaspberry import MyRaspberry
from raspberry import Raspberry
import threading, time, datetime

rasp = MyRaspberry()
rasp.setup()
rasp.BoutonChaudiere.deactivateEvents()
rasp.BoutonPresence.deactivateEvents()
rasp.initStates()

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
        printElement(stdscr,element,x,y,selectedName==element.Name)
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

def printHeader(stdscr):
    y = 1
    x = 2
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(y, x,"RASPBERRY DASHBOARD v1.0")
    stdscr.attroff(curses.color_pair(3))
    y+=2
    s = stdscr.subwin(23, 79, 0, 0)
    s.box()
    s.hline(2, 1, curses.ACS_HLINE, 77)
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
    stdscr.refresh()




def main(stdscr):
    curses.halfdelay(5)           # How many tenths of a second are waited, from 1 to 255
    curses.noecho()
    # turn off cursor blinking
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    index = 0
    # print the menu
    print_menu(stdscr, index)
    


    while 1:
        key = stdscr.getch()

        if key == curses.KEY_UP and index > 0:
            index -= 1
        elif key == curses.KEY_DOWN and index < len(inputPins)-1:
             index += 1
        elif key == ord('0'):
            inputPins[index].debugOutput('0')
        elif key == ord('1') :
            inputPins[index].debugOutput('1')
        elif key == ord('q') or  key == ord('Q'):
            break
       
        print_menu(stdscr, index)
        

curses.wrapper(main)