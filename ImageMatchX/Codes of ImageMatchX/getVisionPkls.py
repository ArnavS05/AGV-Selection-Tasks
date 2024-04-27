import numpy as np
import pickle
from createFilterBank import create_filterbank
from getImageFeatures import get_image_features

def createVision(train_imagenames, train_labels, filterBank, method):
    if method == 'Harris':
        VisualWordDict = pickle.load(open('.../DATA/dictionaryHarris.pkl', 'rb'))
    elif method == 'Random':
        VisualWordDict = pickle.load(open('.../DATA/dictionaryRandom.pkl', 'rb'))
        
    VisionDict = {'dictionary': VisualWordDict, 'filterBank': filterBank, 'trainFeatures': np.zeros((len(train_labels), 50), dtype=np.int32), 'trainLabels': train_labels}
    # K = 50 for my dictionary

    for i, path in enumerate(train_imagenames):
        print('-- processing %d/%d' % (i+1, len(train_imagenames)))
        wordMap = pickle.load(open('.../DATA/%s_%s.pkl' % (path[:-4], method), 'rb'))
        VisionDict['trainFeatures'][i] = get_image_features(wordMap, 50)


    return VisionDict






if __name__ == "__main__":
    filterBank = create_filterbank()
    meta = pickle.load(open('.../DATA/traintest.pkl', 'rb'))
    train_imagenames = meta['train_imagenames']
    train_labels = meta['train_labels']
    
    HarrisDict = createVision(train_imagenames, train_labels, filterBank, 'Harris')
    pickle.dump(HarrisDict, open('.../DATA/visionHarris.pkl', 'wb'))
    
    RandomDict = createVision(train_imagenames, train_labels, filterBank, 'Random')
    pickle.dump(RandomDict, open('.../DATA/visionRandom.pkl', 'wb'))
