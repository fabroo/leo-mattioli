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

text="Bruno Tievoli"

KNOWN_NAMES = f'{os.getcwd()}/fotos'
existe = False

target = (f"{KNOWN_NAMES}/{str(text)}")
print(target)



