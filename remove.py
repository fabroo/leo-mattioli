import pickle
import face_recognition
import os
import shutil
import numpy as np
import time
import math

def borrar(DESIGNATED_NAME):
    start = time.time()
    KNOWN_FACES_DIR = './fotos/'
    

    kf = open('./pickle/known_faces','rb')
    kn = open('./pickle/known_names','rb')
    known_faces = pickle.load(kf)
    known_names = pickle.load(kn)
    kf.close()
    kn.close()

    for i in os.listdir(KNOWN_FACES_DIR):
        if i == DESIGNATED_NAME:
            shutil.rmtree(f'{KNOWN_FACES_DIR}/{i}', ignore_errors=True)

    for i in range(len(known_names)- 1, -1, -1):
            if known_names[i] == DESIGNATED_NAME:
                del known_names[i]
                known_faces.pop(i)

    f = open('./pickle/known_faces','wb')
    n = open('./pickle/known_names','wb')
    newFaces = pickle.dump(known_faces,f, pickle.HIGHEST_PROTOCOL)
    newNames = pickle.dump(known_names,n, pickle.HIGHEST_PROTOCOL)
    f.close()    
    n.close()

    end = time.time()

    print('Tardó: ' + str(end-start)+ ' segundos. Listo para usar!')

