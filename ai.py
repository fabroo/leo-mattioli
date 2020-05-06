import face_recognition
import os
import cv2
import pickle

KNOWN_FACES_DIR = './fotos/'
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):

    # Next we load every file of faces of known person
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
       
        # Load an image
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

        # Get 128-dimension face encoding
        # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        try:
            encoding = face_recognition.face_encodings(image)[0]

        except:
            print("peto: "+str(filename))
            os.remove(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        # Append encodings and name
        known_faces.append(encoding)
        known_names.append(name)
print(known_faces)
print(known_names)

f = open('./pickle/known_faces','wb')
g = open('./pickle/known_names','wb')


serialized = pickle.dump(known_faces,f, protocol=0)
serialized = pickle.dump(known_names,g, protocol=0)
f.close()
g.close()
print('listo')