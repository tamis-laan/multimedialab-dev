import glob
import sys
import numpy as numpy
import cv2 as opencv
import pickle
import re as regex

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

def build_database():
	print("[*] Constructing database")
	database = {}
	for path in glob.glob("../media/*.ogv"):
		print(path)
		filename = ( regex.findall("/([^/]+)\.ogv",path) )[0]
		print(" [-] Parsing path: " + path)
		database[filename] = process_video(path,extract_video_features)	
	print("[*] Saving database to disk")	
	database_file = open('database.db','wb')
	pickle.dump(database,database_file)
	database_file.close()

def load_database():
	print("[*] Loading database from disk")
	database_file = open('database.db', 'rb')
	database = pickle.load(database_file)
	database_file.close()
	print("[*] Done")
	return database


build_database()
database = load_database()
