import sys
import numpy as numpy
import cv2 as opencv

def extract_video_features(frame):
	shape=frame.shape
	num_pixels = shape[0]*shape[1]
	hist_feature_r = opencv.calcHist([frame[:,:,0]],[0],None,[10],[0,256])/num_pixels
	hist_feature_g = opencv.calcHist([frame[:,:,1]],[0],None,[10],[0,256])/num_pixels
	hist_feature_b = opencv.calcHist([frame[:,:,2]],[0],None,[10],[0,256])/num_pixels
	features = numpy.concatenate( (hist_feature_r, hist_feature_g, hist_feature_b) )
	return features

def process_video(file,f_features):
	data		= []
	index 		= 0
	capture		= opencv.VideoCapture(file)
	print("[*] Extracting features from file: " + file)	
	while(True):
		(ret,frame) = capture.read()
		if not ret:
        		break
		sys.stdout.write('\r' + str(index))
		feature = f_features(frame)
		data.append(feature)
		index += 1
	capture.release()
	print("\n[*] Writing features to file: " + file + ".npy")
	numpy.save(file + ".npy",data)

process_video("../media/video_01.ogv",extract_video_features)
process_video("../media/video_02.ogv",extract_video_features)
process_video("../media/video_03.ogv",extract_video_features)
process_video("../media/video_04.ogv",extract_video_features)

#TODO: extract features from video clips
