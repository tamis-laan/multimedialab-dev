import glob
import numpy as numpy
import matplotlib.pyplot as plot
import sklearn as ml
import cv2 as opencv
import read_files

def load_database():
	print("[*] Loading database")
	database = {}
	for filename in glob.glob("../database/*.npy"):
		print("  - " + filename)
		database[filename[12:20]]=numpy.load(filename)
	print("[!] Done Loading")
	return database

def sliding_window(w,l):
	shape = w.shape
	awns = None
	for i in range(0,shape[1]):
		wi = numpy.transpose(w[:,i])
		wi = wi[0]
		li = numpy.transpose(l[:,i])
		li = li[0]
		conv = numpy.convolve(wi[::-1],li,'valid')
		if(awns is None):
			awns = [0]*len(conv)
		awns += conv
	return awns
	
def compare_to_database(clip,database):
	print("[*] Comparing clip to database")
	m 	= -99;
	match 	= 'Error'
	at 	= []
	for video_name in database:
		print("  - " + video_name)
		result = sliding_window(clip,database[video_name])
		if max(result)>m:
			m = max(result)
			match = video_name
			at = numpy.unravel_index(result.argmax(),result.shape)
		plot.plot(range(0,len(result)),result,label=video_name)
		plot.legend()
	print("[!] Done Comparing, identified video: " + match + "@"+str(at))
	print("[*] Plotting Results" )
	plot.show()

database = load_database()
clip = database["video_03"]
read_files.
compare_to_database(clip[1000:1500],database)
