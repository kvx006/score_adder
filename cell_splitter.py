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
        avg_value = np.average(self.avg_vert)
        self.threshold_intensity_FD = 0.5
        
        self.diff_filter  = 1.0/3*(1*self.avg_vert[0:-2]+self.avg_vert[1:-1] + 1*self.avg_vert[2:])

        

        
        plt.subplot(2,1,1)
        plt.plot(self.avg_vert)
        plt.subplot(2,1,2)
        #plt.ylim(-0.02,0.02 )
        plt.plot(np.log(self.avg_vert/avg_value))
        #plt.plot(self.diff_filter[1:]-self.diff_filter[0:-1])
        #plt.plot(self.avg_vert[1:]-self.avg_vert[0:-1])


        plt.savefig(cell_image_loc+'intensity.png')
        plt.close()

        idxs = self.remove_vert_lines()
        idx_min = np.amin(idxs)
        idx_max = np.amax(idxs)
        
        
        idxs_horiz = self.remove_horizontal_lines()
        idxs_h_min = np.amin(idxs_horiz)
        idxs_h_max = np.amax(idxs_horiz)

        buffer_size = 5
        for idx in range(idx_min-buffer_size,idx_max+buffer_size):
            if (idx >0 and idx < len(self.diff_filter)):
                self.cell[:,idx] = np.average(self.avg_vert)
                self.diff_filter[idx] = np.average(self.diff_filter)

        
        for idx_h in range(idxs_h_min-buffer_size, idxs_h_max+buffer_size):
            if (idx_h >0 and idx_h < len(self.avg_horizontal)):
                self.cell[idx_h,:] = np.average(self.avg_horizontal)
                #self.diff_filter[idx] = np.average(self.diff_filter)
        
        
        plt.plot(self.diff_filter)
        plt.savefig('remove_vert_line.png')


        

    #What if we have only one min?
    def split_cell(self):
        guess = int(len(self.diff_filter)/2)
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
                
        
        #print(left_idx, right_idx)
        #print('Cell split at: ', idx_guess)
        
        return idx_guess
        
    #find max between mins
    def valley_peak_split(self):
            
        #Split cell into eigths, imagin 1/8 are border vaulues, so leave those out  
        llim = int(len(self.diff_filter)*1./8.)
        rlim = llim*7
        print("splittings", llim, 2*llim, 3*llim, 4*llim, 5*llim, 6*llim, 7*llim, 8*llim)
        arr_1  = self.diff_filter[llim : 3*llim]
        arr_2 = self.diff_filter[5*llim : 7*llim]
        min_1_idx = self.find_local_min(arr_1)+llim
        min_2_idx = self.find_local_min(arr_2)+5*llim
        
        #left min near center
        if (min_1_idx == llim):
            min_1_idx  = self.find_local_min(self.diff_filter[llim : 4*llim]) + llim
        
        #right min near cener
        if (min_2_idx == 5*llim):
            min_2_idx = self.find_local_min(self.diff_filter[4*llim : 7*llim])+4*llim


        guess = int(self.colLen/2)        
        if min_1_idx != min_2_idx:
            guess = int((min_1_idx+min_2_idx)/2.0)
        
        
        print('idxs ', min_1_idx, min_2_idx)
        return self.find_local_max(self.diff_filter[llim+min_1_idx:llim+min_2_idx])+(min_1_idx)
        
     
     
    def remove_vert_lines(self):
         
         diff_filter_avg = np.average(self.diff_filter)
         idx_to_set_zero = []
         for ind in range(len(self.diff_filter)):
            if np.abs(diff_filter_avg - self.diff_filter[ind]) > 30:
                idx_to_set_zero.append(ind)
        
         
         return idx_to_set_zero
         
    def remove_horizontal_lines(self):
        self.avg_horizontal = np.average(self.cell,axis=1)
        diff_filter_avg = np.average(self.avg_horizontal)
        idx_to_set_zero = []
        for ind in range(len(self.avg_horizontal)):
            if np.abs(diff_filter_avg - self.avg_horizontal[ind]) > 30:
                idx_to_set_zero.append(ind)


        return idx_to_set_zero

         


    #given an array, find a local min and return index
    def find_local_min(self,arr):
        min_val = 10000
        min_idx = 0
        tol_value = 2
        avg = np.average(arr)
        for ind in range(len(arr)):
            #print(ind,  arr[ind])
            if ( arr[ind] < min_val):
                min_idx = ind
                min_val = arr[ind]
                
        
            #see if minimum is truly a valley
            #Need to change here
            #if arr[ind] > avg - tol_value:
            #    min_idx = 0
        
        return min_idx
        

    def find_local_max(self,arr):
        max_val = -10000
        max_idx = 0
        tol_value = 0.1
        avg = np.average(arr)
        for ind in range(len(arr)):
            if ( arr[ind] > max_val):
                max_idx = ind
                max_val = arr[ind]
        
            #see if max is truly a peaks
            #Need to change here
            #print(avg, tol_value, arr[ind])
            #if arr[ind] < avg - tol_value:
                #max_idx = 0
        
        return max_idx

        
        


        
    def draw_splitter(self):
        #x = self.split_cell()
        x = self.valley_peak_split()
        #print('x', x)
        lineThickness =  5
        #x = 175
        
        y1 = 0
        y2 = self.rowLen

        cv2.imwrite('segment_1.jpg',self.cell[0:y2,0:x])       
        cv2.imwrite('segment_2.jpg',self.cell[0:y2,x:])       
        cv2.line(self.cell, (x, y1), (x, y2), (0,255,0), lineThickness)        
        cv2.imwrite('segment.jpg', self.cell)
        
if __name__ == "__main__":
    fName = './img_files/table1_contours5.jpg'
    myCS = CellSplitter(fName)
    myCS.draw_splitter()
