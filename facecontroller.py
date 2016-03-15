#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def draw_circle(img, center):
    color = (0, 0, 255) #red color
    #cv2.circle(img, center, 5, color, 3)
    cv2.circle(img,center, 10, (0,0,255), -1)
    #print("tring to draw a circle at ", center)

def jump():
    print("jumping!")

if __name__ == '__main__':
    import sys, getopt
    print help_message
    width = 640
    height = 480
    middle_x = None
    middle_y = None
    middle = None
    left_x = None
    right_x = None
    top_y = None
    bottom_y = None
    center_point = None
    vis = None
    upper_threshold = int(0.4 * height)
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_frontalface_alt.xml")
    cascade = cv2.CascadeClassifier(cascade_fn)
    cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
    #cap = cv2.VideoCapture(video_src)
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
    #cam = cap

    while True:
        ret, img = cam.read()
        img = cv2.flip(img,1) # flip image horizontally
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        try:
            coordinates = rects[0]
        except:
            print("out of range")
        else:
            left_x = coordinates[0]
            right_x = coordinates[2]
            top_y = coordinates[1]
            bottom_y = coordinates[3]
            middle_x = int((right_x - left_x)/2 + left_x)
            middle_y = int((bottom_y - top_y)/2 + top_y)
            center_point = (middle_x, middle_y)
            print("center: ", center_point)
            if center_point[1] < upper_threshold:
                jump()
            else:
                draw_circle(vis, center_point)
        finally:
            draw_rects(vis, rects, (0, 255, 0))

        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()
