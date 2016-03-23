#!/usr/bin/env python2
import pygame
import os
import sys, getopt
from facecontroller import *
import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import draw_str
import common #clock

w = 800
h = 600
bigcloud_x = w
small_clouds_x = w
speed_big_cloud = 3
speed_small_clouds = 1
small_clouds_width = 704
big_cloud_width = 549
chicken_y_pos = h/2
_image_library = {}

width = 640
halfwidth = int(width/2)
height = 480
middle_x = None
middle_y = h/2
middle = None
left_x = width/2
right_x = None
top_y = None
bottom_y = None
center_point = (width/2,height/2)
vis = None
x_ratio = None
proximity_ratio = 1 # height of tracked face rectangle / height of webcam image, initially defaults to 1
speed_x_multiplier = 1
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
face_detected = False
face_not_detected_timer = None
game_paused = False
now = None
pause_threshold = 0.5

def textOnScreen(screen,message, x, y):
    font = pygame.font.SysFont("comicsansms", 42)
    text = font.render(message, True, (255, 255, 0))
    textrim = font.render(message, True, (255, 255, 255))
    textbg = font.render(message, True, (0, 0, 0))
    screen.blit(textbg, (x+2, y+2))
    screen.blit(textrim, (x-2, y-2))
    screen.blit(text, (x, y))

def draw_face_detect(surf, edge_left, edge_right,edge_top, edge_bottom):
    color = (128,255,128)
    thickness = 5
    edge_left = edge_left * (w/width)
    edge_right = edge_right * (w/width)
    edge_top = edge_top * (h/height)
    edge_bottom = edge_bottom * (h/height)
    pygame.draw.lines(surf, color, False, [(edge_left, edge_top), (edge_right, edge_top), (edge_right, edge_bottom), (edge_left, edge_bottom), (edge_left, edge_top)], thickness)

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

pygame.init()
screen = pygame.display.set_mode((w,h), pygame.SRCALPHA)
done = False
clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # facecontroller code begin
    ret, img = cam.read()
    img = cv2.flip(img,1) # flip image horizontally
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    t = common.clock()
    rects = detect(gray, cascade)
    #vis = img.copy()
    try:
        coordinates = rects[0]
    except:
        #print("GAME PAUSED... (face is out of range)")
        face_detected = False

        if face_not_detected_timer == None:
            face_not_detected_timer = common.clock()

        now = common.clock()

        if now - face_not_detected_timer > pause_threshold:
            game_paused = True

        print("now: ", now, "face_not_detected_timer: ", face_not_detected_timer)
        speed_x_multiplier = speed_x_multiplier
    else:
        game_paused = False
        face_not_detected_timer = None
        face_detected = True
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
            #draw_circle(vis, center_point, (255,0,0), proximity_ratio)
            #jump()
            print("flying high")
        else:
            #draw_circle(vis, center_point, (0,0,255), proximity_ratio)
            print("not drawing circle..")
    finally:
        #draw_rects(vis, rects, (0, 255, 0))
        #draw_str(vis, (int(width/2)-50,int(height - height/6)), 'Speed: %.1f' % speed_x_multiplier)
        print("draw the speed multiplier")


    dt = common.clock() - t

    #draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
 #   if speed_x_multiplier >= 0.5:
 #       score = score + dt*2**(1+speed_x_multiplier*2.5)
 #   else :
 #       draw_str(vis, (int(width/2)-50,int(height/2)), 'PAUSED!')
#
    #draw_str(vis, (20,50), 'Score: %.1f' % score)

    #cv2.imshow('facedetect', vis)
# facecontroller code end
    print(type(middle_y), type(h), type(height))
    chicken_y_pos = middle_y * (h/height)

    screen.fill((255, 255, 255))
    screen.blit(get_image('images/clearsky.png'), (0, 0))
    screen.blit(get_image('images/smallclouds.png'), (small_clouds_x,h/4))
    screen.blit(get_image('images/chicken.png'), (w/4,chicken_y_pos))
    screen.blit(get_image('images/bigclouds.png'), (bigcloud_x,h/2))
    textOnScreen(screen, "Score: " + str(int(score)), 40, 0)
    textOnScreen(screen, "Speed: " + str(round(speed_x_multiplier, 2)), 40, h-110)
    if face_detected:
        draw_face_detect(screen, left_x, right_x, top_y, bottom_y)

    if game_paused:
        textOnScreen(screen, "PAUSED!", w/4, h/2)

    else: # the game is not paused!
        score = score + dt*2**(1+speed_x_multiplier*2.5)
        if bigcloud_x < -big_cloud_width:
            bigcloud_x = w
        else:
            bigcloud_x = bigcloud_x - speed_big_cloud * ( 1 + speed_x_multiplier**4)

        if small_clouds_x < -small_clouds_width:
            small_clouds_x = w
        else:
            small_clouds_x = small_clouds_x - speed_small_clouds *( 1 + speed_x_multiplier**4)

    pygame.display.flip()
    clock.tick(60)
