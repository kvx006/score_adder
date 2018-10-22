import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import ndimage


''' Split the cell image of table by finding the minimum in intesity'''

''' segment image based on non-grayness'''
''' Assume that segmenter should be around center'''
''' Find the edges where the derivative is sharp and take the median'''
''' Need to find a better criteripn for threshold_intensity, possibly be taking the norm'''

class CellSplitter:

    def __init__(self, cell_image_loc):
        image = cv2.imread(cell_image_loc)
        self.cell = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.rowLen, self.colLen = (self.cell).shape
        self.window_size = self.colLen/2
        
        #set guess at center
        self.idx = self.colLen/2
        
        #self.cell = cv2.bitwise_not(image)
        self.avg_vert = np.average(self.cell,axis=0)
        self.threshold_intensity_FD = 0.5
        
        self.diff_filter  = 1.0/3*(1*self.avg_vert[0:-2]+self.avg_vert[1:-1] + 1*self.avg_vert[2:])

        
        plt.subplot(2,1,1)
        plt.plot(self.avg_vert)
        plt.subplot(2,1,2)
        plt.ylim(-2,2)
        plt.plot(self.diff_filter[1:]-self.diff_filter[0:-1])
        
        plt.savefig('intensity.png')
        

        
    def split_cell(self):
        guess = int(self.colLen/2)
        #will be using finite difference
        halfWin = int(self.window_size/2)
        window_data = self.diff_filter[guess-halfWin: guess+halfWin+1]
        window_FD = window_data[1:]-window_data[0:-1]
        
        #find point where finite difference becomes first sharply positive
        #find point where finite difference becomes first sharply negative
        FD_left_max = 0
        left_idx = guess
        for ind in range(0, halfWin):
            print(window_FD[halfWin-ind])
            if window_FD[halfWin-ind] > FD_left_max + self.threshold_intensity_FD:
                FD_left_max = window_FD[halfWin-ind]
                left_idx = -ind
                break
                
        FD_right_min = 0
        right_idx = guess
        for ind in range(0, halfWin):
            if window_FD[halfWin+ind] < FD_right_min - self.threshold_intensity_FD:
                FD_right_min = window_FD[halfWin+ind]
                right_idx = ind
                break


        if (left_idx==guess or right_idx==guess):
            print('Image most likely not centered error; check split cell method in cell_splitter.py')
                
        
        idx_guess = guess + int( (right_idx+left_idx)/2 )
        
        print(left_idx, right_idx)
        print('Cell split at: ', idx_guess)
        
        return idx_guess
        
        
    def draw_splitter(self):
        x = self.split_cell()
        lineThickness =  5
        #x = 175
        
        y1 = 0
        y2 = self.rowLen
        cv2.line(self.cell, (x, y1), (x, y2), (0,255,0), lineThickness)
        cv2.imwrite('segment.jpg',self.cell)       
        
if __name__ == "__main__":
    fName = './img_files/table1_contours6.jpg'
    myCS = CellSplitter(fName)
    myCS.draw_splitter()
