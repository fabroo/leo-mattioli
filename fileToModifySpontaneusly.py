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

dni = 45583265
comm = sqlite3.connect
KNOWN_FACES = './fotos'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "testdb.db")
conn  = sqlite3.connect(db_path)
c = conn.cursor()

c.execute(f''' SELECT createdAccount FROM residents WHERE dni = {dni}; ''')
accCreated = c.fetchone()

print(accCreated)

