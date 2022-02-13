from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import config
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
    try:
        cursor = mysql.connect.cursor()
        cursor.execute("select name from plant where crop = true")
        crops = cursor.fetchall()
        cursor.execute("select name from plant where crop = false")
        weeds= cursor.fetchall()
        cursor.close()
    except Exception as e:  # catches random errors
        return render_template("index.html")
    return render_template("index.html", cropIdList=cropIdList, weedIdList=weedIdList, crops=crops, weeds = weeds)

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        gotData = False
        report = None
        crops ="\'{}\'".format(request.form["crop1"])
        for i in range(2,cropIdList+1):
            value = request.form["crop{}".format(i)]
            if value != "none":
                crops= crops+"\'{}\'".format()
        weeds ="\'{}\'".format(request.form["weed1"])
        
        for i in range(2,weedIdList+1):
            value = request.form["weed{}".format(i)]
            if value != "none":
                weeds= weeds+"\',{}\'".format(request.form["weed{}".format(i)])
        print(crops)
        print(weeds)
        numOfAcres = request.form["numAcr"]
        #session['numOfAcres']= numOfAcres
        try:
            cursor = mysql.connect.cursor()
           #cursor.callproc('addLocation', (session['username'], loc, date, time))
            
            cursor.execute("select * from spray")
            cursor.close()
        except:
            print("Robert Cain has taken over the world!!")  # share on discord
    return render_template("result.html", gotData=gotData, data=report)

@app.route('/spray/<spray>')
def calcSpray(spray):
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)