from ipaddress import AddressValueError
import pandas as pd
import numpy
import mysql.connector
import config

def addPlantNames(cursor,plants,isCrop):
    lists=[]
    values ='INSERT INTO plant (name, crop) values '
    for plant in plants :
        values=values+"('{}',{}),".format(plant[0],isCrop)
        lists.append(plant[0])
    values = values[:-1] # rmoves extra comma
    try:
        cursor.execute(values)
    except Exception as e:
        print(e)
    return lists


def addSprays(cursor,sprays):
    values ='INSERT INTO spray (name,price) values '
    for spray in sprays:
        values = values +"('{}',{}),".format(spray[0],spray[1])
    values = values[:-1]
    try:
        cursor.execute(values)
    except Exception as e:
        print(e)
    return

def addSprayData(cursor,data,safe,lists):
    cursor.execute("Select name from spray")
    queryresult=list(cursor.fetchall())
    sprayNames=[]
    for name in queryresult:
        sprayNames.append(name[0])
    for sprayData in data:
        sprays = list(sprayData[:10])
        sprays = sprays[:sprays.index(numpy.nan)]
        plants = list(sprayData[10:])
        if numpy.nan in plants:
            plants = plants[:plants.index(numpy.nan)]
        
        insertStr = 'INSERT INTO SprayData (sprayName,plantName,safes) values '
        values = ''
        addedValues=[]
        for plant in plants:
            string ="('@','{}',{}),\n".format(plant,safe)
            if plant in lists and string not in addedValues :
                values = values+string
                addedValues.append(string)
        fValues =''
        addedSprays =[]      
        for spray in sprays:
            if spray in sprayNames and spray not in addedSprays:
                fValues = fValues + values.replace('@',spray)
                addedSprays.append(spray)
        fValues=insertStr+fValues[:-2]
        
        try:
            if len(fValues)>len(insertStr)+5:
                cursor.execute(fValues)
        except Exception as e:
           print(e)
    return

        
def main():
    mydb = mysql.connector.connect(host=config.host,user =config.user,password  =config.password,database  =config.database)
    with mydb.cursor() as cursor:
        try:
            cursor.execute("delete from SprayData where True = True")
            cursor.execute("delete from plant where True = True")
            cursor.execute("delete from spray where True = True")
            cursor.execute("delete from SprayData where True = True")
        except Exception as e:
            print(e)
        mydb.commit()
        with pd.ExcelFile('SprayData.xlsx') as xls:
            plantList=[]
        #add crop names
            cropNames =(pd.read_excel(xls,'Crop Names')).values
            plantList =addPlantNames(cursor,cropNames,True)
        #add weeds to weeds table
            weedNames = (pd.read_excel(xls,'Weed Names')).values
            plantList = plantList+ addPlantNames(cursor,weedNames,False)
        #add sprays
            sprayNames=(pd.read_excel(xls,'Spray Names')).values
            addSprays(cursor,sprayNames)
        #add sprayData for crops
            cropsSpray=(pd.read_excel(xls,'SafeOn').T).values
            addSprayData(cursor,cropsSpray,True,plantList)
        #add sprayData for weeds         
            weedsSpray = (pd.read_excel(xls,'Kill').T).values
            addSprayData(cursor,weedsSpray,False,plantList)

        mydb.commit()
if __name__=='__main__':
    main()