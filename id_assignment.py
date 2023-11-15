
import numpy as np
import collections
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

for i in os.listdir(os.getcwd() +'/GroundTruth20/'):
        print(i)
        glob_id = 0
        #if i[0:27] == 'LABEL_GRAPH_CLASSIFICATION_':
        #if i == 'LABEL_GRAPH_CLASSIFICATION_07.txt':
        
        with open(os.getcwd() +'/ByteTrack20/'+i[27:]) as f:
                bytetrack=f.readlines()
        bytetrack = [x.split(',') for x in bytetrack]

        with open(os.getcwd()+'/OUTrack20/'+i[27:]) as f:
                outrack=f.readlines()
        outrack = [x.split(',') for x in outrack]
        
        with open(os.getcwd() +'/SVaMOT20/MOT20-'+i[27:]) as f:
                results=f.readlines()
        results = [x.split(',') for x in results]


        bytetrack = pd.DataFrame(bytetrack)
        outrack = pd.DataFrame(outrack)                
        results = pd.DataFrame(results)

        bytetrack.columns = ['frame','id','x','y','w','h','score']
        outrack.columns = ['frame','id','x','y','w','h','score']                
        results.columns = ['frame','label']
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
        
        bt_remap = {}                
        ot_remap = {}
        with open(os.getcwd() +'/SVaMOT20_dacaricare/MOT20-'+i[27:],'w') as f:
                tracker = -1

                ids_frames = results['frame'].unique()

                for j in range(0,len(ids_frames)):
                        s = ids_frames[j]
                        print(glob_id)
                        #try:
                        ## trasforma tutti i dataframe in liste di interi                                    
                        print('frame..................', j, s)
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
                        #print(ot_h)                                        
                        rs_l = [int(x) for x in results.loc[results['frame']==s]['label'].reset_index()['label']]
                        b = int(s)
                        #print(rs_l[0][0], s, ids_frames[j], j)
                        print("bt_remap:", bt_remap)
                        print("ot_remap:", ot_remap)
                        print("ot_previous_id:", ot_id_previous)
                        print("bt_previous_id:", bt_id_previous)
                        if b == int(ids_frames[0]): #primo frame
                                
                                tracker = rs_l[0]

                                if tracker == 0: #bytetrack
                                        for v in range(0,len(bt_id)):
                                                f.write(str(s)+','+str(bt_id[v])+','+str(bt_x[v])+','+str(bt_y[v])+','+str(bt_w[v])+','+str(bt_h[v])+','+'-1,-1,-1,-1\n')
                                                                                #frame previous
                                        bt_id_previous = bt_id
                                        bt_x_previous = bt_x
                                        bt_y_previous = bt_y
                                        bt_w_previous = bt_w
                                        bt_h_previous = bt_h
#                                                        bt_remap = {}
                                        for c in bt_id_previous:
                                            bt_remap[c] = c
                                        glob_id = max(bt_id_previous)+1
                                else: #outrack
                                        for v in range(0,len(ot_id)):
                                                print(ot_id[v])
                                                f.write(str(s)+','+str(ot_id[v])+','+str(ot_x[v])+','+str(ot_y[v])+','+str(ot_w[v])+','+str(ot_h[v])+','+'-1,-1,-1,-1\n')
                                                                                #frame previous
                                        ot_id_previous = ot_id
                                        print("ot_id_previous:",ot_id_previous)
                                        ot_x_previous = ot_x
                                        ot_y_previous = ot_y
                                        ot_w_previous = ot_w
                                        ot_h_previous = ot_h
