from ipaddress import AddressValueError
import pandas as pd
import numpy
import mysql.connector
import config

def addPlantNames(cursor,plants,isCrop):
    values ='INSERT INTO plant (name, crop) values '
    for crop in cropNames.values :
        values=values+"('{}',isCrop),".format(crop[0])
    values = values[:-1] # rmoves extra comma
    try:
        cursor.execute(values)
    except Exception as e:
        print(e)
    return


def addSprays(cursor,sprays):
    values ='INSERT INTO spray (name,price) values '
    for spray in sprays:
        values = values +"({},{}),".format(spray[0],spray[1])
    try:
        cursor.execute(values)
    except Exception as e:
        print(e)
    return

def addSprayData(cursor,data,safe):
    for sprayData in data:
        sprays = list(sprayData[:10])
        sprays = sprays[:sprays.index(numpy.nan)]
        plants = list(sprayData[10:])
        values ='INSERT INTO sprayData (sprayName,plantName,safe) values '
        for plant in plants:
            values = values+"(@,{},{}),".format(plant,safe)
        fValues =''
        for spray in sprays:
            fValues = fValues + values.replace('@',spray)
        print(fValues)
        try:
            cursor.execute(fValues)
        except Exception as e:
            print(e)
    return

        
def main():
    mydb = mysql.connector.connect(host=config.host,user =config.user,password  =config.password,database  =config.database)
    with mydb.cursor() as cursor:
        cursor.execute("delete from SpraySafe where TRUE = TRUE")
        cursor.execute("delete from plant where TRUE = TRUE")
        cursor.execute("delete from spray where TRUE = TRUE")
        mydb.commit()
        with pd.ExcelFile('SprayData.xlsx') as xls:
        #add crop names
            cropNames =(pd.read_excel(xls,'Crop Names')).values
            addPlantNames(cursor,cropNames,TRUE)
        #add weeds to weeds table
            weedNames = (pd.read_excel(xls,'Weed Names')).values
            addPlantNames(cursor,weedNames,FALSE)
        #add sprays
            sprayNames=(pd.read_excel(xls,'Spray Names')).values
            addSprays(cursor,sprayNames)
        #add sprayData for crops
            cropsSpray=(pd.read_excel(xls,'SafeOn').T).values
            addSprayData(cursor,cropsSpray,TRUE)
        #add sprayData for weeds         
            weedSpray = (pd.read_excel(xls,'Kill').T).values
            addSprayData(cursor,cropsSpray,FALSE)

        mydb.commit()
if __name__=='__main__':
    main()