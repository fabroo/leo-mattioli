import pickle
import os
import cv2
import face_recognition
import shutil
import numpy as np 
import time



start =time.time()

kf = open('./pickle/known_faces','rb')
kn = open('./pickle/known_names','rb')
known_faces = pickle.load(kf)
known_names = pickle.load(kn)
kf.close()
kn.close()
new_faces_array = []
new_faces_names = []
NEW_FACES= './new_faces/'
for name in os.listdir(NEW_FACES):

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
        new_faces_names.append(name)
    dir_done = './fotos/'
    shutil.move(f'{NEW_FACES}/{name}',f'{dir_done}/{name}')

arrayPrevio = np.array(known_names)
arrayNuevo = np.array(new_faces_names)
total_names = list(np.concatenate((arrayPrevio, arrayNuevo)))

arrayPrevio_faces = np.array(known_faces)
arrayNuevo_faces = np.array(new_faces_array)

total_faces = list(np.concatenate((arrayPrevio_faces, arrayNuevo_faces)))


f = open('./pickle/known_faces','wb')
g = open('./pickle/known_names','wb')


serialized = pickle.dump(total_faces,f, protocol=0)
serialized = pickle.dump(total_names,g, protocol=0)
f.close()
g.close()

end = time.time()

#print(total_names)
print('en: '+str(end-start)+' segundos')