#Importing Required Libraries
import cv2 
import numpy as np 
import time 

#capturing video from webcam
cap = cv2.VideoCapture(0)

#giving time to adjust according to webcam
time.sleep(4)

#Initializing background
background= 0


#Giving 30 iterations to get best background data
for i in range(40):
    ret,background=cap.read()

#Running till video is opened 
while (cap.isOpened()):

    #Reading image from video
    ret,img= cap.read()

    #Breaking if image not captured    
    if not ret:
        break 
    

    #Converting RGB to HSV 
    hsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    #Setting the limit of cloak color 
    lower_limit_red = np.array([0,98,100])
    upper_limit_red = np.array([10,255,255])
    #creating a mask from color limit
    mask1=cv2.inRange(img,lower_limit_red,upper_limit_red)

    #Setting Limit for background
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    #Concatenating mask to detect red color
    mask1 = mask1 + mask2

    ## Open and Dilate the mask image 
    ## It is done to reduce noise and to increase object area
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)

    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img, img, mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask=mask1)

    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("Invisible!!", finalOutput)
    Q = cv2.waitKey(10)
    if Q == 27:
        break

cap.release()
cv2.destroyAllWindows()
