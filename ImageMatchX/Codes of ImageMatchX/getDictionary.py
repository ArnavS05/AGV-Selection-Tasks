import numpy as np
import cv2 as cv
from createFilterBank import create_filterbank
from extractFilterResponses import extract_filter_responses
from getRandomPoints import get_random_points
from getHarrisPoints import get_harris_points
from sklearn.cluster import KMeans


def get_dictionary(imgPaths, alpha, K, method):

    filterBank = create_filterbank()

    pixelResponses = np.zeros((alpha * len(imgPaths), 3 * len(filterBank)))
    # i.e., pixelResponses will store filter values of 3*20 filters for
    # alpha number of corners for all the images.
    # Those 3*20 values will form a visual word.

    for i, path in enumerate(imgPaths):
        print('-- processing %d/%d' % (i, len(imgPaths)))
        image = cv.imread('.../DATA/%s' % path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)    # convert the image from bgr to rgb, OpenCV use BGR by default
        
        # -----fill in your implementation here --------
        filterResponses = extract_filter_responses(image, filterBank)
        
        if method == 'Random':
            points = get_random_points(image, alpha)
        elif method == 'Harris':
            points = get_harris_points(image, alpha, 0.06)

        for j, point in enumerate(points):
            x, y = point
            pixelResponses[i * alpha + j] = filterResponses[x, y].flatten()
            
        # ----------------------------------------------

    dictionary = KMeans(n_clusters=K, random_state=0).fit(pixelResponses).cluster_centers_
    return dictionary
