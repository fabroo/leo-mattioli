import sqlite3
from sqlite3 import Error

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "testdb.db")
MINLENGTH = 6
MAX_FAILURES = 5 #intuitivo.

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT * FROM residents")
res = c.fetchall()

def createTemporaryFile(name,password):
    temporaryFile= open("pass.txt","w+")
    temporaryFile.write(name+'\n'+password)
    temporaryFile.close()

while True:
    fallos = 0
    while fallos < MAX_FAILURES:

        contra = int(input("passw: "))
        # name = str(input("name: ")) #cara
        pasar = False

        if len(str(contra)) >= MINLENGTH:
            try:
                c.execute("SELECT name FROM residents WHERE id={}".format(contra))
                res = c.fetchone()
                print('Bienvenido, ' + res[0])
                fallos = 0
                createTemporaryFile(res[0], str(contra))
            except:
                print('arafue')
                fallos +=1
                contra = None  
                name = None
                pasar = False 
        else:
            print("no puede pasar") 
            fallos +=1
        contra = None  
        name = None
        pasar = False 

    else:
        print('pip pip, sos gay')
        #insert codigo de mandar alerta el porterowo
        fallos = 0 

