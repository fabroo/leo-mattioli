import pickle

kn = open('./pickle/known_names','rb')
known_names = pickle.load(kn)
for i in range(len(known_names)):
    known_names[i].rstrip('\r\n')

serialized = pickle.dump(known_names,kn, protocol=0)
kn.close()

