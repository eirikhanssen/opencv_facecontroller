# OpenCV Facecontroller
OpenCV Facecontroller is a python script using the OpenCV library to provide a 
simple game controller relying on webcam and face detection.

It uses horizontal and vertical postion of the center point of the detected face to control properties such as game speed and jumping.
Proximity of the face can also be detected by looking at the size of the rectangle identified in the webcam image stream.

The idea is that this can controll a very basic sidescrolling game, only by using the webcam and moving the head.

## Install
- Download and install python 2
- Download and install OpenCV 2.4.12
- Put facecontroller.py in the right folder

### Some OS specific install instructions
Install on linux: http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html
Install on windows: http://docs.opencv.org/2.4/doc/tutorials/introduction/windows_install/windows_install.html

## facecontroller.py
After downloading and unpacking the opencv-2.4.12 package from opencv.org, facecontroller.py should be 
placed in the folder:
opencv-2.4.12/samples/python2

facecontroller.py is a fork of opencv-2.4.12/samples/python2/facedetect.py

It requires some other files in the opencv-2.4.12 package to operate:
- opencv-2.4.12/samples/python2/video.py - get videostream from webcam
- opencv-2.4.12/samples/python2/common.py
- opencv-2.4.12/data/haarcascades/haarcascade_frontalface_alt.xml - used in face detection
