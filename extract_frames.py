
import cv2
import random

font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (100, 100)
  
# fontScale
fontScale = 4
  
# Line thickness of 2 px
thickness = 20
vidcap = cv2.VideoCapture("MOT17-01-DPM.mp4")
# get total number of frames
totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
randomFrameNumber=random.randint(0, totalFrames)
# set frame position
vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber)
success, image = vidcap.read()
cv2.putText(image, 'a', org, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
if success:
    cv2.imwrite("MOT17-01-DPM-01.jpg", image)
vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber+100)
success, image = vidcap.read()
cv2.putText(image, 'b', org, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
if success:
    cv2.imwrite("MOT17-01-DPM-02.jpg", image)