from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from SprayerApplication.queryFunctions import filterQuery
import config
import queryFunctions
SECRET_KEY = 'GDtfDCFYjD'
app = Flask(__name__,
            instance_relative_config=False,
            template_folder="templates",
            static_folder="static")
app.config['MYSQL_HOST'] = config.host
app.config['MYSQL_USER'] = config.user
app.config['MYSQL_PASSWORD'] = config.password
app.config['MYSQL_DB'] = config.database
mysql = MySQL(app)
app.secret_key = 'abc'
cropIdList=3
weedIdList=5
# Home Page
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/crop")
def crop():
    try:
        cursor = mysql.connect.cursor()
        cursor.execute("select name from plant where crop = true")
        crops = cursor.fetchall()
        
    except Exception as e:  # catches random errors
        return render_template("index.html")
    return render_template("crop.html", cropIdList=cropIdList, crops=crops)

@app.route('/weed', methods=['POST', 'GET'])
def weed():
    cursor = mysql.connect.cursor()
    weeds =[]
    if request.method == 'POST':
        gotData = False
        report = None
        crops =["'{}'".format(request.form["crop1"])]
        for i in range(2,cropIdList+1):
            value = request.form["crop{}".format(i)]
            if value != "none":
                crops.append("{}".format(value))
        equalQuery = ""
        subQuery = ""
        ident = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        i = 0
        for crop in crops:
            subQuery = subQuery+"(select sprayName from CropSprayData where plantName = '{}') as {},".format(crop,ident[i])
            equalQuery = equalQuery+"a.plantName ={}.plantName and ".format(ident[i])
            i=i+1
        subQuery = subQuery[:-1]
        equalQuery= equalQuery[:-5]
        cursor.execute("select a.sprayName from {} where {}".format(subQuery,equalQuery))
        sprays = cursor.fetchall()
        sprayQuery='('
        sprayNames=[]
        for spray in sprays:
            sprayNames.append(spray[0])
            sprayQuery= sprayQuery+"'{}',".format(spray[0])
        sprayQuery=sprayQuery[:-1]+")"
        session['sprays']=sprayQuery
        cursor.execute("select WeedSprayData.plantName from WeedSprayData as w where w.sprayName in {}".format(sprayQuery))
        weedNames= cursor.fetchall()
        cursor.close()
        for weed in weedNames:
            weeds.append(weed[0])

    return render_template("weed.html",  weedIdList=weedIdList, weeds = weeds)

        
        
        

@app.route('/spray', methods=['POST', 'GET'])
def spray():
    weeds ="("   
    for i in range(1,weedIdList+1):
        value = request.form["weed{}".format(i)]
        if value != "none":
            weeds=weeds+"'{}',".format(value)
    weeds=weeds[:-1]+")"
    sprayQuery= session['sprays']

    try:
        cursor = mysql.connect.cursor()
        query="select sprayName, plantName, price from WeedSprayData as weed, spray where  spray.name = weed.sprayName and weed.plantName in {} and weed.sprayName in {}".format(weeds,sprayQuery)
        cursor.execute(query)
        result=cursor.fetchall()
        cursor.close()
        filterQuery(result=result)
        
        
    except Exception as e:
        print(e)  # share on discord
    return render_template("result.html", data=report)

@app.route('/spray/<spray>')
def calcSpray(spray):

    return spray

if __name__ == '__main__':
    app.run(debug=True)