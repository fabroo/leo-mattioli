import pickle
path = './pickle/known_names'
kn = open(path).read().replace('\r','\n')
dst = path + '.tmp'
open(dst,'w').write(kn)

known_names = pickle.load(open(dst,'rU'))
#for i in range(len(known_names)):
#    known_names[i].rstrip('\r\n')

serialized = pickle.dump(known_names,kn, protocol=0)
kn.close()