#                                                        ot_remap = {}
                                        for c in ot_id_previous:
                                            ot_remap[c] = c
                                        print('prima')
                                        glob_id = max(ot_id_previous)+1
                                        print('dopo')
                        if b > int(ids_frames[0]): #dopo il primo frame
                                print(tracker,rs_l[0],'prima')
                                if tracker != rs_l[0]: #switch dell'algoritmo
                                        
                                        if tracker == 0:    #before bytetrack, now is outrack    
                                                print('byte to out')
                                                dim_1 = max(len(ot_x),len(bt_x_previous))
                                                
                                                ot_bt = np.ones((dim_1,dim_1))
                                                
                                                #print(gt_bt, gt_ot)

                                                #iou matrices building
                                                for k in range(0,len(ot_x)):
                                                        for d in range(0,len(bt_x_previous)):
                                                                #print([float(gt_x[k]),float(gt_y[k]),float(gt_x[k])+float(gt_w[k]),float(gt_y[k])+float(gt_h[k])],[float(bt_x[d]),float(bt_y[d]),float(bt_x[d])+float(bt_w[d]),float(bt_y[d])+float(bt_h[d])])

                                                                ot_bt[k][d] = 1-iou([float(ot_x[k]),float(ot_y[k]),float(ot_x[k])+float(ot_w[k]),float(ot_y[k])+float(ot_h[k])],[float(bt_x_previous[d]),float(bt_y_previous[d]),float(bt_x_previous[d])+float(bt_w_previous[d]),float(bt_y_previous[d])+float(bt_h_previous[d])])

                                                copy_ot_bt = ot_bt.copy()
                                                 
                                                #hungarian algorithm, in place (so we did a copy to indicize on the original)
                                                m = Munkres()
                                                indexes_ot_bt = m.compute(ot_bt)
                                                ot_id_previous = []
                                                ot_x_previous = []
                                                ot_y_previous = []
                                                ot_w_previous = []
                                                ot_h_previous = []
                                                
                                                for z in range(0,len(ot_id)):
                                                            if ot_bt[indexes_ot_bt[z][0]][indexes_ot_bt[z][1]] < 1 and indexes_ot_bt[z][1] <= len(bt_id_previous) - 1:
                                                                    f.write(str(s)+','+str(bt_id_previous[indexes_ot_bt[z][1]])+','+str(ot_x[z])+','+str(ot_y[z])+','+str(ot_w[z])+','+str(ot_h[z])+','+'-1,-1,-1,-1\n')
                                                                    keys = ot_remap.keys()
                                                                    keys_list = []
                                                                    for key in keys:
                                                                        keys_list.append(key)
                                                                    for key in keys_list:
                                                                        if ot_remap[key] == bt_id_previous[indexes_ot_bt[z][1]]:
                                                                            ot_remap.pop(key)
                                                                                # ot_remap[ot_id[indexes_ot_bt[z][0]]] = bt_id_previous[indexes_ot_bt[z][1]]
                                                                                # ot_id_previous.append(bt_id_previous[indexes_ot_bt[z][1]])
                                                                    ot_remap[ot_id[indexes_ot_bt[z][0]]] = bt_id_previous[indexes_ot_bt[z][1]]
                                                                    ot_id_previous.append(bt_id_previous[indexes_ot_bt[z][1]])
                                                            else:
                                                                    f.write(str(s)+','+str(glob_id)+','+str(ot_x[z])+','+str(ot_y[z])+','+str(ot_w[z])+','+str(ot_h[z])+','+'-1,-1,-1,-1\n')
                                                                #     for k, v in ot_remap.items():
                                                                #         if v == glob_id:

                                                                #                 ot_remap.pop(k) 
                                                                    ot_remap[ot_id[indexes_ot_bt[z][0]]] = glob_id
                                                                    ot_id_previous.append(glob_id)
                                                                    glob_id += 1
                                                            ot_x_previous.append(ot_x[z])
                                                            ot_y_previous.append(ot_y[z])
                                                            ot_w_previous.append(ot_w[z])
                                                            ot_h_previous.append(ot_h[z])            

                                                print('occorrenze dopo:',collections.Counter(ot_remap.values()))
                                        else: #before outrack, now is bytetrack
                                                print('out to byte')
                                                dim_1 = max(len(bt_x),len(ot_x_previous))
                                                
                                                bt_ot = np.ones((dim_1,dim_1))
                                                
                                                #print(gt_bt, gt_ot)

                                                #iou matrices building
                                                for k in range(0,len(bt_x)):
                                                        for d in range(0,len(ot_x_previous)):
                                                                #print([float(gt_x[k]),float(gt_y[k]),float(gt_x[k])+float(gt_w[k]),float(gt_y[k])+float(gt_h[k])],[float(bt_x[d]),float(bt_y[d]),float(bt_x[d])+float(bt_w[d]),float(bt_y[d])+float(bt_h[d])])

                                                                bt_ot[k][d] = 1-iou([float(bt_x[k]),float(bt_y[k]),float(bt_x[k])+float(bt_w[k]),float(bt_y[k])+float(bt_h[k])],[float(ot_x_previous[d]),float(ot_y_previous[d]),float(ot_x_previous[d])+float(ot_w_previous[d]),float(ot_y_previous[d])+float(ot_h_previous[d])])

                                                copy_bt_ot = bt_ot.copy()
                                                 
                                                #hungarian algorithm, in place (so we did a copy to indicize on the original)
                                                m = Munkres()
                                                indexes_bt_ot = m.compute(bt_ot)
                                                bt_id_previous = []
                                                bt_x_previous = []
                                                bt_y_previous = []
                                                bt_w_previous = []
                                                bt_h_previous = []
                                                
                                                for z in range(0,len(bt_id)):
                                                            if bt_ot[indexes_bt_ot[z][0]][indexes_bt_ot[z][1]] < 1 and indexes_bt_ot[z][1] <= len(ot_id_previous) - 1:
                                                                    f.write(str(s)+','+str(ot_id_previous[indexes_bt_ot[z][1]])+','+str(bt_x[z])+','+str(bt_y[z])+','+str(bt_w[z])+','+str(bt_h[z])+','+'-1,-1,-1,-1\n')
                                                                    keys = bt_remap.keys()
                                                                    keys_list = []
                                                                    for key in keys:
                                                                        keys_list.append(key)
                                                                    for key in keys_list:
                                                                        if bt_remap[key] == ot_id_previous[indexes_bt_ot[z][1]]:
                                                                            bt_remap.pop(key)
                                                                    bt_remap[bt_id[indexes_bt_ot[z][0]]] = ot_id_previous[indexes_bt_ot[z][1]]
                                                                    bt_id_previous.append(ot_id_previous[indexes_bt_ot[z][1]])
                                                            else:
                                                                    f.write(str(s)+','+str(glob_id)+','+str(bt_x[z])+','+str(bt_y[z])+','+str(bt_w[z])+','+str(bt_h[z])+','+'-1,-1,-1,-1\n')
                                                                #     for k, v in bt_remap.items():
                                                                #         if v == glob_id:
                                                                #                 bt_remap.pop(k)
                                                                    
                                                                    bt_remap[bt_id[indexes_bt_ot[z][0]]] = glob_id
                                                                    bt_id_previous.append(glob_id)
                                                                    glob_id += 1
                                                            bt_x_previous.append(bt_x[z])
                                                            bt_y_previous.append(bt_y[z])
                                                            bt_w_previous.append(bt_w[z])
                                                            bt_h_previous.append(bt_h[z])            
                                else: #stesso algoritmo, id matching is verified by remapping on old ids, and increasing +1 if there is no match found                                                                        
                                                                               
                                        if tracker == 0:    #before bytetrack, now is bytetrack
                                                print('byte to byte')
                                                bt_id_previous = []
                                                bt_x_previous = []
                                                bt_y_previous = []
                                                bt_w_previous = []
                                                bt_h_previous = []

                                                for z in range(0,len(bt_id)):
                                                            if bt_id[z] in bt_remap:
                                                                    f.write(str(s)+','+str(bt_remap[bt_id[z]])+','+str(bt_x[z])+','+str(bt_y[z])+','+str(bt_w[z])+','+str(bt_h[z])+','+'-1,-1,-1,-1\n')
                                                                    bt_id_previous.append(bt_remap[bt_id[z]])
                                                            else:
                                                                    f.write(str(s)+','+str(glob_id)+','+str(bt_x[z])+','+str(bt_y[z])+','+str(bt_w[z])+','+str(bt_h[z])+','+'-1,-1,-1,-1\n')
                                                                #     for k, v in bt_remap.items():
                                                                #         if v == glob_id:

                                                                #                 bt_remap.pop(k)
                                                                    bt_remap[bt_id[z]] = glob_id
                                                                    bt_id_previous.append(glob_id)
                                                                    glob_id += 1
                                                            bt_x_previous.append(bt_x[z])
                                                            bt_y_previous.append(bt_y[z])
                                                            bt_w_previous.append(bt_w[z])
                                                            bt_h_previous.append(bt_h[z])            

                                                
                                        else: #before outrack, now is outrack
                                                print('out to out')
                                                ot_id_previous = []
                                                ot_x_previous = []
                                                ot_y_previous = []
                                                ot_w_previous = []
                                                ot_h_previous = []
                                                
                                                for z in range(0,len(ot_id)):
                                                            if ot_id[z] in ot_remap:
