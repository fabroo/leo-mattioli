import face_recognition
import os
import cv2
import pickle
import json
import time
#proba con el dump y el load
jsonFile = open('sth.json')

jsonParsed = json.load(jsonFile)

KNOWN_FACES_DIR = './fotos/'
#UNKNOWN_FACES_DIR = 'frecon/unknown/'
TOLERANCE = 0.4
FRAME_THICKNESS = 3
SUCCESS_NEEDED = 5
FONT_THICKNESS = 2
SELECTED_FRAMES = 10  #n of pictures taken 
MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model

video = cv2.VideoCapture(0) #CAMBIAR SEGUN LA PC QUE SEA, BRENDA Y TIEVO USAN 0, FABRO USA 2

kf = open('./pickle/known_faces','rb')
kn = open('./pickle/known_names','rb')
known_faces = pickle.load(kf)
known_names = pickle.load(kn)
kf.close()
kn.close()


# Returns (R, G, B) from name
def name_to_color(name):
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

def buscarArchivo():
    
    comparador = False
    password = ""
    nombre = ""

    if os.path.exists('pass.txt'):
        pswFile = open('pass.txt','r+')
        time.sleep(3)
        pswRaw = pswFile.readlines()
        
        try:
            nombre = pswRaw[0][:-1] #sacar el \n
            password = pswRaw[1]
            comparador = True
            pswFile.close()
            os.remove('pass.txt')
        except:
            
            nombre = pswRaw[0][:-1] #sacar el \n
            password = pswRaw[1]
            comparador = True
            pswFile.close()
            os.remove('pass.txt')

    return comparador,password,nombre

while True:    
    passExist = False

    while not passExist:
        passExist,psw,name = buscarArchivo()
    print('Loading known faces...')


    if passExist:
        success_count = 0
        for i in range(SELECTED_FRAMES):
            
            ret,image = video.read() 
            # image = cv2.resize(ima, (1280, 720) ) #cosas de tievo.
        
            locations = face_recognition.face_locations(image, model=MODEL)

            encodings = face_recognition.face_encodings(image, locations)
            print(f', found {len(encodings)} face(s)')

            for face_encoding, face_location in zip(encodings, locations):

                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

                match = None
                if True in results:  # If at least one is true, get a name of first of found labels
                    
                    match = known_names[results.index(True)]
                    print(f' - {match}')
                    if name == match:
                        success_count += 1
                    
                    # Each location contains positions in order: top, right, bottom, left
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    # Get color by name using our fancy function
                    color = name_to_color(match)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                    # Now we need smaller, filled grame below for a name
                    # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

                    # Wite a name
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

                if match == None:
                    match = 'unknown'
                    # Each location contains positions in order: top, right, bottom, left
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    # Get color by name using our fancy function
                    color = name_to_color(match)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                    # Now we need smaller, filled grame below for a name
                    # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

                    # Wite a name
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

            # Show image
            cv2.imshow("uwu",image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()
        if success_count >= SUCCESS_NEEDED:
            print('Se abrio la puerta mirey')
            
        else:
            print('no se abrio un pingo, mishey')

           
    