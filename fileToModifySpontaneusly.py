import face_recognition
import os
import cv2
import pickle
import json
import numpy
import sqlite3
import shutil
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "testdb.db")
conn  = sqlite3.connect(db_path)
c = conn.cursor()
# dni = str(input('Tu DNI: '))
# name = str(input('Nuevo nombre: '))
# mail = str(input("Tu E-Mail: "))

c.execute(f'''SELECT dni FROM residents WHERE company = 'Mattioli Learning' ''')

    
#??????????
