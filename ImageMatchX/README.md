The folder 'Codes of ImageMatchX' has all the given python files in which I have added my implementation. Apart from that, it also has a few more python files which were required for the completion of the task, as mentioned in the task description.

The folder 'DATA' has the following things generated using my code (according to instructions in the task description):
1. The visual words dictionary for both, Random and Harris points.
2. All the Class folders (airport, desert, etc.) have word-maps of each image, stored as 2 pkl files (one made using Harris dictionary, and the other made using Random points dictionary). (I haven't uploaded these here.)
3. visionHarris.pkl and visionRandom.pkl as asked in the task description.

The data we were provided included traintest.pkl and 8 folders (of different classes) namely airport, campus, bedroom, auditorium, desert, landscape, rainforest, football_stadium. Each folder had about 300 images. (I haven't uploaded those 8 folders.)

To see the working of the code, you need to run getSimilarImage.py.
For that, you will also have to download getImageFeatures.py and all the class folders (so that the word-maps can be accessed). Also, the Data paths should be changed in getSimilarImage.py and getImageFeatures.py according to the path were the DATA folder has been downloaded.
