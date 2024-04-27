import numpy as np
from scipy.spatial.distance import cdist
from extractFilterResponses import extract_filter_responses


def get_visual_words(I, dictionary, filterBank):

    # -----fill in your implementation here --------
    
    # Let wordMap have the index of the word in the dictionary for all pixels
    wordMap = np.zeros((I.shape[0], I.shape[1]), dtype=np.int32)   #Since indices are of integer datatype
    filterResponses = extract_filter_responses(I, filterBank)
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            dist = cdist(np.reshape(filterResponses[i, j].flatten(), (1,-1)), dictionary, 'cosine')
            # Using cosine distance as it shows extent of similarity
            # and similarity is what matters here.

            # dist is a 1x(no. of words in dictionary) array.
            wordMap[i, j] = np.argmin(dist[0])    # To get the index of the word in dictionary to which ijth pixel is closest to

    # ----------------------------------------------

    return wordMap





if __name__ == "__main__":
    from createFilterBank import create_filterbank
    import pickle
    import cv2 as cv
    point_method = 'Harris'    # You can change the method here
    dictionary = pickle.load(open('.../DATA/dictionary%s.pkl' % point_method, 'rb'))
    filterBank = create_filterbank()
    image = cv.imread('.../DATA/auditorium/sun_aaslkqqibkansrbd.jpg')
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)     # convert the image from bgr to rgb
    wordMap = get_visual_words(image, dictionary, filterBank)
    print(wordMap)
