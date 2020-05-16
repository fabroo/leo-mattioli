import os

from flask import Flask, request, render_template, send_from_directory, flash, g, session, redirect, url_for

__author__ = 'ibininja'

import sys
from pathlib import Path


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

class User:
    def __init__(self, id, fullName, contra, mail):
        self.id = id
        self.fullname = fullName
        self.contra = contra
        self.mail = mail

comm = sqlite3.connect
BASE_DIR = os.getcwd()
db_path = os.path.join(BASE_DIR, "testdb.db")
conn  = sqlite3.connect(db_path)
c = conn.cursor()

c.execute(f'''SELECT * FROM residents''')
pakesepa = c.fetchall()
userList = []
for el in pakesepa:
    userList.append(User(id=str(el[0]),fullName = str(el[1]),contra=str(el[2]),mail=str(el[3])))

@app.route("/")
def index():
    if 'user_id' in session:
        user = [x for x in userList if x.id == session['user_id']][0]
        g.user = user
        return render_template("index_logged.html")
    return render_template("index.html")

@app.before_request
def before_request():
    g.user = None
    
    if 'user_id' in session:
        user = [x for x in userList if x.id == session['user_id']][0]
        g.user = user
  


@app.route("/upload", methods=["GET","POST"])
def upload():
    if not g.user:
        return render_template('login.html')
    else:
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

@app.route('/close_sess', methods=['GET', 'POST'])
def closeSess():
    session.pop('user_id', None)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['user']
        password = request.form['password']
        

        if inputId.inputear(password,username):
            user = [x for x in userList if x.fullname == username][0]
            session['user_id'] = user.id
            g.user = user
            return render_template('index_logged.html')

        else:
            flash('not a valid username!, try again','warning')
    
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
        # else:
        #     flash("P  E  B  E  T  E")
    except Exception as err:
        print('ESTE ES EL ERROR REY E' +str(err))
    return render_template('register.html')




@app.route("/home",methods = ["GET","POST"])
def home():
    try:
        if 'user_id' in session:
            user = [x for x in userList if x.id == session['user_id']][0]
            g.user = user
            return render_template("index_logged.html")
        return render_template('index.html')
    except:
        if 'user_id' in session:
            user = [x for x in userList if x.id == session['user_id']][0]
            g.user = user
            return render_template("index_logged.html")
        return render_template('index.html')


@app.route('/admin')
def about():
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM residents")
    res = c.fetchall()
    print(res)

    return render_template("admin.html", todo = res)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
