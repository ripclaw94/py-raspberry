import sqlite3
import datetime

class DataBaseHelper:
    dbFile = 'gpio.db'
    
    def __init__(self, filename): 
        self.dbFile = filename

    def fetchQuery(self,query):
        rows = []
        try:
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
        except :
            rows = []
        finally:
            conn.close()
        return rows
    
    def fetchOneQuery(self,query):
        rows = []
        try:
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchone()
        except :
            rows = []
        finally:
            conn.close()
        return rows

    def executeQuery(self,query,param):
        ret = True
        try:
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()
            c.execute(query,param)
            conn.commit()
        except :
            ret = False
        finally:
            conn.close()
        return ret

    def getLastTemperaturesOfTable(self,table):
        rows = []
        query = f"select temperature from {table} order by id desc limit 1"
        # print(query)
        rows = self.fetchOneQuery(query)
        return rows[0]

    def getTemperaturesOfDate(self,date:datetime):
        rows = []
        if(date!=None):
            qDate = date.strftime('%Y-%m-%d')
            query = f"""select cast( strftime('%H',t1.date) as INTEGER ) hour, cast(strftime('%M',t1.date) as INTEGER ) minute,
                    t1.temperature temp1,
                    t2.temperature temp2,
                    t3.temperature temp3
                    from temperatures_cave t1,
                        temperatures_chaudiere t2,
                        temperatures_exterieur t3
                    where t1.date = t2.date
                    and   t1.date = t3.date
                    and  strftime('%Y-%m-%d',t1.date) = '{qDate}'
                    order by hour,minute"""
            # print(query)
            rows = self.fetchQuery(query)
        return rows
    
    def getTemperaturesCaveAndRaspOfDate(self,date:datetime):
        rows = []
        if(date!=None):
            qDate = date.strftime('%Y-%m-%d')
            query = f"""select cast( strftime('%H',t1.date) as INTEGER ) hour, cast(strftime('%M',t1.date) as INTEGER ) minute,
                    t1.temperature temp1,
                    t2.temperature temp2
                    from temperatures_chaudiere t1,
                        temperatures_rasp t2
                    where t1.date = t2.date
                    and  strftime('%Y-%m-%d',t1.date) = '{qDate}'
                    order by hour,minute"""
            # print(query)
            rows = self.fetchQuery(query)
        return rows


    def getTemperatureMinMaxCurrent(self,date:datetime):
        rows = []
        temps = {}
        if(date!=None):
            qDate = date.strftime('%Y-%m-%d')
            query = f"""select sum(curCave) as curCave,sum(moyCave) as moyCave,sum(minCave) as minCave,sum(maxCave) maxCave, 
                sum(curChaud) curChaud,sum(moyChaud) moyChaud,sum(minChaud) minChaud,sum(maxChaud) maxChaud,
                sum(curExt) curExt,sum(moyExt) moyExt,sum(minExt) minExt,sum(maxExt) maxExt
                from
                ( 
			   select 0 as curCave,
				round(sum(t1.temperature) / count(t1.id),1) moyCave,
                min(t1.temperature) minCave,
                max(t1.temperature) maxCave,
                0 as curChaud,
				round(sum(t2.temperature) / count(t2.id),1) moyChaud,
                min(t2.temperature) minChaud,
                max(t2.temperature) maxChaud,
                0 as curExt,
				round(sum(t3.temperature) / count(t3.id),2) moyExt,
                min(t3.temperature) minExt,
                max(t3.temperature) maxExt
                from temperatures_cave t1,
                    temperatures_chaudiere t2,
                    temperatures_exterieur t3
                where t1.date = t2.date
                and   t1.date = t3.date
                and  strftime('%Y-%m-%d',t1.date) = '{qDate}'
				union 
                select temperature as curCave,0,0,0,0,0,0,0,0,0,0,0
                from temperatures_cave
                where id = (select max(id) from temperatures_cave )
                union 
                select 0 as curCave,0 as moyCave,0 as minCave,0 as maxCave,temperature as curChaud,0 as moyChaud,0 as moyChaud,0 as maxChaud,0 as curExt,0 as moyExt,0 as minExt,0 as maxExt
                from temperatures_chaudiere
                where id = (select max(id) from temperatures_chaudiere )
                union 
                select 0 as curCave ,0 as moyCave ,0 as minCave,0 as maxCave,0 as curChaud,0 as moyChaud,0 as minChaud,0 as maxChaud,temperature as curExt,0 as moyExt,0 as minExt,0 as maxExt
                from temperatures_exterieur
                where id = (select max(id) from temperatures_exterieur )
                )
                
                """
            # print(query)
            rows = self.fetchOneQuery(query)
            temps['curCave'] = rows[0]
            temps['moyCave'] = rows[1]
            temps['minCave'] = rows[2]
            temps['maxCave'] = rows[3]
            temps['curChaud'] = rows[4]
            temps['moyChaud'] = rows[5]
            temps['minChaud'] = rows[6]
            temps['maxChaud'] = rows[7]
            temps['curExt'] = rows[8]
            temps['moyExt'] = rows[9]
            temps['minExt'] = rows[10]
            temps['maxExt'] = rows[11]
        return temps
        
    def getPasswordAuthentification(self,password):
        row = []
        query = "select password from config"
        # print(query)
        row = self.fetchOneQuery(query)
        result = (row[1]==password)
        return result
    
    def insertTemperature(table, temperature:float, date:datetime):
        self.executeQuery(f"INSERT INTO '{table}' ('date','temperature') values (?,?)",(date,temperature))
    
    def updateDns(ipDns):
        self.executeQuery("update config set ddns_ip = ?",(ipDns,))