import numpy as np

def iou(boxA, boxB):
# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
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

gt=[]
tctr=[]
outrack=[]
ou = 0
mo = 0
for i in os.listdir(os.getcwd()+'/MOTRealGroundTruth17'):
	if i[-3:] == 'txt':
			with open(os.getcwd()+'/MOTRealGroundTruth17/'+i) as f:
					gt=f.readlines()
			gt = [x.split(',') for x in gt]

			with open(os.getcwd()+'/ByteTrack17/'+i) as f:
					tctr=f.readlines()
			tctr = [x.split(',') for x in tctr]

			with open(os.getcwd()+'/OUTrack17/'+i) as f:
					outrack=f.readlines()
			outrack = [x.split(',') for x in outrack]

			gt = pd.DataFrame(gt)
			tctr = pd.DataFrame(tctr)
			outrack = pd.DataFrame(outrack)
			#if i[-7:] == 'DPM.txt':
			#			gt.columns = ['frame','id','x','y','w','h','score','primo','secondo','terzo']
			#else:
			gt.columns = ['frame','id','x','y','w','h','score','primo','secondo','terzo']            
			tctr.columns = ['frame','id','x','y','w','h','score','primo','secondo','terzo']
			outrack.columns = ['frame','id','x','y','w','h','primo','secondo','score']



			with open(os.getcwd()+'/OUTrack_ByteTrack_GroundTruth17/LABEL_GRAPH_CLASSIFICATION_'+i,'w') as f:
					for j in gt['frame'].unique(): #if all 3 have the frame, we consider them, else not
							print(j)                    
							try:
									gt_x = [float(x) for x in gt.loc[gt['frame']==j]['x'].reset_index()['x']]						
									bt_x = [float(x) for x in tctr.loc[tctr['frame']==j]['x'].reset_index()['x']]
									ot_x = [float(x) for x in outrack.loc[outrack['frame']==j]['x'].reset_index()['x']]
									gt_y = [float(x) for x in gt.loc[gt['frame']==j]['y'].reset_index()['y']]						
									bt_y = [float(x) for x in tctr.loc[tctr['frame']==j]['y'].reset_index()['y']]
									ot_y = [float(x) for x in outrack.loc[outrack['frame']==j]['y'].reset_index()['y']]
									gt_w = [float(x) for x in gt.loc[gt['frame']==j]['w'].reset_index()['w']]						
									bt_w = [float(x) for x in tctr.loc[tctr['frame']==j]['w'].reset_index()['w']]
									ot_w = [float(x) for x in outrack.loc[outrack['frame']==j]['w'].reset_index()['w']]
									gt_h = [float(x) for x in gt.loc[gt['frame']==j]['h'].reset_index()['h']]						
									bt_h = [float(x) for x in tctr.loc[tctr['frame']==j]['h'].reset_index()['h']]
									ot_h = [float(x) for x in outrack.loc[outrack['frame']==j]['h'].reset_index()['h']]
									#zero padding as in SimGNN
									dim_1 = max(len(gt_x),len(bt_x))
									dim_2 = max(len(gt_x),len(ot_x))
									gt_bt = np.ones((dim_1,dim_1))
									gt_ot = np.ones((dim_2,dim_2))
									#iou matrices building
																		                 
									for k in range(0,len(gt_x)):
											for d in range(0,len(bt_x)):
													gt_bt[k][d] = 1-iou([float(gt_x[k]),float(gt_y[k]),float(gt_x[k])+float(gt_w[k]),float(gt_y[k])+float(gt_h[k])],[float(bt_x[d]),float(bt_y[d]),float(bt_x[d])+float(bt_w[d]),float(bt_y[d])+float(bt_h[d])])
											for q in range(0,len(ot_x)):
													gt_ot[k][q] = 1-iou([float(gt_x[k]),float(gt_y[k]),float(gt_x[k])+float(gt_w[k]),float(gt_y[k])+float(gt_h[k])],[float(ot_x[q]),float(ot_y[q]),float(ot_x[q])+float(ot_w[q]),float(ot_y[q])+float(ot_h[q])])
									#hungarian algorithm

									copy_gt_bt = gt_bt.copy()
									copy_gt_ot = gt_ot.copy()
									m = Munkres()
									indexes_gt_bt = m.compute(gt_bt)
									indexes_gt_ot = m.compute(gt_ot)
									total_gt_bt = 0
									total_gt_ot = 0
									                                 
									for l in range(0,len(gt_x)): #we go back to the groundtruth graph dimension
											                                    
											total_gt_bt += copy_gt_bt[indexes_gt_bt[l]]
											total_gt_ot += copy_gt_ot[indexes_gt_ot[l]]
									                                    
									if total_gt_bt >= total_gt_ot:
											#label is 1 (outrack for MOT17 training, else is 0, or bytetrack, for MOT20 training, if we do not reverse it will be a cheat)
											ou += 1
											f.write(str(j)+','+str(1)+'\n')
									else:
											#label is 0
											mo += 1
											f.write(str(j)+','+str(0)+'\n')       
									
							except Exception as e:
									print('ok')
print(ou, mo)                                    