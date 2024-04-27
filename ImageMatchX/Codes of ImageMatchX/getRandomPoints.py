import numpy as np


def get_random_points(I, alpha):

    # -----fill in your implementation here --------
    l, b = I.shape[0], I.shape[1]
    points = []
    for i in range(alpha):   # To get alpha random points
        points.append([int(np.random.rand()*(l-1)), int(np.random.rand()*(b-1))])   #The random points should be integer and should lie inside the image

    points = np.array(points)

    # ----------------------------------------------

    return points






if __name__=="__main__":
    import cv2 as cv
    image = cv.imread(".../DATA/airport/sun_afbxsdfksjhcunpb.jpg")
    points = get_random_points(image, 1000)
    for i in points:
        image[i[0]][i[1]]=[0, 0, 255]
    cv.imshow('img', image)
