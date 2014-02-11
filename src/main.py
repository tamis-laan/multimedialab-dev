#Set the python modules search path 
import sys
sys.path.append('../lib')

#Import libraries
import numpy as numpy
import matplotlib.pyplot as plot
import sklearn as ml
import cv2 as opencv

video = numpy.load("../media/video_02.ogv.npy")
clip  = numpy.load("../media/video_02.ogv.npy")
print(video.shape)
plot.plot(range(0,len(video)),video[:,2 ], '-r', linewidth=1)
plot.plot(range(0,len(video)),video[:,12], '-g', linewidth=1)
plot.plot(range(0,len(video)),video[:,22], '-b', linewidth=1)


plot.show()
print(data)
