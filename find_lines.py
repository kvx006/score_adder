import cv2
import numpy as np
from scipy import stats
import imutils

img = cv2.imread('table1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,100,200,apertureSize = 3)
#cv2.imshow('edges',edges)
#cv2.waitKey(0)

minLineLength = 200
maxLineGap = 10
line_length = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
angles = []
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        d = np.sqrt( np.power(x1-x2,2)+np.power(y1-y2,2) )
        dy = y2-y1
        dx = x2-x1

        angle = np.arctan2(dy,dx)
        #if angle !=0 and angle !=np.pi/2 and angle !=-np.pi/2:
        #if angle != 0 and angle !=-np.pi/2 and angle !=np.pi/2:
        angles.append(angle )
        #print(d)
        #if d > line_length:
           # cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            
print(angles)
rot_angle = stats.mode(angles)[0]*(180/np.pi)

rotated = imutils.rotate(gray, 0*(rot_angle))

edges = cv2.Canny(rotated,100,200,apertureSize = 3)

minLineLength = 100
maxLineGap = 10
line_length = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)

for x in range(0, len(lines)):
    print(lines)
    for x1,y1,x2,y2 in lines[x]:
        d = np.sqrt( np.power(x1-x2,2)+np.power(y1-y2,2) )
        dy = y2-y1
        dx = x2-x1


        print(d)
        #if d > line_length:
        cv2.line(rotated,(x1,y1),(x2,y2),(0,255,0),2)            





cv2.imwrite('table1_rotated.jpg',rotated)
