import cv2
import numpy as np

#C:\Users\Artorn\TestPy\Smile\Face_eyes_smile-detection-master

face_cascade = cv2.CascadeClassifier("frontalface_default.xml")

eye_cascade = cv2.CascadeClassifier("eye.xml")

smile_cascade = cv2.CascadeClassifier("smile.xml")

cap = cv2.VideoCapture(0)

while True:

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        smile = smile_cascade.detectMultiScale(roi_gray,
                                               scaleFactor=1.7,
                                               minNeighbors=22,
                                               minSize=(25, 25),
                                               )

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

        for (ex, ey, ew, eh) in smile:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,255), 2)
           
            text = "Smile"
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

            cv2.imwrite('opencv.png', img)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
