from fileinput import filename
from ipaddress import AddressValueError
import pandas as pd
import numpy
import mysql.connector
import config

def addPlantNames(cursor,plants,isCrop):
    values ='INSERT INTO plant (name, crop) values '
    for plant in plants :
        values=values+"('{}',{}),\n".format((plant[0]).lower(),isCrop)
    values = values[:-2] # rmoves extra comma
    #print(values)
    try:
        cursor.execute(values)
    except Exception as e:
       print("error in add plants")
       print(e)
    return

def addSprays(cursor,sprays):
    values ='INSERT INTO spray (name,price) values '
    for spray in sprays:
        values = values +"('{}',{}),\n".format( (spray[0]).lower(),spray[1])
    values = values[:-2]
    try:
        cursor.execute(values)
    except Exception as e:
        print("error in add sprays")
        print(e)
        print(values+";")
    return
def addCropSprayData(cursor,data):
    cropNames=[]
    sprayNames=[]
    try:
        cursor.execute("select name from plant where crop=True")
        cropQueryResult = cursor.fetchall()
        cursor.execute("select name from spray")
        sprayQueryResult=cursor.fetchall()
        
        for weed in cropQueryResult:
            cropNames.append(weed[0])
        
        for spray in sprayQueryResult:
            sprayNames.append(spray[0])
    
    except Exception as e:
        print(e)
    insertString = ''
    
    for row in data:
        row = list(row)
        spray = row[0].lower()
        crop = row[1].lower()
        if spray in sprayNames and crop in cropNames:
            insertString=insertString+"('{}','{}',{}),\n".format(spray ,crop,row[2])
    if len(insertString)>1:
        try:
            insertString ="Insert INTO CropSprayData (sprayName,plantName,pintsPerAcre) values \n"+insertString[:-2]
            cursor.execute(insertString)
        except Exception as e:
            print("execption in add crop spray data")
            print(e)
            print(insertString)
    return
def addWeedSprayData(cursor,data):
    weedNames=[]
    sprayNames=[]
    try:
        cursor.execute("select name from plant where crop<>True")
        weedQueryResult = cursor.fetchall()
        cursor.execute("select name from spray")
        sprayQueryResult=cursor.fetchall()
        
        for weed in weedQueryResult:
            weedNames.append(weed[0])
        
        for spray in sprayQueryResult:
            sprayNames.append(spray[0])
    except Exception as e:
        print(e)
    insertString=""
    for row in data:
        spray=(row[0]).lower()
        weeds = list(row[1:])
        if numpy.nan in weeds:
            weeds=weeds[:weeds.index(numpy.nan)]

        if spray in sprayNames:
            for weed in weeds:
                weed=weed.lower()
                if weed in weedNames:
                    insertString= insertString+"('{}','{}'),\n".format(spray,weed)
    if len(insertString)>0:
        try:
            insertString = "Insert into WeedSprayData (sprayName,plantName) values\n"+insertString[:-2]
            #print(insertString+";")
            cursor.execute(insertString)
        except Exception as e:
            print("execption in add weed spray data")
            print(e)
            print (insertString+";")
    return;

def run(filename):
    mydb = mysql.connector.connect(host=config.host,user =config.user,password  =config.password,database  =config.database)
    with mydb.cursor() as cursor:
        try:
            cursor.execute("delete from CropSprayData where True = True")
            cursor.execute("delete from WeedSprayData where True = True")
            cursor.execute("delete from plant where True = True")
            cursor.execute("delete from spray where True = True")
            cursor.execute("delete from users where True = True")
        except Exception as e:
            print(e)
        mydb.commit()
        cursor.execute("Insert into users (username, passwd) values ('CPS','CPS'), ('Loveland','Loveland')")
        with pd.ExcelFile(filename) as xls:
        #add crop names
            cropNames =(pd.read_excel(xls,'Crop Names')).values
            addPlantNames(cursor,cropNames,True)
        #add weeds to weeds table
            weedNames = (pd.read_excel(xls,'Weed Names')).values
            addPlantNames(cursor,weedNames,False)
        #add sprays
            sprayNames=(pd.read_excel(xls,'Spray Names')).values
            addSprays(cursor,sprayNames)
        #add sprayData for crops
            cropsSpray=(pd.read_excel(xls,'SafeOn')).values
            addCropSprayData(cursor,cropsSpray)
        #add sprayData for weeds         
            weedsSpray = (pd.read_excel(xls,'Kill').T).values
            addWeedSprayData(cursor,weedsSpray)

        mydb.commit()
if __name__=='__main__':
    run('SprayData.xlsx')