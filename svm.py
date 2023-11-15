from sklearn import svm
from sklearn.svm import LinearSVC, SVC
import pickle
import numpy as np

#with open("moterpermatrack17train_data.pkl","rb") as f:
#    train = pickle.load(f)
#with open("moterpermatrack17_data.pkl","rb") as f:
#    test = pickle.load(f)
with open("outrackbytetrack_data17.pkl","rb") as f:
    train = pickle.load(f)
with open("outrackbytetrack_data20.pkl","rb") as f:
    test = pickle.load(f)

X = np.array([x[1:3]+x[5:7]+x[11:13] for x in train])


y = np.array([x[13] for x in train])

target = np.array([x[13] for x in test])

clf = svm.SVC(C=0.025, class_weight='balanced', kernel='linear', verbose=True) 

clf.fit(X, y)

sample = np.array([x[1:3]+x[5:7]+x[11:13] for x in test])

label = clf.predict(sample)
ith open('svm0025bytetrackouttrack20.pkl','wb') as f:
    pickle.dump([h for h in zip([x[0] for x in test],label)], f)

#with open('svmoterpermatrack17.pkl','wb') as f:
#    pickle.dump([h for h in zip([x[0] for x in test],label)], f)

#print(sum(label==target)*100/len(target))                                       
