import pygame
import sys
import traceback
from pygame.locals import *
from random import *

# define a Mixer class that inherits from Sprite
class Mixer(pygame.sprite.Sprite):
    def __init__(self, mixer_image, park_image, position, speed, size, target):
        pygame.sprite.Sprite.__init__(self)

        self.mixer_image = pygame.image.load(mixer_image).convert_alpha()
        self.park_image = pygame.image.load(park_image).convert_alpha()
        self.rect = self.mixer_image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.size = size
        self.target = target
        self.control = False
        self.direction = [choice([-1, 1]), choice([-1, 1])]
        self.collided = False

    # a method for truck moving
    def moving(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.direction[0] * self.speed[0], self.direction[1] * self.speed[1]))

        # circle the moving when it gets out of boundary
        if self.rect.right <= 0:
            self.rect.left = self.size[0]

        elif self.rect.left >= self.size[0]:
            self.rect.right = 0

        elif self.rect.bottom <= 0:
            self.rect.top = self.size[1]

        elif self.rect.top >= self.size[1]:
            self.rect.bottom = 0

    # check if the mouse motion meet the requirement to stop a truck
    def check(self, motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return False

# class for the specific are for mouse moving
class Ipad(pygame.sprite.Sprite):
    def __init__(self, ipad_image, mouse_image, size):
        pygame.sprite.Sprite.__init__(self)

        self.size = size
        self.ipad_image = pygame.image.load('ipad.png').convert_alpha()
        self.ipad_rect = self.ipad_image.get_rect()
        self.ipad_rect.center = self.size[0] // 2, self.ipad_rect.height // 2

        self.mouse_image = pygame.image.load('mouse.png').convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = self.ipad_rect.left, self.ipad_rect.top
        # made the mouse invisible so that new mouse pic can be used
        pygame.mouse.set_visible(False)


def main():
    pygame.init()
    pygame.mixer.init()

    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    mixer_image = "mixer_truck.png"
    park_image = "park_mixer_truck.png"
    ipad_image = "ipad.png"
    mouse_image = "mouse.png"

    pygame.display.set_caption('Paring Mixer Trucks')
    bg_picture = pygame.image.load('bg.png').convert_alpha()
    win_picture = pygame.image.load('win.png').convert_alpha()
    win_rect = win_picture.get_rect()
    win_rect.center = width // 2, height // 2

    truck_num = 5
    running = True
    mixer_list = []
    msgs = []

    #used for collide checking
    group = pygame.sprite.Group()

    # specific place for parking the truck
    location = [(130, 140, 494, 504), (430, 440, 695, 705), (698, 708, 415, 425), (1097, 1107, 695, 705), (1288, 1298, 513,523)]

    # creating the trucks
    for i in range(truck_num):
        # random position and speed(200x111 is the size for the truck pic)
        position = (randint(0, width - 200), randint(0, height - 111))
        speed = [randint(1, 10), randint(1, 10)]
        mixer = Mixer(mixer_image, park_image, position, speed, size, 5 * (i + 1))

        # checking the collision while creating the mixer, allocate a new position if collided
        while pygame.sprite.spritecollide(mixer, group, False):
            mixer.rect.left, mixer.rect.top = randint(0, width - 200), randint(0, height - 111)

        mixer_list.append(mixer)
        group.add(mixer)

    # background music and sound
    pygame.mixer.music.load('bg_dance.ogg')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    park_sound = pygame.mixer.Sound('parked.wav')
    winner_sound = pygame.mixer.Sound('winner.wav')
    loser_sound = pygame.mixer.Sound('loser.wav')
    laugh_sound = pygame.mixer.Sound('laugh.wav')

    # set userevent to play loser & laugh sound when music is over
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    # get a ipad obj
    ipad = Ipad(ipad_image, mouse_image, size)

    # counts the movement of mouse per sec
    motion = 0

    # set userevent to check the motion per second
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER, 1000)

    # send the key event every 100ms when push down a key
    pygame.key.set_repeat(100, 100)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            # capture the GAMEOVER event to play sounds
            elif event.type == GAMEOVER:
                loser_sound.play()
                pygame.time.delay(2000)
                laugh_sound.play()
                running = False

            # capture the MYTIMER event to check motion
            elif event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            each.speed = [0, 0]
                            each.control = True
                    motion = 0

            # capture the mouse motion to increase motion value
            elif event.type == MOUSEMOTION:
                motion += 1

            # WASD to move the truck
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1

                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1

                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1

                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1

                # space to check if the truck has entered the correct location
                if event.key == K_SPACE:
                    for each in group:
                        if each.control:
                            for i in location:
                                if i[0] < each.rect.left < i[1] and i[2] < each.rect.top < i[3]:
                                    park_sound.play()
                                    each.speed = [0, 0]
                                    group.remove(each)
                                    temp = mixer_list.pop(mixer_list.index(each))
                                    mixer_list.insert(0, temp)
                                    location.remove(i)

                                # if all trucks have parked then show victory
                                if not location:
                                    pygame.mixer.music.stop()
                                    winner_sound.play()
                                    pygame.time.delay(3000)
                                    msg = (win_picture, win_rect)
                                    msgs.append(msg)
                                    laugh_sound.play()

        screen.blit(bg_picture, (0,0))
        screen.blit(ipad.ipad_image, ipad.ipad_rect)

        # use the new mouse image
        ipad.mouse_rect.center = pygame.mouse.get_pos()
        # the mouse can only show in the boundary of ipad image
        if ipad.mouse_rect.left < ipad.ipad_rect.left:
            ipad.mouse_rect.left = ipad.ipad_rect.left
        if ipad.mouse_rect.right > ipad.ipad_rect.right:
            ipad.mouse_rect.right = ipad.ipad_rect.right
        if ipad.mouse_rect.top < ipad.ipad_rect.top:
            ipad.mouse_rect.top = ipad.ipad_rect.top
        if ipad.mouse_rect.bottom > ipad.ipad_rect.bottom:
            ipad.mouse_rect.bottom = ipad.ipad_rect.bottom

        # blit the mouse image
        screen.blit(ipad.mouse_image, ipad.mouse_rect)

        # adding mixer into the screen and let them move
        for each in mixer_list:
            each.moving()
            if each.collided:
                each.speed = [randint(1, 10), randint(1, 10)]
                each.collided = False

            # check the control flag and blit different pic
            if each.control:
                screen.blit(each.park_image, each.rect)
            else:
                screen.blit(each.mixer_image, each.rect)

        # collide checking and reverse the speed if collided
        # the move direction reversed after 2 truck collided
        # if the controlled truck is collided then its direction reversed(-1)
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each, group, False):
                each.direction[0] = -each.direction[0]
                each.direction[1] = -each.direction[1]
                each.collided = True
                if each.control:
                    each.direction[0] = -1
                    each.direction[1] = -1
                    each.control = False
            group.add(each)

        for each in msgs:
            screen.blit(each[0], each[1])

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    # capture the exception if using double-click in cmd
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input("please contact author!")

# This is a test for emergency fix