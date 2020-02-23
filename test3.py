from flask import Flask, render_template

app = Flask(__name__)
@app.route('/execute')

def execute():
    
    x="hello"
    #return x
    
    import cv2
    import numpy as np

    img=cv2.imread('/home/anika/Downloads/712d7A89SDL._SL1500_.jpg',1)
    #img=cv2.imread('/home/anika/Downloads/green1.jpg',1)
    hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)

    lb=np.array([40,100,100])
    ub=np.array([90,255,255])

    r=cv2.inRange(hsv,lb,ub)
    im2=cv2.bitwise_and(img,img,mask=r)
    #cv2.imshow('a',r)
    #cv2.imshow('result',im2)

    #to detect a circle(hough gradient method)
    im2=cv2.cvtColor(im2,cv2.COLOR_RGB2GRAY)
    im2 = cv2.medianBlur(im2,5)
    cimg =cv2.cvtColor(im2,cv2.COLOR_GRAY2RGB)
    #im2=cv2.GaussianBlur(im2,(5,5),0)


    circles = cv2.HoughCircles(im2,cv2.HOUGH_GRADIENT,1,100,
                            param1=50,param2=40,minRadius=50,maxRadius=0)

    circles = np.uint16(np.around(circles))#converting the coordinates to integers

    (h,w)=cimg.shape[:2]
    #print(circles)

    p=1
    sum1=0
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),2)#i[0]=x,i[1]=y&i[2]=radius,0,0,255->red color,2=thickness
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(255,0,0),2)#0,0,255->blue for centre ,second parameter is for radius of centre 
        sum1+=22*i[2]*i[2]/7
        l=list()
        
        
        if i[0]<(w/2) and i[1]<(h/2):
            print("ball",p,"position=top left")
            l.append("ball")
            l.append("position=top left")
            #cv2.putText(cimg,'Bottom Left',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
        elif i[0]>(w/2) and i[1]<(h/2):
            print("ball",p,"position=top right")
            l.append("ball")
            l.append("position=top right")
            #cv2.putText(cimg,'Bottom Right',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
        elif i[0]<(w/2) and i[1]>(h/2):
            print("ball",p,"position=bottom left")
            l.append("ball")
            l.append("position=bottom left")
            #cv2.putText(cimg,'Top Left',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
        elif i[0]>(w/2) and i[1]>(h/2):
            print("ball",p,"position=bottom right")
            l.append("ball")
            l.append("position=bottom right")
            #cv2.putText(cimg,'Bottom Left',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
        p+=1
    percent_area=(sum1/(h*w))*100
    
    l.append(percent_area)
    for i in range(0,len(l)):
        print(l[i])
    
    #print(count)
    #print(circles[0][0])
    #l=circles.transpose(2,0,1).reshape(3,-1)
    #print(l)
    #print(l[1][0])
    
    print(h)
    print(w)
    
    cv2.imshow('detected GREEN circles',cimg)
    #return render_template('/home/anika/Desktop/Templates/index.html',len=len(l),l=l)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  

@app.route('/')  
def home(): 
    # running app 
    app.run(use_reloader = True, debug = True)   
'''
def home():
    output= execute('./test3.py')
    
    #print(output)
'''    
