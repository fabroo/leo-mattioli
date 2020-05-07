import json

database = "random.json"
data = json.loads(open(database).read())

#print(data[0]["id"])
MINLENGTH = 6

def createTemporaryFile(name,password):
    temporaryFile= open("pass.txt","w+")
    temporaryFile.write(name+'\n'+password)
    temporaryFile.close()



contra = str(input("passw: "))
name = str(input("name: ")) #cara
pasar = False

if len(contra) == MINLENGTH:
    for dict in data:
        if dict['pasw'] == contra and dict['id'] == name:
            pasar = True
    if pasar:
        createTemporaryFile(name, contra)
        print("puede pasar")
            
    else:
        print("no puede pasar")
else:
    print("no puede pasar")        
contra = None  
name = None
pasar = False 

