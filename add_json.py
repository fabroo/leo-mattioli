import json


nameUser = str(input("enter name: "))
password = str(input("enter password: "))

jsonFile = open('random.json')

jsonParsed = json.load(jsonFile)

jsonParsed.append({'id' : nameUser})
jsonParsed.append({'pasw': password})

print(jsonParsed)
