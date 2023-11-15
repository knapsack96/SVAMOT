import numpy as np
import collections
import numpy as np
import pickle
def iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    #print(interArea)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

from munkres import Munkres

import os
import pandas as pd


training = []
counter = 0

for i in os.listdir(os.getcwd() +'/OUTrack_ByteTrack_GroundTruth17/'):
        
        glob_id = 0
        
        #if i[0:27] == 'LABEL_GRAPH_CLASSIFICATION_':
        #if i == 'LABEL_GRAPH_CLASSIFICATION_07.txt':
        
        with open(os.getcwd() +'/ByteTrack17/'+i[27:]) as f:
                bytetrack=f.readlines()
        bytetrack = [x.split(',') for x in bytetrack]
        
        with open(os.getcwd()+'/OUTrack17/'+i[27:]) as f:
                outrack=f.readlines()
        outrack = [x.split(',') for x in outrack]
        
        with open(os.getcwd()+'/OUTrack_ByteTrack_GroundTruth17/'+i) as f:
                gt=f.readlines()
        gt = [x.split(',') for x in gt]
        
        bytetrack = pd.DataFrame(bytetrack)
        outrack = pd.DataFrame(outrack)                
        gt = pd.DataFrame(gt)
        
        bytetrack.columns = ['frame','id','x','y','w','h','score','primo','secondo','terzo']
        outrack.columns = ['frame','id','x','y','w','h','primo','secondo','score']                
        gt.columns = ['frame','label']
        ot_id_previous = []
        ot_x_previous = []
        ot_y_previous = []
        ot_w_previous = []
        ot_h_previous = []
        bt_id_previous = []
        bt_x_previous = []
        bt_y_previous = []
        bt_w_previous = []
        bt_h_previous = []
        
        ids_frames = outrack['frame'].unique()
        print(len(ids_frames))
        for j in range(0,len(ids_frames)):
                counter+=1
                s = ids_frames[j]
                #try:
                ## trasforma tutti i dataframe in liste di interi                                    
                #print('frame..................', j)
                
                #print(ot_id)                                        
                bt_s = [float(x) for x in bytetrack.loc[bytetrack['frame']==s]['score'].reset_index()['score']]
                #print(bt_x)                                        
                ot_s = [float(x) for x in outrack.loc[outrack['frame']==s]['score'].reset_index()['score']]
                #print(tracker)
                bt_id = [int(x) for x in bytetrack.loc[bytetrack['frame']==s]['id'].reset_index()['id']]
                #print(bt_id)
                ot_id = [int(x) for x in outrack.loc[outrack['frame']==s]['id'].reset_index()['id']]
                #print(ot_id)        
                
                bt_x = [float(x) for x in bytetrack.loc[bytetrack['frame']==s]['x'].reset_index()['x']]
                #print(bt_x)                                        
                ot_x = [float(x) for x in outrack.loc[outrack['frame']==s]['x'].reset_index()['x']]
                #print(ot_x)                                            
                bt_y = [float(x) for x in bytetrack.loc[bytetrack['frame']==s]['y'].reset_index()['y']]
                #print(bt_y)                                        
                ot_y = [float(x) for x in outrack.loc[outrack['frame']==s]['y'].reset_index()['y']]
                #print(ot_y)
                bt_w = [float(x) for x in bytetrack.loc[bytetrack['frame']==s]['w'].reset_index()['w']]
                #print(bt_w)                                        
                ot_w = [float(x) for x in outrack.loc[outrack['frame']==s]['w'].reset_index()['w']]
                #print(ot_w)
                bt_h = [float(x) for x in bytetrack.loc[bytetrack['frame']==s]['h'].reset_index()['h']]
                #print(bt_h)                                        
                ot_h = [float(x) for x in outrack.loc[outrack['frame']==s]['h'].reset_index()['h']]
                
                gt_l = [int(x) for x in gt.loc[gt['frame']==s]['label'].reset_index()['label']]
        
                #print(np.mean(bt_s), np.mean(ot_s), gt_l[0])
                a = 0
                b = 0
                g = 0
                features_bt=[]
                features_ot=[]
                if len(bt_s)==0 or  len(bt_id)==0 or  len(bt_x)==0 or  len(bt_y)==0 or  len(bt_w)==0 or  len(bt_h)==0:
                    features_bt=[0,0,0,0,0,0]
                if len(ot_s)==0 or len(ot_id)==0 or len(ot_x)==0 or len(ot_y)==0 or len(ot_w)==0 or len(ot_h)==0:
                    features_ot=[0,0,0,0,0,0]
                if len(bt_s)!=0 and  len(bt_id)!=0 and  len(bt_x)!=0 and  len(bt_y)!=0 and  len(bt_w)!=0 and  len(bt_h)!=0:
                    features_bt=[np.mean(bt_s), len(bt_id), np.mean(bt_x), np.mean(bt_y), np.mean(bt_w), np.mean(bt_h)]
                if len(ot_s)!=0 and  len(ot_id)!=0 and  len(ot_x)!=0 and  len(ot_y)!=0 and  len(ot_w)!=0 and  len(ot_h)!=0:
                    features_ot=[np.mean(ot_s), len(ot_id), np.mean(ot_x), np.mean(ot_y), np.mean(ot_w), np.mean(ot_h)]
                if len(gt_l)!=0:                    
                    features = [s]+features_bt+features_ot+[gt_l[0]]
                    #è necessario l'id
                    training.append(features)#, c])
print(counter)

with open("outrackerbytetrack_data17.pkl", "wb") as f: 
    training = pickle.dump(training, f)
