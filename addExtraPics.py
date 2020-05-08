import pickle
import face_recognition
import os
import shutil
import numpy as np
import time
import math

KNOWN_FACES_DIR = './fotos/'
DESIGNATED_NAME  = 'tievo_mom' #aca hacemos que importe loss datos en la webapp!!!

kf = open('./pickle/known_faces','rb')
kn = open('./pickle/known_names','rb')
known_faces = pickle.load(kf)
known_names = pickle.load(kn)
new_array = []
kf.close()
kn.close()

start = time.time()
indiv_names = np.unique(known_names)

NEW_FACES= './new_faces/'


for name in os.listdir(NEW_FACES):
    print('Cargando fotos de ' + name)
    for filename in os.listdir(f'{NEW_FACES}/{name}'):
        image = face_recognition.load_image_file(f'{NEW_FACES}/{name}/{filename}')
        try:
            encoding = face_recognition.face_encodings(image)[0]
            shutil.move(f'{NEW_FACES}/{name}/{filename}',f'{KNOWN_FACES_DIR}/{name}')
        except:
            print("peto: "+str(filename))

        new_array.append(encoding)

    pingo = False
    numPics = 0
    numAppear = 0
    for i in range(len(known_names)):
        if known_names[i] == DESIGNATED_NAME:
            numPics += 1
            if not pingo:
                numAppear = i
                pingo = True

    elNumero = numAppear + numPics
    for i in range(len(new_array)):
        y = i + elNumero
        known_faces.insert(y, new_array[i])
        known_names.insert(y, DESIGNATED_NAME)
    
    f = open('./pickle/known_faces','wb')
    n = open('./pickle/known_names','wb')
    newFaces = pickle.dump(known_faces,f, pickle.HIGHEST_PROTOCOL)
    newNames = pickle.dump(known_names,n, pickle.HIGHEST_PROTOCOL)
    f.close()
    n.close()

end = time.time()
print('tardo ' + str(math.ceil(start - end)) + ' segundos (aprox uwu) en procesar.')
    #for i in range(len(known_names)):
        #if known_names[i] =designated name
            #known_names.remove[i]
            #known_faces.remove[i]
            


