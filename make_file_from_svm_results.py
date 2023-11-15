#example
import pickle
with open("svm0025bytetrackouttrack20.pkl","rb") as f:
    res = pickle.load(f)
with open("MOT20-04","w") as f:
#here you set the limits of all the frames belonging to the written sequence. Be careful, sometimes some frames are excluded from results, so check before.
    for k in ris[0:2080]: 
        f.write(str(k[0])+','+str(k[1])+'\n')
