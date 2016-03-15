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

def draw_circle(img, center, color, ratio):
    circle_radius = int(ratio*ratio*ratio*100)
    if circle_radius < 5:
        circle_radius = 5
    cv2.circle(img,center, circle_radius, color, -1)
    #print("tring to draw a circle at ", center)

def jump():
    print("jumping!")
    draw_str(vis, (int(width/2)-50,int(height/2)), 'AIRBORNE!') # tell user is jumping


def draw_str(dst, (x, y), s):
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 2.0, (40, 40, 40), thickness = 8, lineType=cv2.CV_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 255), thickness = 4, lineType=cv2.CV_AA)

if __name__ == '__main__':
    import sys, getopt
    print help_message
    width = 640
    halfwidth = int(width/2)
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
    x_ratio = None
    proximity_ratio = 1 # height of tracked face rectangle / height of webcam image, initially defaults to 1
    speed_x_multiplier = None
    height_diff = None
    score = 0
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
            print("GAME PAUSED... (face is out of range)")
            speed_x_multiplier = 0
        else:
            left_x = coordinates[0]
            right_x = coordinates[2]
            top_y = coordinates[1]
            bottom_y = coordinates[3]
            middle_x = int((right_x - left_x)/2 + left_x)
            middle_y = int((bottom_y - top_y)/2 + top_y)
            center_point = (middle_x, middle_y)
            x_ratio = (center_point[0]-0.25*width)/halfwidth
            if x_ratio < 0:
                x_ratio = 0
            if x_ratio > 1:
                x_ratio = 1
                print("x-ratio: " + str(x_ratio))
            print("bottom and top y: " + str(bottom_y) + "," + str(top_y))
            height_diff = int(bottom_y-top_y)
            proximity_ratio = float(height_diff)/float(height)
            print("height ratio: " + str(proximity_ratio))
            speed_x_multiplier = 1.5*x_ratio + 0.5
            print("speed multiplier: " + str(speed_x_multiplier)) #0.5 to 2.0
            print(str("center: " + str(center_point)))
            if center_point[1] < upper_threshold:
                draw_circle(vis, center_point, (255,0,0), proximity_ratio)
                jump()
            else:
                draw_circle(vis, center_point, (0,0,255), proximity_ratio)
        finally:
            draw_rects(vis, rects, (0, 255, 0))
            draw_str(vis, (int(width/2)-50,int(height - height/6)), 'Speed: %.1f' % speed_x_multiplier)


        dt = clock() - t

        #draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        if speed_x_multiplier > 0:
            score = score + dt*2**(1+speed_x_multiplier*2.5)
        else :
            draw_str(vis, (int(width/2)-50,int(height/2)), 'PAUSED!')

        draw_str(vis, (20,50), 'Score: %.1f' % score)

        cv2.imshow('facedetect', vis)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()
