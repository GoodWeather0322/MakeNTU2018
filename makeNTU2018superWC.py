# For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import requests
import urllib.request
import cv2
import numpy as np
import threading
import time
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import serial

%matplotlib inline

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print( "Starting " + self.name)
        face_detect(self.name)
        print( "Exiting " + self.name)

def face_detect(threadName):
    face_api_url = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0/detect'

    params = {
    'subscription-key': "6dff3941a6c24ce392f9524b9cf9a5cd",
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    } 

    headers = {
        'Content-type': 'application/octet-stream',
    }
    body = "" 

    #load image
    image_url = 'D:\Jupyter\data.jpg'

    f = open(image_url, "rb")

    body = f.read()

    f.close()

    #conn = http.client.HTTPSConnection('https://eastasia.api.cognitive.microsoft.com')

    #conn.request("POST", "/face/v1.0/?%s" % params, body, headers)
    response = requests.post(face_api_url, params=params, data=body, headers=headers)

    #response = conn.getresponse("")

    faces = response.json()

    print(faces)
    

    
    
    
    #response = requests.get(image_url)
    image = Image.open(image_url)
    plt.figure(figsize=(8,8))
    ax = plt.imshow(image, alpha=0.8)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]), fontsize=20, weight="bold", va="bottom")
    _ = plt.axis("off")
    
    if fa["gender"]==None:
        contents = urllib.request.urlopen("http://linebot-arduino-test.herokuapp.com/btn?key=55688&id=alarm").read()
    
    if fa["gender"]=='male':
        contents = urllib.request.urlopen("http://linebot-arduino-test.herokuapp.com/btn?key=55688&id=alarm").read()
        s.write('H'.encode())
    
    #print(fa["gender"])
    fig = plt.gcf()
    fig.savefig('solution.jpg',bbox_inches='tight')
    plt.show()

    #conn.close()
        
def streaming():
    #ser = serial.Serial('COM9', 9600)
    #s = ser.read(20)
    have=False
    printcount=0
    cap = cv2.VideoCapture(0)
    currentFrame = 0
    #ret, pic = cap.read()
    while(True):
        # Capture frame-by-frame
        printcount += 1
        if printcount == 20:
            print(s.read())
            printcount = 0
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame',frame)
        #cv2.imshow('pic', pic)

        #if cv2.waitKey(1) & 0xFF == ord('c'):
            #ret, pic = cap.read()
            #pic = cv2.flip(frame, 2)q
            #cv2.imshow('pic', pic)
            #thread1 = myThread(1, "Thread-facedetect", pic)
            #cv2.imwrite('data.jpg', pic)
            #thread1 = myThread(1, "Thread-facedetect")
            #thread1.start()
          
        if have==False :
            if s.read() == b'y':
                ret, pic = cap.read()
                #pic = cv2.flip(frame, 2)q
                #cv2.imshow('pic', pic)
                #thread1 = myThread(1, "Thread-facedetect", pic)
                cv2.imwrite('data.jpg', pic)
                thread1 = myThread(1, "Thread-facedetect")
                thread1.start()
                have=True
            

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # To stop duplicate images
        currentFrame += 1
        
        if have == True:
            if s.read() != b'y' :
                have=False

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    s=serial.Serial("com9",9600)
    streaming()
