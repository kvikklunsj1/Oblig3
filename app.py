import mysql.connector
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from db import createTablesInDatabase #fra db.py

dbconfig = { 'host': '127.0.0.1',
    'user': 'user',
    'password': 'test',
    'database': 'myDb', }

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleaseworkthistime'

#fra db.py, sjekker om alle tabellene eksiterer, og lager dem om nødvendig
createTablesInDatabase()
    

class regAdmin(FlaskForm):
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Enter username", "class": "textinput"})
    fornavn = StringField('fornavn' , validators=[DataRequired()], render_kw={"placeholder": "Fornavn", "class": "textinput"})
    etternavn = StringField('etternavn' , validators=[DataRequired()], render_kw={"placeholder": "Etternavn", "class": "textinput"})
    passord = PasswordField('passord' , validators=[DataRequired()], render_kw={"placeholder": "Passord", "class": "textinput"})


class regNormal(FlaskForm):
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Enter username", "class": "textinput"})
    passord = PasswordField('passord' , validators=[DataRequired()], render_kw={"placeholder": "Passord", "class": "textinput"})



@app.route("/", methods=['GET', 'POST'])
def login():
    loginormalForm = regNormal()
    if loginormalForm.validate_on_submit():
        conn = mysql.connector.connect(**dbconfig) #kontakt med db
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (loginormalForm.username.data,))
        userInfo = cursor.fetchone()
        what = cursor.fetchall() #nødfiks for at koden ikke skal ødelegg
        cursor.close()
        conn.close()
        if userInfo and check_password_hash(userInfo[2], loginormalForm.passord.data):
            user = userInfo[0]
            session['userID'] = user #bruker PK fra databasen som ID
            return redirect(url_for('quiz'))
        else:
            flash("Ugyldig brukernavn eller passord!")
    return render_template("home.html", login=loginormalForm)



@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if 'userID' not in session:
        flash("Vennligst logg inn!")
        return redirect(url_for(""))
    else:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT quiz_name FROM quiz')


        return render_template("quiz.html")
    



@app.route("/usertype", methods=['GET', 'POST'])
def usertype():
    return render_template("usertype.html")



@app.route("/submitKontovalg", methods=['POST'])
def submitKontovalg():
    valg =  request.form["brukertype"]
    return redirect(valg)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    adminForm = regAdmin()
    if adminForm.validate_on_submit():
        passwordhash = generate_password_hash(adminForm.passord.data, method='sha256')
        
        conn = mysql.connector.connect(**dbconfig) #kontakt med db
        cursor = conn.cursor() #lager en cursor som skal utføre spørringer
        inserNewUser = """INSERT INTO adminUser (username, fornavn, etternavn, hashedpassword) VALUES (%s, %s, %s, %s)""" #genererer sql-setning
        values = (adminForm.username.data, adminForm.fornavn.data, adminForm.etternavn.data, passwordhash) #det som skal settes inn i DB
        cursor.execute(inserNewUser, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "takk, du er nå regga, bror"
    return render_template("registrerAdmin.html", admin=adminForm)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    return render_template("adminlogin.html")



    
@app.route("/regnormal", methods=['GET', 'POST'])
def normal():
    normalForm = regNormal()
    if normalForm.validate_on_submit():
        passwordhash = generate_password_hash(normalForm.passord.data, method='sha256')

        conn = mysql.connector.connect(**dbconfig) 
        cursor = conn.cursor()
        inserNewUser = """INSERT INTO user (username, hashedpassword) VALUES (%s, %s)"""
        values = (normalForm.username.data, passwordhash)
        cursor.execute(inserNewUser, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "bruker registrert"    
    return render_template("regnormal.html", normal=normalForm) #Må fikses
    




if __name__ == "__main__":
    app.run(debug=True)



