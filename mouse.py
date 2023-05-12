import cv2 as cv
import numpy as np
import pyautogui

cam = cv.VideoCapture(0)

lower_orange = np.array([5,100,100])
upper_orange = np.array([15,255,255])

lower_green = np.array([50,100,100])
upper_green = np.array([80,255,255])

lower_violet = np.array([20,100,100])
upper_violet = np.array([40,255,255])
while(True):        
        ret,frame = cam.read()
        frame = cv.flip(frame,1)

        #Smoothen the image
        image_smooth = cv.GaussianBlur(frame,(7,7),0)

        #Define ROI
        mask = np.zeros_like(frame)
        mask[100:350,100:350] = [255,255,255]
        image_roi = cv.bitwise_and(image_smooth,mask)
        cv.rectangle(frame,(50,50),(350,350),(0,0,255),2)
        cv.line(frame,(150,50),(150,350),(0,0,255),1)
        cv.line(frame,(250,50),(250,350),(0,0,255),1)
        cv.line(frame,(50,150),(350,150),(0,0,255),1)
        cv.line(frame,(50,250),(350,250),(0,0,255),1)

        #Threshold the image for orange color
        image_hsv = cv.cvtColor(image_roi,cv.COLOR_BGR2HSV)
        image_threshold = cv.inRange(image_hsv,lower_orange,upper_orange)

        #Find Contours
        contours,heirarchy = cv.findContours(image_threshold, \
                                                           cv.RETR_TREE, \
                                                           cv.CHAIN_APPROX_NONE)

        #Find the index of the largest contour
        if(len(contours)!=0):
                areas = [cv.contourArea(c)  for c in contours]
                max_index = np.argmax(areas)
                cnt = contours[max_index]
 
                #pointer on video
                M = cv.moments(cnt)
                if(M['m00']!=0):
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv.circle(frame, (cx,cy),4,(0,255,0),-1)

                        # Cursor Motion
                        if cx < 150:
                                dist_x = -20
                        elif cx > 250:
                                dist_x = 20
                        else:
                                dist_x = 0

                        if cy < 150:
                                dist_y = -20
                        elif cy > 250:
                                dist_y = 20
                        else:
                                dist_y = 0
                        pyautogui.FAILSAFE = False
                        pyautogui.moveRel(dist_x,dist_y,duration=0.25)

                # Check for left click
                image_threshold_green = cv.inRange(image_hsv, lower_green, upper_green)
                contours_green,heirarchy = cv.findContours(image_threshold_green,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
                                                            

                if(len(contours_green)!=0):
                        pyautogui.click()
                        cv.waitKey(1000)


                
                # Check for Right click
                image_threshold_violet = cv.inRange(image_hsv, lower_violet, upper_violet)
                contours_violet,heirarchy = cv.findContours(image_threshold_violet,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)


                if(len(contours_violet)!=0):
                        pyautogui.click(button='right')
                        cv.waitKey(1000)                
                                                
        cv.imshow('Frame',frame)
        if cv.waitKey(10) == 27:
                break


cam.release()
cv.destroyAllWindows()