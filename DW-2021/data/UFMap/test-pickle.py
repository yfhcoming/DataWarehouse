import pickle

f = open('component_mapping.pickle','rb')
info = pickle.load(f)
print(info)
