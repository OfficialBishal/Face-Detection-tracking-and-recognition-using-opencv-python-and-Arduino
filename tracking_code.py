### By Bishal Shrestha
### this program is based on the haar_cascade classifier which are based on  Viola and Jones algorithm
### this program is creating database of the detected face during real time

import numpy as np
import cv2
import serial
import pickle



ser = serial.Serial(port='/dev/tty.usbmodem14111',baudrate=9600,timeout=1) #change this according to your system, here I have used for my mac


#this function will create the box arround the detcted face
def create_box(a,b,c,d):
    cv2.rectangle(imag,(a,b),(a+c,b+d),(0,255,0),2)

def variable_itteration(l):
    l=l+1
    return(l)

def write_image():
    save_image= imag[y:y+h, x:x+w] #cut out the face portion from image
    cv2.imwrite("hey%d.png"%(n),save_image)

# This will send data to the arduino according to the x coordinate
def angle_servox(angle):

    if angle>600:
        prov=1
        ser.write(b'1')
        print("Right")


    elif angle<400:
        prov=2
        ser.write(b'2')
        print("Left")

    elif angle>400 & angle<600:
        ser.write(b'0')
        print("Stop")

# This will send data to the arduino according to the y coordinate
def angle_servoy(angle):

    if angle>250:
        prov=3
        ser.write(b'3')
        print("Down")


    elif angle<100:
        prov=4
        ser.write(b'4')
        print("Up")

    elif angle>50 & angle<250:
        ser.write(b'5')
        print("Stop")

# import the haarcascade file
face_casc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#train the face for recognition
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

# for default camera put value 0 or else 1
videoWeb = cv2.VideoCapture(1)

n=0

while (videoWeb.isOpened()):

    ret,imag = videoWeb.read()
    gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('xyz',imag)
    faces = face_casc.detectMultiScale(imag, 1.2, 5, minSize=(10,10),maxSize=(500,500))
    for (x,y,w,h) in faces:

        roi_gray = gray[y:y + h, x:x + w]  # (ycord_start, ycord_end)
        roi_color = imag[y:y + h, x:x + w]
        # recognize? deep learned model predict keras tensorflow ytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 4 and conf <= 85:
            # print(5: #id_)
            # print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(imag, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = "7.png"
        cv2.imwrite(img_item, roi_color)

        create_box(x,y,w,h)
        n=variable_itteration(n)
        # If you want to save all the detected face,then uncomment the following line
        #write_image()

        # calling function to send serial data of angle to rotate servo motor
        angle_servox(x)
        angle_servoy(y)

      #this is very helpful for calibrating servomotors
        print(x)
        print(y)

#press q to close the program
    cv2.imshow('image',imag)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

videoWeb.release()
cv2.destroyAllWindows()
