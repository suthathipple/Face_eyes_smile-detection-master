#! /usr/bin/python

import cv2
from itertools import count

face_cascade = cv2.CascadeClassifier('frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('eye.xml')

# Load the overlay image: glasses.png
imgGlasses = cv2.imread('Mask2web.png')

#Check if the files opened
if  imgGlasses is None :
    exit("Could not open the image")
if  face_cascade.empty() :
    exit("Missing: haarcascade_frontalface_default.xml")
if  eye_cascade.empty() :
    exit("Missing: haarcascade_eye.xml")


# Create the mask for the glasses
imgGlassesGray = cv2.cvtColor(imgGlasses, cv2.COLOR_BGR2GRAY)
ret, orig_mask = cv2.threshold(imgGlassesGray, 10, 255, cv2.THRESH_BINARY)

#orig_mask = imgGlasses[:,:,3]

# Create the inverted mask for the glasses
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert glasses image to BGR
# and save the original image size (used later when re-sizing the image)
imgGlasses = imgGlasses[:,:,0:3]
origGlassesHeight, origGlassesWidth = imgGlasses.shape[:2]

#cv2.imshow('Video', imgGlasses)
#cv2.waitKey()


video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened() :
    exit('The Camera is not opened')


counter = count(1)

while True:
    #print "Iteration %d" % counter.next()
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        #cv2.imshow('Video', roi_gray)
        #cv2.waitKey()

        #print 'X:%i, Y:%i, W:%i, H:%i' % (x, y, w, h)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            #print 'EX:%i, EY:%i, EW:%i, EH:%i' % (ex, ey, ew, eh)

        for (ex, ey, ew, eh) in eyes:
            glassesWidth = 3*ew
            glassesHeight = glassesWidth * origGlassesHeight / origGlassesWidth

            # Center the glasses on the bottom of the nose
            x1 = ex - (glassesWidth/4)
            x2 = ex + ew + (glassesWidth/4)
            y1 = ey + eh - (glassesHeight/2)
            y2 = ey + eh + (glassesHeight/2)

                # Check for clipping
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > w:
                x2 = w
            if y2 > h:
                y2 = h

            # Re-calculate the width and height of the glasses image
            glassesWidth = x2 - x1
            glassesHeight = y2 - y1

            # Re-size the original image and the masks to the glasses sizes
            # calcualted above
            glasses = cv2.resize(imgGlasses, (glassesWidth,glassesHeight), interpolation = cv2.INTER_AREA)
            mask = cv2.resize(orig_mask, (glassesWidth,glassesHeight), interpolation = cv2.INTER_AREA)
            mask_inv = cv2.resize(orig_mask_inv, (glassesWidth,glassesHeight), interpolation = cv2.INTER_AREA)

            # take ROI for glasses from background equal to size of glasses image
            roi = roi_color[y1:y2, x1:x2]

            # roi_bg contains the original image only where the glasses is not
            # in the region that is the size of the glasses.
            roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

            # roi_fg contains the image of the glasses only where the glasses is
            roi_fg = cv2.bitwise_and(glasses,glasses,mask = mask)

            # join the roi_bg and roi_fg
            dst = cv2.add(roi_bg,roi_fg)

            # place the joined image, saved to dst back over the original image
            roi_color[y1:y2, x1:x2] = dst
    #break
    #Display the resulting frame
    cv2.imshow('Video', frame)
    cv2.waitKey()   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()