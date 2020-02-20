
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret,frame = cap.read()
    
    # Our operations on the frame come here
    im2 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #img=cv2.imread('/home/anika/Downloads/green1.jpg',1)
    #hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    
    lb=np.array([40,100,100])
    ub=np.array([90,255,255])
    r=cv2.inRange(im2,lb,ub)
    im2=cv2.bitwise_and(im2,im2,mask=r)
    #cv2.imshow('a',r)
    #cv2.imshow('result',im2)
    
#to detect a circle(hough gradient method)
    im2=cv2.cvtColor(im2,cv2.COLOR_HSV2RGB)
    im2=cv2.cvtColor(im2,cv2.COLOR_RGB2GRAY)
    im2=cv2.medianBlur(im2,5)
    cimg=cv2.cvtColor(im2,cv2.COLOR_GRAY2RGB)
    
    '''The function cv2.HoughCircles() contains the following arguments:image, method, dp, minDist,param1,param2,minradius,maxradius.
    Colored images are converted to grayscale images as we need an 8-bit single channel image,
    method:method used to detect the circles,minDist:minimum distance between the
    center coordinates of the circles'''
    
    circles = cv2.HoughCircles(im2,cv2.HOUGH_GRADIENT,1,150,param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))#converting the x-coordinate,y-coordinate of center and radius to integers
    
    #print(circles)
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),2)  #i[0]=x,i[1]=y&i[2]=radius,(0,0,255)->red color,2=thickness
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(255,0,0),2)  #(255,0,0)->blue for centre
    
    #for getting height and width of image so as to use it further as coordintaes
    (h,w)=cimg.shape[:2]
    print(h)
    print(w)
    
    cv2.imshow('frame',cimg)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
         
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
