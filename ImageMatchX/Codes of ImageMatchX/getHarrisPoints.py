import numpy as np
import cv2 as cv
from scipy import ndimage
from utils import imfilter


def get_harris_points(I, alpha, k):

    if len(I.shape) == 3 and I.shape[2] == 3:
        I = cv.cvtColor(I, cv.COLOR_RGB2GRAY)
    if I.max() > 1.0:
        I = I / 255.0

    # -----fill in your implementation here --------

    # To convolve through the image to detect variation in intensity along x axis.
    Ix = imfilter(I, np.array([[-1, 0, 1]]))
    # To convolve through the image to detect variation in intensity along y axis.
    Iy = imfilter(I, np.array([[-1], [0], [1]]))

    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy

    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

    Sxx = ndimage.convolve(Ixx, kernel)
    Syy = ndimage.convolve(Iyy, kernel)
    Sxy = ndimage.convolve(Ixy, kernel)

    det = Sxx * Syy - Sxy * Sxy
    trace = Sxx + Syy
    R = det - k * (trace ** 2)


    # Getting alpha number of points with maximum R
    flattened_indices = np.argsort(R, axis=None)[::-1]
    indices = np.unravel_index(flattened_indices, R.shape)
    indices = tuple(np.array(indices)[:, :alpha])
    points = []
    for i in range(len(indices[0])):
        points.append([indices[0][i], indices[1][i]])

    points = np.array(points)
    # ----------------------------------------------
    
    return points




if __name__=="__main__":
    image = cv.imread(".../DATA/airport/sun_afbxsdfksjhcunpb.jpg")
    image2 = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    corners = get_harris_points(image2, 1000, 0.06)
    for i in corners:
        image[i[0]][i[1]]=[0, 0, 255]
    cv.imshow('img', image)
