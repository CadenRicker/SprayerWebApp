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
	""" loads index.html

	Returns:
		_type_: jinja template
	"""
	return render_template("index.html")
# Crop page
@app.route("/crop", methods=['POST', 'GET'])
def crop():	
	""" reads the input from index.html form and saves it to the session
	it then renders the corp.html with the crop list from the database.

	Returns:
		_type_: html template or redirects to home
	"""
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
	"""reads form from crop.html and then renders weed.html with weeds that have sprays
	that are safe on the crops.

	Returns:
		_type_: _description_
	"""
	if request.method == 'POST':
		weeds, session['crops'], session['sprays'] = getWeeds(mysql=mysql, 
														crops=requestPlant(request=request,plant='crop', numberOfCrops=cropIdList))
		return render_template("weed.html",  weedIdList=weedIdList, weeds = weeds)      
	return redirect(url_for('crop'))
#Spray page
@app.route('/spray', methods=['POST', 'GET'])
def spray():
	"""reads form from weed.html and uses weed list and crop list to select viable sprays.
	then renders template for spray.html

	Returns:
		_type_: spray.html
	"""
	if request.method == 'POST':
		fullReport = getReport(mysql=mysql,crops=session['crops'],sprays=session['sprays'],
						 weeds=requestWeeds(request=request,numberOFWeeds=weedIdList))
		session['sprayReport']=fullReport
		return render_template("spray.html", data=fullReport,numAcr = session['numOfAcr'])
	return redirect(url_for('weed'))
#Result Page
@app.route('/spray/<spray>')
def calcSpray(spray):
	"""uses the spray name generate the report

	Args:
		spray (string): name of spray selected

	Returns:
		_type_: result.html
	"""
	report = calculateResult(spray, session['sprayReport'], session['numOfAcr'],
							 session['GPA'], session['tankSize'])
	return render_template("result.html", report = report)

@app.route('/login')
def loadLogin():
	"""loads the login.html

	Returns:
		_type_: login.html
	"""
	return render_template("login.html")

@app.route('/validateLogin', methods=['POST', 'GET'])
def validateLogin():
	""" reads form from login.html username and password. If the user name and password are valid
		redirct user to addSpray otherwise redirects user to login.

	Returns:
		_type_: redirct url
	"""    
	uName = request.form['username']
	pWord = request.form['password']
	cursor = mysql.connection.cursor()

	cursor.execute("SELECT username FROM users WHERE username = %s AND passwd = %s", (uName, pWord))
	for (username) in cursor:
		session['username'] = username
		cursor.close()
		session['added'] = False
		return redirect(url_for('add'))
	cursor.close()
	return render_template("login.html", invalid=True)
@app.route('/add')
def add():
	"""renders addSpray.html with weed and crop names from the database

	Returns:
		_type: addSpray.html
	"""
	cropNames, weedNames = getPlantNames(mysql)
	added = session['added']
	session['added']=False
	return render_template('addSpray.html',crops=cropNames,weeds=weedNames,
						   cropIdList=maxNumberOfCrops,weedIdList=maxNumberOfWeeds,added = added)

@app.route('/add/spray', methods=['POST','GET'])
def sqladdSpray():
	"""reads form from addSpray.html and adds the spray and data to the database.
		on a successful addition it redirects to add spray.
		on failure returns user to /

	Returns:
		_type_: redirect
	"""
	if request.method == 'POST':
		success = addSpray( mysql=mysql,spray="{}".format(request.form['spray']), price=float(request.form['price']),
						   crops=requestPlant(request=request,plant='crop', numberOfCrops=maxNumberOfCrops),
						   cropPPA=requestPlant(request=request,plant='cropPPA',numberOfCrops=maxNumberOfCrops),
						   weeds=requestPlant(request=request,plant='weed', numberOfCrops=maxNumberOfWeeds))
		if success== True:
			session['added'] = True
			return redirect(url_for('add'))
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)