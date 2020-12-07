from IoHelper import readFile


def getTemperatureFromText(text_sonde,factor : int):
    temp = 0.0
    if(factor>0) :
        try:
            index = text_sonde.index("t=")+2
            temp = float(text_sonde[index:])/factor
        except Exception as identifier:
            print(f"exception {identifier}")
            temp = 0.0
    return temp

def getTemperatureRaspberry(fichierRaspberry,factor:int) :
    contenu = readFile(fichierRaspberry)
    temp = 0.0
    if(contenu!=None) :
        try:
            temp = float(contenu)/factor
        except:
            temp=0.0
    return temp


def getTemperatureFromSonde(fichierSonde,factor) :
    contenu = readFile(fichierSonde)
    temp = 0.0
    if(contenu!=None) :
        temp = getTemperatureFromText(contenu,factor)
    return temp










