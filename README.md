# SVAMOT
Support Vector Machine Approach for Multi-Object Trackers Fusion Strategy (#1 on MOT17, MOT20 on both private and public detections, considering published works)

The files in this repo have different and consequent functionalities.

1) MOT17 and MOT20 groundtruth files are in folders starting with "MOTRealGroundTruth".
They are needed to make the specific groundtruth for training the SVM.

2) Test results of the trackers are in ByteTrack17, ByteTrack20, ImprAsso17, ImprAsso20, BrinqTraq_v217, BrinqTraqv220, MOTer17, OUTrack17, OUTrack20.zip (unzip it), Permatrack17, NvMOT_DS230517.

3) Training results are in the same folders but ending in "train".

4) The first operation is the specific groundtruth building through the file "label_maker.py". You should adjust the path in order to refer to the right folders (an example is already in the file). Be careful to the fields of every file, not every file has the same number of fields, so change it in the 3 lists if it raises an error.

5) Once specific groundtruth are built, some folders will be populated (in the repo these are BrinqTraq_v2_ImprAsso_GroundTruth17, BrinqTraq_v2_NvMOT_DS2305_GroundTruth17train, OUTrack_ByteTrack_groundtruth17, PermaTrack_MOTer_GroundTruth17train).

6) For training the SVM, you should transform the data in the 5) folders into pickle files. To do that, run make_features_for_svm.py adjusting the paths in the right way, and setting the name of the final pickle file in the right way. This file would create the training and test data, so: BrinqTraq_v2_ImprAsso_17_data.pkl, BrinqTraq_v2_ImprAsso_20_data.pkl, BrinqTraq_v2_NvMOT_DS2305_data_17.pkl, BrinqTraq_v2_NvMOT_DS2305_data17train.pkl, moterpermatrack17_data.pkl, moterpermatrack17train_data.pkl, outrackbytetrack_data17.pkl, outrackbytetrack_data20.pkl. Intuitively, the files ending in "train" are the training files, the others are the test files.

7) After the previous step you can now run a train/test phase. Run svm.py after modifying correctly the paths inside (the input data and the svm destination model path). In the file there are already two examples (one commented and one not). The parameters and features chosen for the experiments are in the paper.

8) Once the model has been saved, you can create the results file by using make_file_from_svm_results.py, setting up the paths in the right way.
   
