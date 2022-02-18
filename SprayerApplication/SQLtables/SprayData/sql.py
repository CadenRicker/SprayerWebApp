from ipaddress import AddressValueError
import pandas as pd
import numpy
import mysql.connector
import config
mydb = mysql.connector.connect(host=config.host,user =config.user,password  =config.password,database  =config.database)


with mydb.cursor() as cursor:
    cursor.execute("delete from SpraySafe where TRUE = TRUE")
    cursor.execute("delete from plant where TRUE = TRUE")
    cursor.execute("delete from spray where TRUE = TRUE")
    mydb.commit()
    with pd.ExcelFile('SprayData.xlsx') as xls:
        cropNames =pd.read_excel(xls,'Crop Names')
        values ='INSERT INTO plant (name, crop) values '
        for crop in cropNames.values :
            values=values+"('{}',TRUE),".format(crop[0])
        values = values[:-1]
        try:
            cursor.execute(values)
        except Exception as e:
            print(e)
        values ='INSERT INTO plant (name, crop) values '
        print("here")
        weedNames = pd.read_excel(xls,'Weed Names')
        for weed in weedNames.values :
            values=values+"('{}',False),".format(weed[0])
        values = values[:-1]
        try:
            cursor.execute(values)
        except Exception as e:
            print(e)
        
        cropsSpray=(pd.read_excel(xls,'SafeOn').T).values
        for sprayData in cropsSpray:
            sprays = list(sprayData[:10])
            sprays = sprays[:sprays.index(numpy.nan)]
            plants = list(sprayData[10:])
            for plant in plants:
            try:
                plants = plants[:plants.index(numpy.nan)]
                print(plants)
            except Exception as e:
                print("Empty array")
        for plant in plants:
        weedSpray = pd.read_excel(xls,'Kill')
    mydb.commit()
    