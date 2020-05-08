import pickle
import face_recognition
import os
import shutil
import numpy as np
import time
import math

def checkeoa():
    KNOWN_FACES_DIR = './fotos/'
    DESIGNATED_NAME  = 'juan_amigo_fabro'

    kf = open('./pickle/known_faces','rb')
    kn = open('./pickle/known_names','rb')
    known_faces = pickle.load(kf)
    known_names = pickle.load(kn)
    kf.close()

    kn.close()

    print(known_names)

