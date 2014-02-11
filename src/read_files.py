#Set the python modules search path 
import sys
sys.path.append('../lib')

#Import libraries
import numpy as numpy
import matplotlib as plot
import sklearn as ml
import cv2 as opencv

#This method extracts the feature from the given frame
def extract_video_features(frame):
	#extract normalized histograms for each collor channel
	shape=frame.shape
	num_pixels = shape[0]*shape[1]
	hist_feature_r = opencv.calcHist([frame[:,:,0]],[0],None,[10],[0,256])/num_pixels
	hist_feature_g = opencv.calcHist([frame[:,:,1]],[0],None,[10],[0,256])/num_pixels
	hist_feature_b = opencv.calcHist([frame[:,:,2]],[0],None,[10],[0,256])/num_pixels
	#Concatenate the histograms into one feature
	features = numpy.concatenate( (hist_feature_r, hist_feature_g, hist_feature_b) )
	return features

#This function reads in a video file and builds an array of features.
def process_video(file,f_features):
	capture	= opencv.VideoCapture(file)
	capture.set(3,80)
	capture.set(4,60)
	data		= []
	frame_count 	= capture.get(7)
	index 		= 0
	print("[*] Extracting features from file: " + file)	
	while(True):
		sys.stdout.write('\r' + str(index))
		(ret,frame) = capture.read()
		if not ret:
        		break
		feature = f_features(frame)
		data.append(feature)
		index = index+1
	capture.release()
	print("\n[*] Writing features to file: " + file + ".npy")
	numpy.save(file + ".npy",data)

#Extract the features from all four video files
process_video("../media/video_01.ogv",extract_video_features)
process_video("../media/video_02.ogv",extract_video_features)
process_video("../media/video_03.ogv",extract_video_features)
process_video("../media/video_04.ogv",extract_video_features)

#Extract features from video clips (TODO)
