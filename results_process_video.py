import cv2
import os
from random import randrange

frames =[]
# for i in os.listdir('MOT20/test/MOT20-04/img1'):
#root = '/media/wprumm01/DISK_PhD_WP/Documents/Multi_object_tracking_CVPR/GNN_TrackPrediction/submit/img1/'
for i in os.listdir(r'C:\Users\vince\OneDrive\Desktop\MOT\DaModificare\corrections\MOT17\MOT17\test\MOT17-01-DPM\img1'):
# reading the input
#cap = cv2.VideoCapture("input.mp4")
  if i[0:2]!='._' :
    frames.append(i)
frames = sorted(frames)
print(frames[0])

img = cv2.imread(r'C:/Users/vince/OneDrive/Desktop/MOT/DaModificare/corrections/MOT17/MOT17/test/MOT17-01-DPM/img1/'+frames[0])

h,w,c = img.shape
output = cv2.VideoWriter(
        "MOT17-01-DPM.mp4", cv2.VideoWriter_fourcc(*'MPEG'), 
      30, (w, h))
bb = []
# with open(os.getcwd()+'/ReadyToVideo20/MOT20-04.txt') as f:
with open(r'C:/Users/vince/OneDrive/Desktop/MOT/EsperimentiSVaMOT/moterpermatrack_dacaricare/MOT17-01-DPM.txt') as f:
    bb = f.readlines()
final_bb = []
for j in bb:
    final_bb.append(j.split(','))

old_frame = final_bb[0][0]
# img = cv2.imread('MOT20/test/MOT20-04/img1/'+frames[0])
img = cv2.imread(r'C:/Users/vince/OneDrive/Desktop/MOT/DaModificare/corrections/MOT17/MOT17/test/MOT17-01-DPM/img1/'+frames[0])
# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (50, 50)
  
# fontScale
fontScale = 1
  
# Line thickness of 2 px
thickness = 4

color = {}

for i in final_bb:
    if old_frame != i[0]: #frame by frame
        #cv2.imshow("output", img)
        #cv2.waitKey()
        print(i)
        output.write(img)

        img = cv2.imread(r'C:/Users/vince/OneDrive/Desktop/MOT/DaModificare/corrections/MOT17/MOT17/test/MOT17-01-DPM/img1/'+frames[int(i[0])-1])
        old_frame = i[0]
       # adding filled rectangle on each frame
    #try:
    print(i)
    if int(i[1]) not in color.keys(): #there is such id in list
        color[int(i[1])] = (randrange(256),randrange(256),randrange(256)) #very likely it will not repeat the same value twice
    cv2.rectangle(img, (int(float(i[2])), int(float(i[3]))), (int(float(i[2]))+int(float(i[4])), int(float(i[3]))+int(float(i[5]))), color[int(float(i[1]))])
    # cv2.putText(img, i[1], org, font, fontScale, color[int(i[1])], thickness, cv2.LINE_AA)
    # cv2.addText(img, i[1], (int(float(i[2])), int(float(i[3]))))
    #except e:
#        print('')
            # writing the new frame in output
     
    

#cv2.destroyAllWindows()
output.release()


