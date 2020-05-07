import pickle
import os
import cv2
import face_recognition
import shutil
import numpy as np 
import time


KNOWN_FACES_DIR = './fotos/'
start =time.time()

kf = open('./pickle/known_faces','rb')
kn = open('./pickle/known_names','rb')
known_faces = pickle.load(kf)
known_names = pickle.load(kn)
kf.close()
kn.close()
new_faces_array = []
new_names_array = []
NEW_FACES= './new_faces/'

for i in range(len(known_names)):
    known_names[i].rstrip('\r\n')
#@FABRIZIO ESTO HACE QUE SE BORREN LOS \R PORQUE NO SE NOS OCURRIO BORRARLOS MANUALMENTE PORQUE SOMOS RE IMBECILESS UWUWUWUWUWUWUWUWUWUWUWUWU
for name in os.listdir(NEW_FACES):
    print('Cargando fotos de ' + name)
    for filename in os.listdir(f'{NEW_FACES}/{name}'):
         # Load an image
        image = face_recognition.load_image_file(f'{NEW_FACES}/{name}/{filename}')
        try:
            encoding = face_recognition.face_encodings(image)[0]

        except:
            print("peto: "+str(filename))
            dir_error = './error/'
            if not os.path.exists(f'{dir_error}/{name}'):
                os.makedirs(f'{dir_error}/{name}')

            shutil.move(f'{NEW_FACES}/{name}/{filename}',f'{dir_error}/{name}/{filename}')
            
        new_faces_array.append(encoding)
        new_names_array.append(name)
    dir_done = './fotos/'
    shutil.move(f'{NEW_FACES}/{name}',f'{dir_done}/{name}')



arrayPrevio_names = np.array(known_names)
arrayPrevio_faces = np.array(known_faces)

arrayNuevo_faces = np.array(new_faces_array)
arrayNuevo_names = np.array(new_names_array)


# ['mis datos' + 'datos de tievo mom' + 'datos de brenda mom' + ]
try:
    total_faces = list(np.concatenate((arrayPrevio_faces, arrayNuevo_faces)))
    total_names = list(np.concatenate((arrayPrevio_names, arrayNuevo_names)))
    print('Cargando fotos nuevas!')

    f = open('./pickle/known_faces','wb')
    g = open('./pickle/known_names','wb')


    serialized = pickle.dump(total_faces,f, pickle.HIGHEST_PROTOCOL)
    serialized = pickle.dump(total_names,g, pickle.HIGHEST_PROTOCOL)
    f.close()
    g.close()
except:
    print('NO HAY NUEVAS FOTOS QUE CARGAR OWO')
print(total_names)
end = time.time()

print('en: '+str(end-start)+' segundos')

#posible fix: el array_names se completa plenamente en base al .json, y no en base a las carpetas.