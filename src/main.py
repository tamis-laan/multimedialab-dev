import numpy 
import matplotlib.pyplot as plot
import medialab

"""
This example extracts a clip of 5900 frames from video_01 and compares it to all the 10 videos in the database. 
It then plots the resulting comparison signals and prints the video and frame were the clip fits best.
"""
def example01():
	database = medialab.load_database()
	clip = ( database["video_01"] )[100:6000]
	plot.plot(range(0,len(database["video_01"])),database["video_01"],'-k',label="video_01")
	plot.plot(range(100,100+len(clip)),clip,'-y',label="clip")
	medialab.compare(clip,database)

"""
This example extracts a clip of 400 frames from video_01 and compares it to all the 10 videos in the database. 
It then plots the resulting comparison signals and prints the video and frame were the clip fits best.
"""
def example02():
	database = medialab.load_database()
	clip = ( database["video_01"] )[100:500]
	plot.plot(range(0,len(database["video_01"])),database["video_01"],'-k',label="video_01")
	plot.plot(range(100,100+len(clip)),clip,'-y',label="clip")
	medialab.compare(clip,database)

"""
This example compares clip_01.mp4 which is an video recording of video_01 and compares it to all the 10 videos
in the database. It then plots the resulting comparison signals and prints the video and frame were the clip fits best.
"""
def example03():
	database = medialab.load_database()
	clip = medialab.process_video("../clips/clip_01.mp4",medialab.extract_video_features)
	medialab.compare(clip,database)

#MAIN: build database and run examples	
medialab.build_database()
example01()
example02()
example03()
