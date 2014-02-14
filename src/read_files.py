import glob
import sys
import numpy as numpy
import cv2 as opencv

def extract_video_features(frame):
	shape=frame.shape
	num_pixels = shape[0]*shape[1]
	hist_feature_r = opencv.calcHist([frame[:,:,0]],[0],None,[255],[0,256])/num_pixels
	hist_feature_g = opencv.calcHist([frame[:,:,1]],[0],None,[255],[0,256])/num_pixels
	hist_feature_b = opencv.calcHist([frame[:,:,2]],[0],None,[255],[0,256])/num_pixels
	features = numpy.concatenate( (hist_feature_r, hist_feature_g, hist_feature_b) )
	return features

def process_video(file,f_features):
	data		= []
	index 		= 0
	capture		= opencv.VideoCapture(file)
	frame_count	= capture.get(opencv.cv.CV_CAP_PROP_FRAME_COUNT)	
	while(True):
		(ret,frame) = capture.read()
		if not ret:
        		break
		sys.stdout.write('\r' + str(index) + '/' + str(frame_count))
		feature = f_features(frame)
		data.append(feature)
		index += 1
	capture.release()
	print("\n")
	if len(data) is 0:
		print("[!] Error Reading Video")
	return data

def build_data_base():
	print("[*] Constructing database")
	for filename in glob.glob("../media/*.ogv"):
		print(" [-] Parsing file: " + filename[9:17])
		numpy.save("../database/" + filename[9:17] + ".npy",process_video(filename,extract_video_features))

process_video("../clips/clip01.ogv",extract_video_features)
