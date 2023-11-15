#example
import pickle
with open("svm0025bytetrackouttrack20.pkl","rb") as f:
    res = pickle.load(f)
#this code can be repeated for each sequence of test of a dataset
with open("SVaMOT20/MOT20-04.txt","w") as f:
#here you set the limits of all the frames belonging to the written sequence. Be careful, sometimes some frames are excluded from results, so check before.
    for k in ris[0:2080]: 
        f.write(str(k[0])+','+str(k[1])+'\n')
