import pygame
import os

w = 800
h = 600
bigcloud_x = w
small_clouds_x = w
speed_big_cloud = 3
speed_small_clouds = 1
small_clouds_width = 704
big_cloud_width = 549
speed_x_multiplier = 0.5

_image_library = {}

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

#bg = pygame.image.load("images/clearsky.png")
#chicken = pygame.image.load("images/chicken.png")
#smallclouds = pygame.image.load("images/smallclouds.png")
#bigclouds = pygame.image.load("images/bigclouds.png")

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    screen.blit(get_image('images/clearsky.png'), (0, 0))
    screen.blit(get_image('images/smallclouds.png'), (small_clouds_x,h/4))
    screen.blit(get_image('images/chicken.png'), (w/4,h/2))
    screen.blit(get_image('images/bigclouds.png'), (bigcloud_x,h/2))

    if bigcloud_x < -big_cloud_width:
        bigcloud_x = w
    else:
        bigcloud_x = bigcloud_x - speed_big_cloud * speed_x_multiplier**2

    if small_clouds_x < -small_clouds_width:
        small_clouds_x = w
    else:
        small_clouds_x = small_clouds_x - speed_small_clouds * speed_x_multiplier**2
    pygame.display.flip()
    clock.tick(60)