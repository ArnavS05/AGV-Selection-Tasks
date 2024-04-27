import numpy as np
import pickle
from getImageFeatures import get_image_features


def get_similarity(h1, h2, algo):
    if algo == 'cosine':
        len_h1 = np.linalg.norm(h1)
        len_h2 = np.linalg.norm(h2)
        dot = np.dot(h1, h2)
        cosine = dot/(len_h1*len_h2)    # cosine of angle between h1 and h2
        similarity_score = cosine*100     # To get as a percentage

    elif algo == 'euclidean':
        # Finds the distance between h1 and h2 relatice to the maximum possible distance between h1 and h2
        dist = np.linalg.norm(h1-h2)
        max_dist = np.linalg.norm(h1) + np.linalg.norm(h2)
        similarity_score = (1 - (dist/max_dist))*100     # To get as a percentage

    elif algo == 'iou':
        # Calculates intersection over union
        intersection = np.minimum(h1, h2).sum()     # Sum of element wise minimum numbers
        union = np.maximum(h1, h2).sum()      # Sum of element wise maximum numbers
        iou = intersection/union
        similarity_score = iou*100     # To get as a percentage
        
    return similarity_score


def get_similar_image(image_name, image_names_set, method):
    wordMap = pickle.load(open('.../DATA/%s_%s.pkl' % (image_name[:-4], method), 'rb'))
    h = get_image_features(wordMap, 50)
    
    max_score = 0          # To store the maximum similarity score
    most_similar_image=''       # To store the most similar image's name
    
    for img in image_names_set:    
        wordMap2 = pickle.load(open('.../DATA/%s_%s.pkl' % (img[:-4], method), 'rb'))
        h2 = get_image_features(wordMap2, 50)

        # Experimented with the code several times to come up with the following formula.
        similarity_score = min(0.873*get_similarity(h, h2, 'cosine'), 0.983*get_similarity(h, h2, 'euclidean'), 1.278*get_similarity(h, h2, 'iou'))
        
        if similarity_score>max_score:
            max_score = similarity_score
            most_similar_image = img

    return most_similar_image, max_score



if __name__ == "__main__":
    import cv2 as cv
    import random
    
    traintest = pickle.load(open('.../DATA/traintest.pkl', 'rb'))
    image_name = random.choice(traintest['test_imagenames'])
    image_names_set = set([random.choice(traintest['train_imagenames']) for i in range(300)])
    
    similar_image, score = get_similar_image(image_name, image_names_set, 'Harris')   # Can change method here
    
    print("Test Image:", image_name)
    print("Most Similar Image found:", similar_image)
    print("Similarity score: ", score, "%", sep = '')

    
    image = cv.imread('.../DATA/%s' % (image_name,))
    cv.imshow('Test Image', image)
    
    image2 = cv.imread('.../DATA/%s' % (similar_image,))
    cv.imshow('Most Similar Image', image2)
