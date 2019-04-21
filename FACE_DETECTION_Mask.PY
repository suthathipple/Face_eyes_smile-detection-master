import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("frontalface_default.xml")

# Load the overlay image: glasses.png
imgGlasses = cv2.imread('Mask2web.png')

# Create the mask for the glasses
imgGlassesGray = cv2.cvtColor(imgGlasses, cv2.COLOR_BGR2GRAY)
ret, orig_mask = cv2.threshold(imgGlassesGray, 10, 255, cv2.THRESH_BINARY)

# Create the inverted mask for the glasses
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert glasses image to BGR
# and save the original image size (used later when re-sizing the image)
imgGlasses = imgGlasses[:,:,0:3]
origGlassesHeight, origGlassesWidth = imgGlasses.shape[:2]


cap = cv2.VideoCapture(0)

"""

background = cv2.imread('field.jpg')
overlay = cv2.imread('dice.png')

added_image = cv2.addWeighted(background,0.4,overlay,0.1,0)

cv2.imwrite('combined.png', added_image)
"""

while True:

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
