import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np

import cell_splitter as cspl

#The get_number_guess essentially from  http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html
def get_number_guess(file_name):
    im = cv2.imread(file_name)
    roi = cv2.resize(im, (28, 28), interpolation=cv2.INTER_AREA)
    roi = cv2.dilate(roi, (3, 3))
    # Calculate the HOG features
    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))

    return nbr[0]

def list_of_scores(file_name_list):
       
    score_list = []
    for my_score in file_name_list:
        print(my_score)
        #my_score  = './img_files/table1_contours6.jpg'

        myCS = cspl.CellSplitter(my_score)
        myCS.draw_splitter()
        first_digit = get_number_guess('segment_1.jpg')
        second_digit = get_number_guess('segment_2.jpg')
        my_score = first_digit*10 + second_digit
        score_list.append(my_score) 

    return score_list

def print_score_table(list_out_of, list_scores):
    num_nums = len(list_out_of)
    
    for ind in range(num_nums):
        print(list_out_of[ind], " ", list_scores[ind])
    print(np.sum(list_out_of), " ", np.sum(list_scores))

if __name__ == "__main__":
    # Load the classifier
    clf = joblib.load("digits_cls.pkl")


    psble_score_number_file_id = [5, 8, 11, 14, 17]
    score_number_file_id = [6, 9, 12, 15, 18]

    file_header = './img_files/table1_contours'
    file_ending = '.jpg'

    possible_score_file_names = [file_header + str(s) + file_ending for s in psble_score_number_file_id]


    score_file_names = [file_header + str(s) + file_ending for s in score_number_file_id]


    list_possible = list_of_scores(possible_score_file_names)
    list_scores = list_of_scores(score_file_names)
    
    print_score_table(list_possible, list_scores)
    
    
