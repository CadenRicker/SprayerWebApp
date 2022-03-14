from ast import Num
import string
import sys
from typing import Any
from urllib.request import Request
from flask_mysqldb import MySQL
from numpy import number
def getCrops(mysql):
    cropList = None
    try:
        cursor = mysql.connect.cursor()
        cursor.execute("select name, crop from plant where crop = true")
        cropList =[]
        for (crop, isCrop) in cursor:
                cropList.append(crop)		
    except Exception as e:  # catches random errors
        print(e)
    return cropList
def requestPlant(request: Request ,plant: string, numberOfCrops):
    plants =["{}".format(request.form["{}1".format(plant)])]
    for i in range(2,numberOfCrops+1):
        value = request.form["{}{}".format(plant,i)]
        if value != "none":
            plants.append("{}".format(value))
    return plants
def getWeeds(mysql: MySQL, crops):
    cursor = mysql.connect.cursor()
    weeds =[]		
    
    equalQuery = ""
    subQuery = ""
    ident = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    i = 0
    for crop in crops:
        subQuery = subQuery+"(select sprayName from CropSprayData where plantName = '{}') as {},".format(crop,ident[i])
        equalQuery = equalQuery+"a.sprayName ={}.sprayName and ".format(ident[i])
        i=i+1
    subQuery = subQuery[:-1]
    equalQuery= equalQuery[:-5]
    query =""
    query1=""
    sprayQuery='('
    try:
        query1 ="select a.sprayName from {} where {}".format(subQuery,equalQuery)
        cursor.execute(query1)            
        sprays = cursor.fetchall()
        sprayNames=[]
        for spray in sprays:
            sprayNames.append(spray[0])
            sprayQuery= sprayQuery+"'{}',".format(spray[0])
        sprayQuery=sprayQuery[:-1]+")"		
        query ="select Distinct(w.plantName) from WeedSprayData as w where w.sprayName in {}".format(sprayQuery)
    except Exception as e:
        print(e)
        print(query1)
    try: 
        cursor.execute(query)
        weedNames= cursor.fetchall()
        cursor.close()
        for weed in weedNames:
            weeds.append(weed[0])
    except Exception as e:
        print(e)
        print(query)
    return weeds, crops,sprayQuery
def requestWeeds(request, numberOFWeeds):
    weeds ="("   
    for i in range(1,numberOFWeeds+1):
        value = request.form["weed{}".format(i)]
        if value != "none" :
            weeds=weeds+"'{}',".format(value)
    weeds=weeds[:-1]+")"
    return weeds
def getSprays(mysql: MySQL,crops, sprays, weeds):
    sprayQuery= sprays
    report =None
    cursor = mysql.connect.cursor()
    try:
        query="select sprayName, plantName, price from WeedSprayData as weed, spray where  spray.name = weed.sprayName and weed.plantName in {} and weed.sprayName in {} order by weed.sprayName".format(weeds,sprayQuery)
        cursor.execute(query)
        result=cursor.fetchall()
        report =filterQuery(result=result)					
    except Exception as e:
        print(e)
    fullReport=[]
    try:
        listOfCrops = "("
        for crop in crops:
            listOfCrops="{}'{}',".format(listOfCrops,crop)
        listOfCrops = listOfCrops[:-1]+")"
        for row in report:
            query="SELECT MIN(pintsPerAcre) from CropSprayData where sprayName='{}' and plantName in {}".format(row[0],listOfCrops)
            cursor.execute(query)
            result=cursor.fetchone()
            ppa =  "{:.2f}".format(result[0])
            row.append(ppa)            
            fullReport.append(row)
    except Exception as e:
        print(e)
        print("exception")
    return  fullReport

def sortByList(list1,list2):
    zipped_lists = zip(list1, list2)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    list1, list2 = [ list(tuple) for tuple in  tuples]
    return list2
def filterQuery(result):
    weeds = []
    last = result[0][0]
    sprayNames =[last]
    sprayPrices = [result[0][2]]
    weedRow =[]
    orderByList =[]
    for row in result:            
        if last==row[0]:
            weedRow.append(row[1])
        else:
            last=row[0]
            weeds.append(weedRow)
            orderByList.append(len(weedRow))
            weedRow=[row[1]]
            sprayNames.append(last)
            sprayPrices.append(row[2])
           
    weeds.append(weedRow)
    zippedList =list(zip(sprayNames,sprayPrices,weeds))
    orderByList.append(len(weedRow))
    zippedList = sortByList(orderByList,zippedList)
    filtterd =[]
    for row in zippedList:
        tmpRow =[row[0],"{:.2f}".format(row[1]),row[2]]
        filtterd.append(tmpRow)
    return filtterd
def calculateResult(sprayName, sprayData, acerage, sprayGPA,tankSize):
    report =None
    info = None
    for row in sprayData:
        if row[0] == sprayName:
            info = row
            break
    if info == None:
        return None
    price =float(info[1])
    ppa = float(info[3])
    pintsToGallons = float(0.125)
    gallonsOfSpray =ppa*pintsToGallons*float(acerage)
    cost = gallonsOfSpray*float(price)
    totalGallons = float(acerage) * float(sprayGPA)
    ratio = gallonsOfSpray/totalGallons
    lastTank = int(totalGallons)%int(tankSize)
    numberOFFullTanks = (totalGallons-float(lastTank))/float(tankSize)
    sprayPerFullTank = round(float(tankSize)*ratio,4)
    sparyPerPartTank = round(float(lastTank)*ratio,4)
    report = [sprayName, gallonsOfSpray, cost,[numberOFFullTanks,sprayPerFullTank],
              [sparyPerPartTank,(float(lastTank)-sparyPerPartTank)]]
    return report
def getPlantNames(mysql: MySQL):
    crops =[]
    weeds =[]
    try:	
        with mysql.connect.cursor() as cursor:
            cursor.execute("select name, crop from plant")
            for (name,crop) in cursor:
                if crop:
                    crops.append(name)
                else:
                    weeds.append(name)
    except Exception as e:
        print(e)
    return crops, weeds
def addSpray(mysql: MySQL,spray: string,price: float, crops: list, cropPPA, weeds: list):
    try:
        with mysql.connect.cursor() as cursor:    
            cursor.callproc('addspray',(spray,price))
            result = mysql.connection.commit()  
            cursor.close()
        with mysql.connect.cursor() as cursor:
            for crop,ppa in list(zip(crops,cropPPA)):
                cursor.callproc('addCropToSpray',(crop,spray,ppa))
            for weed in weeds:
                cursor.callproc('addWeedToSpray',(weed,spray))
            mysql.connection.commit()
        return True
    except Exception as e:
        print(e)
        return False