#                                                                                    print('si')                                                                                
                                                                    f.write(str(s)+','+str(ot_remap[ot_id[z]])+','+str(ot_x[z])+','+str(ot_y[z])+','+str(ot_w[z])+','+str(ot_h[z])+','+'-1,-1,-1,-1\n')
                                                                    ot_id_previous.append(ot_remap[ot_id[z]])

                                                            else:
#                                                                                    print('no')                                                                                
                                                                    f.write(str(s)+','+str(glob_id)+','+str(ot_x[z])+','+str(ot_y[z])+','+str(ot_w[z])+','+str(ot_h[z])+','+'-1,-1,-1,-1\n')
                                                                #     for k, v in ot_remap.items():
                                                                #         if v == glob_id:

                                                                #                 ot_remap.pop(k)
                                                                    ot_remap[ot_id[z]] = glob_id
                                                                    ot_id_previous.append(glob_id)
                                                                    glob_id += 1
                                                            ot_x_previous.append(ot_x[z])
                                                            ot_y_previous.append(ot_y[z])
                                                            ot_w_previous.append(ot_w[z])
                                                            ot_h_previous.append(ot_h[z])
                                tracker = rs_l[0]
                                print(tracker,rs_l[0])
                        #except Exception as e:
                        #    print(e)
                                                                        
