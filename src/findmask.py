import os
import cv2
import argparse
import numpy as np
path = os.getcwd() + '/'
faceCascade = cv2.CascadeClassifier(path + 'assets/models/face.xml')
mouthCascade = cv2.CascadeClassifier(path + 'assets/models/mouth.xml')

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
args = parser.parse_args()

image = cv2.imread((args.path).split('=')[1])
image = cv2.resize(
    image, None, fx = 0.5, fy = 0.5,
    interpolation = cv2.INTER_CUBIC
)

imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh, imageBlackAndWhite = cv2.threshold(imageGray, 80, 255, cv2.THRESH_BINARY)

faces = faceCascade.detectMultiScale(imageGray, 1.1, 4)
facesBlackAndWhite = faceCascade.detectMultiScale(imageBlackAndWhite, 1.1, 4)
mouthContours = mouthCascade.detectMultiScale(imageGray, 1.5, 5)

faceContours = faces if (len(faces) > 0) else facesBlackAndWhite
foundFace = (len(faces) > 0) or (len(facesBlackAndWhite) > 0)
foundMouth = (len(mouthContours) > 0)
wearingMask = foundFace and not(foundMouth)
color = (0, 0, 255) if (foundMouth) else (0, 255, 0)

for (x, y, w, h) in faceContours:
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

if not(foundFace):
    cv2.putText(image, "No face found...", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

cv2.imshow('Output', image)
cv2.waitKey(0)
cv2.destroyAllWindows()