import glob
import sys
import pickle
import numpy 
import cv2 as opencv
import matplotlib.pyplot as plot
import re as regex
import math

"""
This function extracts features from a given frame. It extracts a normalized histogram for each of the collor channels
of the frame. The code for extracting a normalized histogram is also present below but commented out as for the moment
it is to slow. This code however could be incorperated to increase detection rate.
"""
def extract_video_features(frame):
	shape=frame.shape
	num_pixels = shape[0]*shape[1]
	hist_feature_r = opencv.calcHist([frame[:,:,0]],[0],None,[2],[0,255])/num_pixels
	hist_feature_g = opencv.calcHist([frame[:,:,1]],[0],None,[2],[0,255])/num_pixels
	hist_feature_b = opencv.calcHist([frame[:,:,2]],[0],None,[2],[0,255])/num_pixels

	#gray = opencv.cvtColor(frame,opencv.COLOR_BGR2GRAY)
	#sobelx = opencv.Sobel(gray,opencv.CV_64F,1,0,ksize=5)
	#sobely = opencv.Sobel(gray,opencv.CV_64F,0,1,ksize=5)
	#theta  = numpy.arctan2(sobelx,sobely)
	#(hist_theta,_) = numpy.histogram(theta,2,(-math.pi,math.pi),True)
	#print( numpy.concatenate( (hist_feature_r, hist_feature_g, hist_feature_b, hist_theta) ) )
	
	features = numpy.concatenate( (hist_feature_r, hist_feature_g, hist_feature_b) )
	
	return features

"""
This function processes a file by extracting features using the function f_features. The students may write their own
feature extraction function and use this command with their custom function. 
"""
def process_video(file,f_features):
	data			= []
	index			= 0
	capture			= opencv.VideoCapture(file)
	frame_count		= capture.get(opencv.cv.CV_CAP_PROP_FRAME_COUNT)
	features_old		= []
	features_new		= []
	#start extracting frames from video.
	while(True):
		features_old = features_new
		(success,frame) = capture.read()
		if not success:
			break
		features_new = f_features(frame)
		#compute the 2-norm as the signal between features of concequtive frames.
		if len(features_old)>0 and len(features_new)>0:		
			data.append(numpy.linalg.norm(features_old-features_new))
		sys.stdout.write('\r' + str(index) + '/' + str(frame_count))
		index += 1
	capture.release()
	print("\n")
	if not data:
		print("[!] Error Reading Video")
	return numpy.asarray(data)

"""
This function builds a database of feature signals that can then be processed later if needed. It does this by
processing all the media .ogv file in the folder /media/.
"""
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

"""
This function loads all the feature signals stored in a databse file.
"""
def load_database():
	print("[*] Loading database from disk")
	database_file = open('database.db', 'rb')
	database = pickle.load(database_file)
	database_file.close()
	print("[*] Done")
	return database

"""
This function implements a sliding window that can be used to compare a clip(window) and a video(signal) for each 
position of the window it will take the 2-norm of the diffrences between the window and the signal. The signal
returned indicates the quallity of the match.
"""
def sliding_window(window,signal):
	wl	= len(window)
	sl	= len(signal)
	if sl-wl<0:
		return ([],float("inf"),-1)

	diff	= numpy.zeros(sl-wl)
	minimum	= 9999
	frame	= -1
	for i in range(0,sl-wl):
		diff[i] = numpy.linalg.norm(window-signal[i:(i+wl)])
		if diff[i]<minimum:
			minimum	= diff[i]
			frame	= i
	return (diff,minimum,frame)

"""
This function compares a given clip to all the videos in a database. It then plots the results and prints the best 
matching video and the best matching frame position.
"""
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

