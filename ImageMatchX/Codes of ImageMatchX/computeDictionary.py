import pickle
from getDictionary import get_dictionary


meta = pickle.load(open('/DATA/traintest.pkl', 'rb'))
train_imagenames = meta['train_imagenames']

# -----fill in your implementation here --------
HarrisDict = get_dictionary(train_imagenames, 1000, 50, 'Harris')
pickle.dump(HarrisDict, open('.../DATA/dictionaryHarris.pkl', 'wb'))

RandomDict = get_dictionary(train_imagenames, 1000, 50, 'Random')
pickle.dump(RandomDict, open('.../DATA/dictionaryRandom.pkl', 'wb'))

# ----------------------------------------------



