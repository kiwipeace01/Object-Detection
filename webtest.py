from collections import deque
import argparse
import numpy as np
import imutils
import serial
import time
import cv2
from flask import Flask,render_template, Response

app=Flask(__name__)

@app.route('/')
def index():
    #homepage
    return render_template('index1.html')

class vi():
    
    def position(h,w,x,y,j):
        print("Data for Ball",j+1)
        if x<(w/2) and y<(h/2):
            print("position of ball",j+1,"is  =top left")
        elif x>(w/2) and y<(h/2):
            print("position of ball ",j+1,"is =top right")
        elif x<(w/2) and y>(h/2):
            print("position of ball ",j+1,"is =bottom left")
        elif x>(w/2) and y>(h/2):
            print("position of ball",j+1,"is =bottom right ")   
                                                          
                            
                                 
    def gen():
        
        cap = cv2.VideoCapture(0)
        arduino = serial.Serial('/dev/ttyACM0',9600)
        time.sleep(2)

        
        while(True):
            
        # Capture frame-by-frame
            #return render_template('index1.html',parea=x)
                            
            ret,img= cap.read()
            #img=cv2.imread('/home/anika/Downloads/552964.jpg')
            if ret==True:
                
                lb=np.array([40,100,100])
                ub=np.array([90,255,255])
               
                count=0
                pts=[]
                rad=[]
                #ret, frame=cap.read()
                img=imutils.resize(img,height=640,width=400)
                img2=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
                mask1=cv2.inRange(img2,lb,ub)
                mask2=cv2.bitwise_and(img2,img2,mask=mask1)
                (h,w)=img.shape[:2]
                
                cnts=cv2.findContours(mask1.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
                cnts = imutils.grab_contours(cnts)
                #frame=cv2.drawContours(mask1.copy(), cnts, -1, (255,0,255), 3)

                center = None
                count=0
                    
                
                #print(cnts)
                
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
                            
                            cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                            cv2.circle(img, center, 5, (0, 0, 255), -1)
                            pts.append(center)
                            rad.append(radius)
                            c=center
                            #print(center)
                            count=count+1
                            area=0
                            #tot=0
                            
                            for j in range(len(pts)):
                                x=pts[j][0]
                                y=pts[j][1]
                                vi.position(h,w,x,y,j)
                               
                               area+=22/7*rad[j]**2
                               
                            percentage=area/(h*w)*100
                            print('Percentage area occupied by balls = ',percentage,'%')
                            
                        #print(count)
                        
                        if(count>0):
                            arduino.write(('1').encode())
                        else:
                            arduino.write(('0').encode())
                        
            
                img=cv2.resize(img,(0,0),fx=2.0,fy=2.0)
                frame=cv2.imencode('.jpg',img)[1].tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+
                    frame + b'\r\n')
                time.sleep(0.1)
            else:
                break

    
@app.route('/video_feed')
def video_feed():
    return Response(vi.gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
