from collections import deque
import argparse
import numpy as np
import imutils
import serial
import time
import cv2

cap=cv2.VideoCapture(0)
#pts =[]
lb=np.array([40,100,100])
ub=np.array([90,255,255])

arduino = serial.Serial('/dev/ttyACM0',9600)
time.sleep(2)

while(True):
    count=0
    pts=[]
    rad=[]
    ret, frame=cap.read()
    frame=imutils.resize(frame,height=640,width=400)
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask1=cv2.inRange(img,lb,ub)
    mask2=cv2.bitwise_and(img,img,mask=mask1)
    (h,w)=frame.shape[:2]

    
    cnts=cv2.findContours(mask1.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    cnts = imutils.grab_contours(cnts)
    #frame=cv2.drawContours(mask1.copy(), cnts, -1, (255,0,255), 3)

    center = None
    count=0
    for i in range(len(cnts)):
        #c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
        M = cv2.moments(cnts[i])
        if(M["m00"]==0):
            continue
        else:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            #print(radius)
            
            if radius > 20:
                c=()
                
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.append(center)
                rad.append(radius)
                c=center
                #print(center)
                count=count+1
                area=0
                #tot=0
                for j in range(len(pts)):
                    print("Data for Ball",j+1)
                    
                    if pts[j][0]<(w/2) and pts[j][1]<(h/2):
                        print("position of ball",j+1,"is  =top left")
                    elif pts[j][0]>(w/2) and pts[j][1]<(h/2):
                        print("position of ball ",j+1,"is =top right")
                    elif pts[j][0]<(w/2) and pts[j][1]>(h/2):
                        print("position of ball ",j+1,"is =bottom left")
                    elif pts[j][0]>(w/2) and pts[j][1]>(h/2):
                        print("position of ball",j+1,"is =bottom right ")
                    
                    area+=22/7*rad[j]**2
                    #tot+=1
                percentage=area/(h*w)*100
                print('Percentage area occupied by ball = ',percentage,'%')
            print(count)
            if(count>0):
                arduino.write(('1').encode())
            else:
                arduino.write(('0').encode())
                                    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        arduino.write(('0').encode())
        break
cap.release()
cv2.destroyAllWindows
           
           
