import pygame
import sys
import myplane
import traceback
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Aircraft Wars")
background = pygame.image.load("images\\background.png").convert()
myplane_image = "images\\me1.png"
clock = pygame.time.Clock()

running = True

# background music and Sounds
pygame.mixer.music.load("sound\\game_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
bullet_sound = pygame.mixer.Sound("sound\\bullet.wav")
bullet_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound\\enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound\\enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound\\enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound("sound\\enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound\\get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound\\get_bullet.wav")
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound\\me_down.wav")
me_down_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound\\supply.wav")
supply_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound\\upgrade.wav")
upgrade_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound("sound\\use_bomb.wav")
use_bomb_sound.set_volume(0.2)

# create myplane
myplane = myplane.MyPlane(myplane_image, bg_size)
key_pressed_list = []


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    key_pressed_list = pygame.key.get_pressed()
    # Use WSAD or UP/DOWN/LEFT/RIGHT to move myplane
    if key_pressed_list[K_w] or key_pressed_list[K_UP]:
        myplane.moveUp()

    if key_pressed_list[K_s] or key_pressed_list[K_DOWN]:
        myplane.moveDown()

    if key_pressed_list[K_a] or key_pressed_list[K_LEFT]:
        myplane.moveLeft()

    if key_pressed_list[K_d] or key_pressed_list[K_RIGHT]:
        myplane.moveRight()

    screen.blit(background, (0,0))
    screen.blit(myplane.image, myplane.rect)
    pygame.display.flip()
    clock.tick(60)

