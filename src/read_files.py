import glob
import sys
import numpy as numpy
import cv2 as opencv
import matplotlib.pyplot as plot

def extract_video_features(frame):
	shape=frame.shape
	num_pixels = shape[0]*shape[1]
	hist_feature_r = opencv.calcHist([frame[:,:,0]],[0],None,[256],[0,256])/num_pixels
	hist_feature_g = opencv.calcHist([frame[:,:,1]],[0],None,[256],[0,256])/num_pixels
	hist_feature_b = opencv.calcHist([frame[:,:,2]],[0],None,[256],[0,256])/num_pixels
	features = numpy.concatenate( (hist_feature_r, hist_feature_g, hist_feature_b) )
	return features

def process_video(file,f_features):
	data			= []
	index			= 0
	capture			= opencv.VideoCapture(file)
	frame_count		= capture.get(opencv.cv.CV_CAP_PROP_FRAME_COUNT)
	features_old		= []
	features_new		= []
	while(True):
		features_old = features_new
		(ret,frame) = capture.read()
		if not ret:
			break
		sys.stdout.write('\r' + str(index) + '/' + str(frame_count))
		features_new = f_features(frame)
		if len(features_old)>0 and len(features_new)>0:		
			data.append(numpy.linalg.norm(features_old-features_new))
		index += 1
	capture.release()
	print("\n")
	if not data:
		print("[!] Error Reading Video")
	return numpy.asarray(data)
		
def build_data_base():
	print("[*] Constructing database")
	for filename in glob.glob("../media/*.ogv"):
		print(" [-] Parsing file: " + filename[9:17])
		numpy.save("../database/" + filename[9:17] + ".npy",process_video(filename,extract_video_features))



