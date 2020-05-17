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

BASE_DIR = os.getcwd()
db_path = os.path.join(BASE_DIR, "testdb.db")

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute(f"SELECT * FROM residents WHERE dni = 45583265")
res = c.fetchone()

print(res[1])



