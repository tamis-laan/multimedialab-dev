import glob
import sys
import pickle
import numpy 
import cv2 as opencv
import matplotlib.pyplot as plot
import re as regex

def extract_video_features(frame):
	shape=frame.shape
	num_pixels = shape[0]*shape[1]
	hist_feature_r = opencv.calcHist([frame[:,:,0]],[0],None,[255],[0,256])/num_pixels
	hist_feature_g = opencv.calcHist([frame[:,:,1]],[0],None,[255],[0,256])/num_pixels
	hist_feature_b = opencv.calcHist([frame[:,:,2]],[0],None,[255],[0,256])/num_pixels

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
		(success,frame) = capture.read()
		if not success:
			break
		features_new = f_features(frame)
		if len(features_old)>0 and len(features_new)>0:		
			data.append(numpy.linalg.norm(features_old-features_new))
		sys.stdout.write('\r' + str(index) + '/' + str(frame_count))
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

def sliding_window(window,signal):
	wl	= len(window)
	sl	= len(signal)
	diff	= numpy.zeros(sl-wl)
	minimum	= 9999
	frame	= -1
	if sl-wl<0:
		return ([],float("inf"),-1)
	for i in range(0,sl-wl):
		diff[i] = numpy.linalg.norm(window-signal[i:(i+wl)])
		if diff[i]<minimum:
			minimum	= diff[i]
			frame	= i
	return (diff,minimum,frame)

def compare(clip,database):
	print("[*] Comparing clip to database")
	match 	= 'Error'
	minimum	= 9999
	frame	= -1
	for video_name in database:
		print("  - " + video_name)
		(result,loop_minimum,loop_frame) = sliding_window(clip,database[video_name])
		plot.plot(range(0,len(result)),result,label="compare(clip," + video_name + ")")
		plot.legend()
		if loop_minimum<minimum:
			minimum	= loop_minimum
			frame	= loop_frame
			match	= video_name 
	print("[*] Identified video: " + match + "@frame:"+str(frame))
	print("[*] Plotting Results" )
	plot.show()

