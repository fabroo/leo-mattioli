import json
import os 
def buscarArchivo():
    
    comparador = False
    
    if os.path.exists('pass.txt'):
        pswFile = open('pass.txt','r+')
        pswRaw = pswFile.readlines()
        nombre = pswRaw[0][:-1] #sacar el \n
        password = pswRaw[1]
        
        
    return comparador,password,nombre
    
passExist,psw,name = buscarArchivo()
print(name)
print(psw)
# if name == "fabri":
#     print('pitoo')