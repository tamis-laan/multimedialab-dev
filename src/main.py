import numpy 
import matplotlib.pyplot as plot
import medialab

def example01():
	database = medialab.load_database()
	clip = ( database["video_01"] )[100:6000]
	plot.plot(range(0,len(database["video_01"])),database["video_01"],'-k',label="video_01")
	plot.plot(range(100,100+len(clip)),clip,'-y',label="clip")
	medialab.compare(clip,database)

def example02():
	database = medialab.load_database()
	clip = ( database["video_01"] )[100:500]
	plot.plot(range(0,len(database["video_01"])),database["video_01"],'-k',label="video_01")
	plot.plot(range(100,100+len(clip)),clip,'-y',label="clip")
	medialab.compare(clip,database)

def example03():
	database = medialab.load_database()
	clip = medialab.process_video("../clips/clip_01.mp4",medialab.extract_video_features)
	medialab.compare(clip,database)

medialab.build_database()
example01()
example02()
example03()
