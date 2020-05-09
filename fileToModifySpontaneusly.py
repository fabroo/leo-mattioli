import face_recognition
import os
import cv2
import pickle
import json
import numpy
import sqlite3
import shutil
import time
import smtplib
from email.mime.text import MIMEText

class User:
    def __init__(self, id, fullName, contra, mail):
        self.id = id
        self.fullname = fullName
        self.contra = contra
        self.mail = mail

# users = []
# users.append(User(id=1, username='Anthony', password='password'))
# users.append(User(id=2, username='Becca', password='secret'))
# users.append(User(id=3, username='Carlos', password='somethingsimple'))


comm = sqlite3.connect
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "testdb.db")
conn  = sqlite3.connect(db_path)
c = conn.cursor()

c.execute(f'''SELECT * FROM residents''')
pakesepa = c.fetchall()
userList = []
for el in pakesepa:
    userList.append(User(id=str(el[0]),fullName = str(el[1]),contra=str(el[2]),mail=str(el[3])))



