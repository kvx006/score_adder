import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np

# Load the classifier
clf = joblib.load("digits_cls.pkl")

im = cv2.imread("segment_2.jpg")

#im2 = cv2.imread("img_files/table1_contours6.jpg")


roi = cv2.resize(im, (28, 28), interpolation=cv2.INTER_AREA)
roi = cv2.dilate(roi, (3, 3))
# Calculate the HOG features
roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
nbr = clf.predict(np.array([roi_hog_fd], 'float64'))

print("nbr is", nbr[0])
cv2.imwrite("guess.jpg", im)
#cv2.waitKey()
