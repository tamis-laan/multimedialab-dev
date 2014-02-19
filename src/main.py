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

def sliding_window(window,signal):
	wl	= len(window)
	sl	= len(signal)
	out	= numpy.zeros(sl-wl)
	m	= 9999
	mi	= -1
	if sl-wl<0:
		return ([],float("inf"),-1)
	for i in range(0,sl-wl):
		out[i] = numpy.linalg.norm(window-signal[i:(i+wl)])
		if out[i]<m:
			m  = out[i]
			mi = i
	return (out,m,mi)

def sliding_window_example():
	database = load_database()
	vid  = database["video_01"]
	clip = vid[100:2000]
	(corr,conv) = sliding_window(clip,vid)
	my = sliding_window(clip,vid)
	plot.plot(range(0,len(vid)),vid,'-b')
	plot.plot(range(100,100+len(clip)),clip,'-r')
	plot.plot(range(0,len(my)),my,'-g')
	plot.show()

def clip_example():
	database = load_database()
	vid  = database["video_01"]
	clip = read_files.process_video("../clips/clip_01.mp4",read_files.extract_video_features)
	(corr,conv) = sliding_window(clip,vid)
	(my,mi) = sliding_window(clip,vid)
	plot.plot(range(0,len(vid)),vid,'-b')
	plot.plot(range(mi,mi+len(clip)),clip,'-r')
	plot.plot(range(0,len(my)),my,'-g')
	plot.show()

def compare_to_database(clip,database):
	print("[*] Comparing clip to database")
	match 	= 'Error'
	at 	= []
	cm	= 9999
	cmi	= -1
	cv	= ""
	for video_name in database:
		print("  - " + video_name)
		(result,m,mi) = sliding_window(clip,database[video_name])
		plot.plot(range(0,len(result)),result,label=video_name)
		plot.legend()
		if m<cm:
			cm  = m
			cmi = mi
			cv  = video_name 
	print("[!] Done Comparing, identified video: " + cv + "@"+str(cmi))
	print("[*] Plotting Results" )
	plot.show()

#read_files.build_data_base()
database = load_database()
clip = read_files.process_video("../clips/clip_01.mp4",read_files.extract_video_features)
compare_to_database(clip,database)
