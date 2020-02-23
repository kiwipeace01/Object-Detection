import cv2
import numpy as np
img1=cv2.imread('/home/koushiki/Downloads/big-green-ball-260nw-167005415.jpg',1)
img1=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
lb=np.array([30,70,70])
ub=np.array([90,255,255])
r=cv2.inRange(img1,lb,ub)
img1=cv2.bitwise_and(img1,img1,mask=r)
img1= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
mask = cv2.threshold(img1,127, 255, cv2.THRESH_BINARY_INV)[1]
edges = cv2.Canny(mask, 40, 90)

contours,hierarchy = cv2.findContours(mask,2,1)
cnt1 = contours[0]
cap = cv2.VideoCapture(0)
while(True):
    ret,frame = cap.read()
    im2 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


    lb=np.array([30,70,70])
    ub=np.array([90,255,255])
    r=cv2.inRange(im2,lb,ub)
    im2=cv2.bitwise_and(im2,im2,mask=r)
    im2 = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    thresh2 = cv2.threshold(im2,127, 255, cv2.THRESH_BINARY_INV)[1]
    contours,hierarchy = cv2.findContours(thresh2,2,1)
    cnt2 = contours[0]
    
    ret=cv2.matchShapes(cnt1,cnt2,1,0.0)
    
    if(ret>1):
        cv2.imshow('result2',thresh2)
        arduino = serial.Serial('/dev/ttyACM0',9600) 
        time.sleep(2)
        var='1'
        arduino.write(var.encode())
        cv2.imshow('result2',thresh2)
        
    cv2.imshow('result1',edges)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
