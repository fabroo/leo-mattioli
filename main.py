#Import .py files
import predictV2
import inputId
import addExtraPics
import trainPeroBien
import trainPorSiAlgoAndaMal
import check
import check_2
import remove
import newUser
#Imports
import time
import os
import sys

def todo(argument):
    switcher = {
        'check': vibeCheck,
        'train': train,
        'train_bad': help_train,
        'remove': remove,
        'quit': salir,
        'newID': newID,
        'predecir': predecir,
        'addPics': addPics,
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "No hay tal funcion")
    # Execute the function
    func()

def predecir():

    predecir = True
    if predecir == True:
        nombre = str(input('nombre: '))
        contra = int(input('contra: '))
        inputId.inputear(contra, nombre)
    predecir = False
    if os.path.exists('pass.txt'):
        b,a,pito = predictV2.buscarArchivo()
        predictV2.predecir(pito)
        predecir = True

def vibeCheck():
    check.checkeo()


def train():
    trainPeroBien.trainearBien()

def help_train():
     trainPorSiAlgoAndaMal.trainOld()

def remove():
    theInput = input("Nombre de carpeta a borrar: ")
    remove.borrar(theInput)

def addPics():
    theInput = input("Nombre de carpeta a agregar fotos: ")
    addExtraPics.nuevasFotos(theInput)

def newID():
    dni = str(input('Tu DNI: '))
    name = str(input('Nuevo nombre: '))
    mail = str(input("Tu E-Mail: "))
    companyId = str(input("Compañia: "))
    newUser.agregarUsuario(dni, name, mail, companyId)

def salir():
    print('Saludos Binarios!')
    time.sleep(1)
    sys.exit(0)

while True:
    todo((input('que funcion desea correr??: ')))
   