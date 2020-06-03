import os

from flask import Flask, request, render_template, send_from_directory, flash, g, session, redirect, url_for
from flask_socketio import SocketIO

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
socketio = SocketIO(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)
KNOWN_NAMES = f'{os.getcwd()}/fotos'



class User:
    def __init__(self, id, fullName, contra, mail, role, company):
        self.id = id
        self.fullname = fullName
        self.contra = contra
        self.mail = mail
        self.role = role
        self.company = company

comm = sqlite3.connect
BASE_DIR = os.getcwd()
db_path = os.path.join(BASE_DIR, "testdb.db")
conn  = sqlite3.connect(db_path)
c = conn.cursor()

c.execute(f'''SELECT * FROM residents''')
pakesepa = c.fetchall()
userList = []
for el in pakesepa:
    userList.append(User(id=str(el[0]),fullName = str(el[1]),contra=str(el[2]),mail=str(el[3]),role=str(el[7]), company = str(el[4])))

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
        if request.method == 'POST':
            texto = request.form['nombre']

            
            existe = False

            target = os.path.join(APP_ROOT, 'images\\' + str(texto)+'')
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
                    render_template("error.html", message="Files uploaded are not supported...")
                destination = "/".join([target, filename])
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                upload.save(destination)

            if os.path.exists(f'{KNOWN_NAMES}/{texto}'):
                existe = True
            
            try:
                if existe:
                    print('Ya existe un directorio con tu nombre, agregando nuevas fotos...')
                    addExtraPics.nuevasFotos(texto) #usa el autocomplete, y esta funcion toma name como argumento
                    flash('Ya se ejecutó y todo salio bien segui viviendo')
                else:
                    print('Nuevo directorio, entrenando reconocimiento facial...')
                    trainPeroBien.trainearBien()#creo que era??
                    flash('Ya se ejecutó y todo salio bien segui viviendo')
            except:
                flash('Amigo se cayo todo sorry cambia de empresa..')
    return render_template("upload.html")
    
    

@app.route('/close_sess', methods=['GET', 'POST'])
def closeSess():
    session.pop('user_id', None)
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje  = "Ingrese contraseña"
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
            mensaje = 'Usuario o Contraseña incorrectos!, try again'
    
    return render_template('login.html', mensaje = mensaje)

@app.route("/register",methods = ["GET","POST"])
def register():
 

    try:
        targetReg = (f'{APP_ROOT}\\static\\assets\\pfp')
        print(targetReg)
        idCompany = request.form.get('companyid',False)
        dni = request.form.get('dni',False)
        email = request.form.get('mail',False)
        fullname = request.form.get('fullname',False)
        pfpPath = f'static/assets/pfp/{dni}.jpg'
        pfp = request.files.get('file')
        filename = pfp.filename
        print(filename)
        filenameNew = f'{dni}.jpg'
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg"):
            print("File supported moving on...")
        else:
            render_template("error.html", message="Files uploaded are not supported...")
        destination = "/".join([targetReg, filenameNew])
        if newUser.agregarUsuario(dni, fullname, email, idCompany,pfpPath):
            flash("Cuenta creada con exito. Inicia Sesion arriba a la derecha. Bienvenido!")
        pfp.save(destination)
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

@app.route("/home_log",methods = ["GET","POST"])
def home_log():
    if not g.user:
        return render_template('login.html')
    else:
        KNOWN_NAMES = f'{os.getcwd()}/fotos/'
        pics = 'No'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"SELECT * FROM residents WHERE dni = {g.user.id}")
        res = c.fetchone()
        c.execute(f"SELECT * FROM residents WHERE companyid = '{g.user.company}' AND createdAccount = 0")
        unregistered = c.fetchall()
        
        if os.path.exists(f'{KNOWN_NAMES}/{res[1]}'):                
            pics = 'Si'
        if request.method == "POST":
            newDni = request.form.get('newdni', False)
            c.execute(f'''INSERT INTO residents VALUES({int(newDni)},NULL,NULL,NULL,"{g.user.company}",0,NULL,'Miembro')''')
            conn.commit()

        return render_template('profile_home.html', info = res, picsvar = pics, unreg = len(unregistered))

@app.route('/admin', methods=["GET","POST"])
def admin():

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM residents WHERE companyid = '{g.user.company}' AND createdAccount = 0")
    unregistereda = c.fetchall()
    c.execute(f"SELECT * FROM residents WHERE companyid = '{g.user.company}' AND createdAccount = 1")
    res = c.fetchall()
    c.execute(f"SELECT * FROM residents WHERE dni = {g.user.id}")
    resAgain = c.fetchone()
    if os.path.exists(f'{KNOWN_NAMES}/{resAgain[1]}'):
        pics = 'Si'

    if not g.user:
        return render_template('login.html')
    elif g.user.role == "Administrador":
        for el in unregistereda:
            elem = str(el[0])
            if request.form.get(elem):
                c.execute(f"DELETE FROM residents WHERE dni = {int(elem)}")
                conn.commit()
                c.execute(f"SELECT * FROM residents WHERE companyid = '{g.user.company}' AND createdAccount = 0")
                unregistereda = c.fetchall()

        return render_template("admin.html", todo = res, info = resAgain, nada = unregistereda)
    else:
        return render_template('profile_home.html', info = resAgain, picsvar = pics, noCapo = "a")
@app.route('/horarios')
def horario():

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM residents WHERE companyid = '{g.user.company}'")
    res = c.fetchall()

    info = [(45500288, 'Fabrizio Corzini', 1234567, 'fcorzini@gmail.com', '1a2b3c', 1, 'static/assets/pfp/45500288.jpg', 'Miembro'), (45013685, 'Brenda Fleischer', 3406748, 'flebrenda@gmail.com', '1a2b3c', 1, 'static/assets/pfp/45013685.jpg', 'Administrador'), (45583265, 'Bruno Tievoli', 737026, 'tievolib@gmail.com', '1a2b3c', 1, 'static/assets/pfp/45583265.jpg', 'Administrador')] 

    if not g.user:
        return render_template('login.html')
    elif g.user.role == "Administrador":        
        return render_template("horarios.html", todo = info)
    else:
        return render_template('profile_home.html', info = res )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    
