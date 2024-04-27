import multiprocessing
import pickle
import math
import cv2 as cv
from createFilterBank import create_filterbank
from getVisualWords import get_visual_words

'''
The given code wasn't working fine. I made the following two alterations to make it work:
1. Defined worker_to_visual_words() outside the definition of batch_to_visual_words().
2. Added 'flush=True' in the print statement so that the print statements are executed in realtime.
'''

def worker_to_visual_words(wind, all_imagenames, num_cores, dictionary, filterBank, point_method):
    for j in range(math.ceil(len(all_imagenames) / num_cores)):
        img_ind = j * num_cores + wind
        if img_ind < len(all_imagenames):
            img_name = all_imagenames[img_ind]
            print('converting %d-th image %s to visual words' % (img_ind, img_name), flush=True)
            image = cv.imread('.../DATA/%s' % img_name)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # convert the image from bgr to rgb
            wordMap = get_visual_words(image, dictionary, filterBank)
            pickle.dump(wordMap, open('.../DATA/%s_%s.pkl' % (img_name[:-4], point_method), 'wb'))


def batch_to_visual_words(num_cores, point_method):

    print('using %d threads for getting visual words' % num_cores)

    meta = pickle.load(open('.../DATA/traintest.pkl', 'rb'))
    all_imagenames = meta['all_imagenames']

    dictionary = pickle.load(open('.../DATA/dictionary%s.pkl' % point_method, 'rb'))

    filterBank = create_filterbank()

    

    workers = []
    for i in range(num_cores):
        workers.append(multiprocessing.Process(target=worker_to_visual_words, args=(i, all_imagenames, num_cores, dictionary, filterBank, point_method)))
    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

    print('batch to visual words done!')


if __name__ == "__main__":
    batch_to_visual_words(num_cores=4, point_method='Harris')
    batch_to_visual_words(num_cores=4, point_method='Random')

