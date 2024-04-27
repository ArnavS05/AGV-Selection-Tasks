import numpy as np


def get_image_features(wordMap, dictionarySize):

    # -----fill in your implementation here --------

    h = np.zeros((dictionarySize,), dtype = np.int32)
    # In h, ith index stores the frequency of ith word of dictionary in wordMap
    for i in wordMap.flatten():
        h[i]+=1

    # ----------------------------------------------
    
    return h



if __name__ == '__main__':
    import pickle
    import matplotlib.pyplot as plt
    wordMap = pickle.load(open('.../DATA/rainforest/sun_aaispeummyknccnf_Random.pkl', 'rb'))
    h = get_image_features(wordMap, 50)

    # Plotting the histogram using matplotlib
    plt.bar(list(range(50)), h, width=0.9)
    plt.xlabel("Visual Word Index")
    plt.ylabel("Frequency")
    plt.title("Bag of visual words histogram")
    plt.show()
