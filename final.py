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
    
   
    
    #for getting height and width of image so as to use it further as coordintaes
    (h,w)=cimg.shape[:2]
    #print(h)
    #print(w)
    
    count=1
    sum1=0
    #print(circles)
    
    circles = cv2.HoughCircles(im2,cv2.HOUGH_GRADIENT,1,150,param1=50,param2=30,minRadius=0,maxRadius=0)
    
    print(circles)
   # print('111')
   

    if(circles!=None):
        #print('111')
        circles = np.uint16(np.around(circles))#converting the x-coordinate,y-coordinate of center and radius to integers
        #print(circles)
        print('111')
        for i in circles[0,:]:
            
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),2)  #i[0]=x,i[1]=y&i[2]=radius,(0,0,255)->red color,2=thickness
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(255,0,0),2)  #(255,0,0)->blue for centre
            sum1+=22*i[2]*i[2]/7
            
            
            if i[0]<(w/2) and i[1]<(h/2):
                print("ball",count,"position=top left")
            elif i[0]>(w/2) and i[1]<(h/2):
                print("ball",count,"position=top right")
            elif i[0]<(w/2) and i[1]>(h/2):
                print("ball",count,"position=bottom left")
            elif i[0]>(w/2) and i[1]>(h/2):
                print("ball",count,"position=bottom right")
            count+=1   
        percent_area=(sum1/(h*w))*100
        print(percent_area)
        
        arduino = serial.Serial('COM7',9600)    #Create Serial port object called arduinoSerialData
        time.sleep(2)    #wait for 2 secounds for the communication to get established
        print(arduino.readline())    #read the serial data and print it as line
        if (count-1)>=1:
            arduino.write('1')
            time.sleep(1)
        else if(count-1)<=1:
            arduino.write('0')
            time.sleep(1)
   
   
    cv2.imshow('frame',cimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
         
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
