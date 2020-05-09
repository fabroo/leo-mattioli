import os

from flask import Flask, request, render_template, send_from_directory, flash

__author__ = 'ibininja'

import sys
from pathlib import Path
import gmail


sys.path.insert(1, os.getcwd())
#Import .py files
import predictV2
import inputId
import addExtraPics
import trainPeroBien
import trainPorSiAlgoAndaMal
import check
import check_2
import remove
import newUser
import sqlite3
import smtplib
from email.mime.text import MIMEText
#
import ssl
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/upload", methods=["GET","POST"])
def upload():
    return render_template('upload.html')
    text = request.form['text']

    KNOWN_NAMES = f'{os.getcwd()}/fotos/'
    existe = False

    target = os.path.join(APP_ROOT,'images/'+str(text)+'')
    print(target)
    
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))


    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    for folder_name in KNOWN_NAMES:
        if text == folder_name:
            existe = True
    
    try:
        if existe:
            print('Ya existe un directorio con tu nombre, agregando nuevas fotos...')
            addExtraPics.nuevasFotos(text) #usa el autocomplete, y esta funcion toma name como argumento
            flash('Ya se ejecutó y todo salio bien segui viviendo')
        else:
            print('Nuevo directorio, entrenando reconocimiento facial...')
            trainPeroBien.trainearBien()#creo que era??
            flash('Ya se ejecutó y todo salio bien segui viviendo')
    except:
         flash('Amigo se cayo todo sorry cambia de empresa..')
    
    
    return render_template("upload.html", image_name=filename)


@app.route("/login",methods = ["GET","POST"])
def login():
    # return render_template("login.html")
    try:
        user = request.form['user']
        password = request.form['password']
        print(user)
        print(password)
        if inputId.inputear(password,user):
            flash('Bienvenido, '+user+' que te contas?')
            return render_template('home.html')
             

        else:
            flash('not a valid username!, try again','warning')
        return render_template('login.html')
    except Exception as err:
        print('ESTE ES EL ERROR REY E' +str(err))
        return render_template('login.html')

@app.route("/register",methods = ["GET","POST"])
def register():
    
    # full_filename = f'{os.getcwd()}/fotos/bren_mom/brenmomm (1).jpeg' #os.path.join('\fotos\bren', '1.jpeg')
    
    # return render_template("register.html", user_image = full_filename)

    

    try:
        idCompany = request.form.get('companyid',False)
        dni = request.form.get('dni',False)
        email = request.form.get('mail',False)
        fullname = request.form.get('fullname',False)
        if newUser.agregarUsuario(dni, fullname, email, idCompany):
            flash("Cuenta creada con exito. Inicia Sesion arriba a la derecha. Bienvenido!")
        else:
            flash("P  E  B  E  T  E")
    except Exception as err:
        print('ESTE ES EL ERROR REY E' +str(err))
    return render_template('register.html')




@app.route("/home",methods = ["GET","POST"])
def home():
    try:
        return render_template('home.html')
    except:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
