import numpy as np
import cv2
from scipy import ndimage


''' Finds the minimum rectangle enclosing the scores'''
''' Divides up the rectangle into score boxes and saves relevant image files'''
''' Center the digit ?'''
''' Interesting part == use image recognition to identify the number'''

class TableFinder:

    def __init__(self, image_location, rows, columns):
        self.image_loc = image_location
        self.image = cv2.imread(image_location)
        self.table_corners = []
        self.table_width = 0
        self.table_height = 0
        self.upright_image = None
        self.rows = rows
        self.cols = columns
        self.cells = []


    #Get length and width of table
    def getTableDimensions(self, pt1, pt2, pt3, pt4):
        s1 = np.sqrt(np.linalg.norm(pt1-pt2,2))
        s2 = np.sqrt(np.linalg.norm(pt2-pt3,2))
        s3 = np.sqrt(np.linalg.norm(pt3-pt4,2))
        s4 = np.sqrt(np.linalg.norm(pt4-pt1,2))
        
        return s1, s2, s3, s4    


    def findTable(self, img):

        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(imgray,255,1,1,11,15)

        #find the countours 
        _, contours0,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        #Find the bounding rectangle
        if len(contours0) != 0:
            # draw in blue the contours that were founded
            #cv2.drawContours(img, contours0, -1, 255, 3)

            #find the biggest area
            c = max(contours0, key = cv2.contourArea)
            #cv2.drawContours(img, c, -1, 255, 3)

            
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            #img = cv2.drawContours(img,[box],0,(0,255,0),2)
            box = np.array(box)
            b1 = np.array(box[0])
            b2 = np.array(box[1])
            b3 = np.array(box[2])
            b4 = np.array(box[3])


        self.table_corners = b1, b2, b3, b4
        
        return b1, b2, b3, b4



    #Rotate so that the long side of the table is vertical and horizontal is shorter side
    def rotateImage(self):

        b1, b2, b3, b4 = self.findTable(self.image)
        s1, s2, s3, s4 = self.getTableDimensions(b1, b2, b3, b4)

        dp = b1 - b2
        if s1 < s2:
            temp = dp[0]
            dp[0] = dp[1]
            dp[1] = temp
            rotation_angle = -np.arctan2(dp[0],dp[1])*180/np.pi
        
        else :
            rotation_angle = np.arctan2(dp[0],dp[1])*180/np.pi


        rot_img = ndimage.rotate(self.image, -rotation_angle)
        
        return rot_img
        
        
    def orientTable(self):
        self.upright_image = self.rotateImage()
        self.table_corners = self.findTable(self.upright_image)
        

        
        
    def findCells(self):
    
        #b1 = top left; b2 = bottom left; b3 = bottom right; b4 = top right
        b1, b2, b3,b4 = self.table_corners
        self.orientTable()
        
        self.table_height = np.abs(b1[1]-b2[1])
        self.table_width = np.abs(b1[0]-b4[0])
        
        dw = int( self.table_width/self.cols)
        dh = int(self.table_height/self.rows)
        
        print(b1, b2, b3, b4)
        print(self.table_width)
        print(self.table_height)
        print('dw, dh', dw, dh)
        
        cell_rloc = b2[1]+np.arange(0,self.rows+1)*dh
        cell_rloc[self.rows] = b1[1]
        
        cell_cloc = b2[0]+np.arange(0,self.cols+1)*dw
        cell_cloc[self.cols] = b3[0]
        
        
        for indr in range(len(cell_rloc)-1):
            for indc in range(len(cell_cloc)-1):
                c1 = [cell_rloc[indr], cell_cloc[indc] ]
                c2 = [cell_rloc[indr+1], cell_cloc[indc] ]
                c3 = [cell_rloc[indr+1], cell_cloc[indc+1] ]
                c4 = [cell_rloc[indr], cell_cloc[indc+1] ]
                
            
                (self.cells).append([c1, c2,c3,c4]) 
                
    def drawCells(self):
        self.orientTable()
        self.findCells()
        self.upright_image
        lineThickness = 20
        
        cellind = 1
        for cell in self.cells:
        
            '''for pt in cell:
                y = pt[0]
                x = pt[1]
                cv2.circle(myTF.upright_image,(x, y), 10, (0,255,0), -1)'''
            
            y1,x1 = cell[0]
            y2,x2 = cell[1]
            y3,x3 = cell[2]
            y4,x4 = cell[3]
            '''cv2.line(self.upright_image, (x1, y1), (x2, y2), (0,255,0), lineThickness)
            cv2.line(self.upright_image, (x2, y2), (x3, y3), (0,255,0), lineThickness)
            cv2.line(self.upright_image, (x3, y3), (x4, y4), (0,255,0), lineThickness)
            cv2.line(self.upright_image, (x4, y4), (x1, y1), (0,255,0), lineThickness)'''
            if (cellind>3 and (cellind%3==0 or cellind%3==2)):
                cv2.imwrite('table1_contours'+str(cellind)+'.jpg',myTF.upright_image[y1:y2, x1:x3])
            cellind +=1
         
        
        
        
    

if __name__ == "__main__":
    fName = 'table2.jpg'
    myTF = TableFinder(fName,7,3)
    #myTF.upright_image = myTF.rotateImage()
    #pt1, pt2, pt3, pt4 = myTF.findTable(myTF.upright_image)
    myTF.drawCells()
    print('cells are\n', myTF.cells)

    #s1, s2, s3, s4 = myTF.getTableDimensions(pt1, pt2, pt3, pt4)
    #print('Point locations')
    #print(pt1, pt2, pt3, pt4)
    #print(s1, s2)
    #print(myTF.table_height, myTF.table_width)

    #print(pt1)
    
    #cv2.circle(myTF.upright_image,(pt1[0], pt1[1]), 5, (0,255,0), -1)
    #cv2.circle(myTF.upright_image,(pt2[0], pt2[1]), 5, (0,0,255), -1)
    cv2.imwrite('table1_contours.jpg',myTF.upright_image)
