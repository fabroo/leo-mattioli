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

while True:
    decision = str(input("Quiere predecir? (Y/N/quit): "))
    if decision.lower()== 'y':
        predecir = True
        if predecir == True:
            inputId.inputear()
        predecir = False
        if os.path.exists('pass.txt'):
            b,a,pito = predictV2.buscarArchivo()
            predictV2.predecir(pito)
            predecir = True
    elif decision.lower() == 'n':
        fileToRun = str(input("Que archivo quiere correr?: "))
        # switch_dem(fileToRun)
        if fileToRun == 'check':
            check.checkeo()
        elif fileToRun == 'trainNew':
            trainPeroBien.trainearBien()
        elif fileToRun == 'trainOld':
            trainPorSiAlgoAndaMal.trainOld()
        elif fileToRun == 'remove':
            theInput = input("Nombre de carpeta a borrar: ")
            remove.borrar(theInput)
        elif fileToRun == 'addPics':
            theInput = input("Nombre de carpeta a agregar fotos: ")
            addExtraPics.nuevasFotos(theInput)
        elif fileToRun == 'newId':
            newUser.agregarUsuario()
        print('Altoke rey, termina10')
    elif decision.lower() == 'quit':
        print('Saludos Binarios!')
        time.sleep(1)
        sys.exit(0)
        


    
    