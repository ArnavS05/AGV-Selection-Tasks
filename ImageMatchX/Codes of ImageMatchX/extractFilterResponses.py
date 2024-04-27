import cv2 as cv
import numpy as np
from utils import *

def extract_filter_responses(I, filterBank):

    I = I.astype(np.float64)
    if len(I.shape) == 2:   #To convert BW images to RGB
        I = np.tile(I, (3, 1, 1))

    # -----fill in your implementation here --------

    filterResponses = np.zeros((I.shape[0], I.shape[1], 3, len(filterBank)))
    for i in range(len(filterBank)):
        filterResponses[:, :, 0, i] = imfilter(I[:,:,0], filterBank[i])  # For R channel
        filterResponses[:, :, 1, i] = imfilter(I[:,:,1], filterBank[i])  # For G channel
        filterResponses[:, :, 2, i] = imfilter(I[:,:,2], filterBank[i])  # For B channel

    # ----------------------------------------------
    
    return filterResponses




if __name__=="__main__":
    from createFilterBank import create_filterbank
    filterBank = create_filterbank()
    image = cv.imread(".../DATA/desert/sun_afferxhafrjnpuri.jpg")
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # convert the image from bgr to rgb
    filterResponses = extract_filter_responses(image, filterBank)
    show = rgb2lab(filterResponses[:,:,:,10])   #Change the number to see different filter respones
    cv.imshow('img', show)
