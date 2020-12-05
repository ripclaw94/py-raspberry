

def readFile(filename ):
    contenu =''
    f=None
    try:
        f = open(filename,"r", encoding = 'utf-8')
        contenu = f.read()
    except:
        contenu = ''
    finally:
        if(f!=None):
            f.close()
    return contenu

def writeFile(filename, value):
    success = True
    f=None
    try:
        f = open(filename,"w+", encoding = 'utf-8')
        f.write(value)
    except:
        success=False
    finally:
        if(f!=None):
            f.close()
    return success


    