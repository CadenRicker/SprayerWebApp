from crypt import methods
from unittest import result
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from numpy import place
import config
from supportFunctions import *
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
maxNumberOfCrops=100
maxNumberOfWeeds=100
# Home Page
@app.route("/")
def index():
	return render_template("index.html")
# Crop page
@app.route("/crop", methods=['POST', 'GET'])
def crop():	
	if request.method == 'POST':
		session['numOfAcr']=request.form['numAcr']
		session['GPA']=request.form['GPA']
		session['tankSize']=request.form['tankSizeG']
		crops= getCrops(mysql=mysql)
		return render_template("crop.html", cropIdList=cropIdList, crops=crops)
	return redirect(url_for(''))
#Weed Page
@app.route('/weed', methods=['POST', 'GET'])
def weed():
	if request.method == 'POST':
		weeds, session['crops'], session['sprays'] = getWeeds(mysql=mysql, 
														crops=requestPlant(request=request,plant='crop', numberOfCrops=cropIdList))
		return render_template("weed.html",  weedIdList=weedIdList, weeds = weeds)      
	return redirect(url_for('crop'))
#Spray pave
@app.route('/spray', methods=['POST', 'GET'])
def spray():
	if request.method == 'POST':
		fullReport = getSprays(mysql=mysql,crops=session['crops'],sprays=session['sprays'],
						 weeds=requestWeeds(request=request,numberOFWeeds=weedIdList))
		session['fullReport']=fullReport
		return render_template("spray.html", data=fullReport,numAcr = session['numOfAcr'])
	return redirect(url_for('weed'))
#Result Page
@app.route('/spray/<spray>')
def calcSpray(spray):
	report = calculateResult(spray, session['sprayReport'], session['numOfAcr'],
							 session['GPA'], session['tankSize'])
	return render_template("result.html", report = report)

@app.route('/login')
def loadLogin():
	return render_template("login.html")
# validates login and loads template for either:
# regular users 
# admin users 
@app.route('/validateLogin', methods=['POST', 'GET'])
def load_menu():
	uName = request.form['username']
	pWord = request.form['password']
	cursor = mysql.connection.cursor()

	cursor.execute("SELECT username FROM users WHERE username = %s AND passwd = %s", (uName, pWord))
	for (username) in cursor:
		session['username'] = username
		cursor.close()
		return redirect(url_for('add'))
	cursor.close()
	return render_template("login.html", invalid=True)
@app.route('/add')
def add():
	cropNames, weedNames = getPlantNames(mysql)
	return render_template('addSpray.html',crops=cropNames,weeds=weedNames,
						   cropIdList=maxNumberOfCrops,weedIdList=maxNumberOfWeeds)

@app.route('/add/spray', methods=['POST','GET'])
def sqladdSpray():
	if request.method == 'POST':
		success = addSpray( mysql=mysql,spray="{}".format(request.form['spray']), price=float(request.form['price']),
						   crops=requestPlant(request=request,plant='crop', numberOfCrops=maxNumberOfCrops),
						   cropPPA=requestPlant(request=request,plant='cropPPA',numberOfCrops=maxNumberOfCrops),
						   weeds=requestPlant(request=request,plant='weed', numberOfCrops=maxNumberOfWeeds))
		if success== True:
			return redirect(url_for('add'))
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)