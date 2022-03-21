import pygame
import sys
import math
from pygame.locals import *
from random import *

class Mixer(pygame.sprite.Sprite):
    def __init__(self, image, position, speed, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.size = size

    def moving(self):
        self.rect = self.rect.move(self.speed)
        # check if the truck go out of boundary
        if self.rect.right < 0:
            self.rect.left = self.size[0]

        if self.rect.left > self.size[0]:
            self.rect.right = 0

        if self.rect.bottom < 0:
            self.rect.top = self.size[1]

        if self.rect.top > self.size[1]:
            self.rect.bottom = 0

def collide_check(item, target):
    collide_list = []
    for each in target:
        distance = math.sqrt((math.pow((item.rect.center[0] - each.rect.center[0]), 2)) +\
                             (math.pow((item.rect.center[1] - each.rect.center[1]), 2)))
        if distance <= (item.rect.width + each.rect.width) / 2:
            collide_list.append(each)
    return collide_list

def main():
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    image = "mixer_truck.png"
    pygame.display.set_caption('Paring Mixer Trucks')
    bg_picture = pygame.image.load('bg.png')

    mixer_list = []
    running = True
    truck_number = 5
    for i in range(truck_number):
        position = (randint(0, width - 200), randint(0, height - 111))
        speed = [randint(-8, 8), randint(-8, 8)]
        mixer = Mixer(image, position, speed, size)
        while collide_check(mixer, mixer_list):
            mixer.rect.left, mixer.rect.top = (randint(0, width - 200), randint(0, height - 111))
        mixer_list.append(mixer)


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        screen.blit(bg_picture, (0,0))

        for each in mixer_list:
            each.moving()
            screen.blit(each.image, each.rect)

        for i in range(truck_number):
            item = mixer_list.pop(i)

            if collide_check(item, mixer_list):
                item.speed[0] = -item.speed[0]
                item.speed[1] = -item.speed[1]
            mixer_list.insert(i, item)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()