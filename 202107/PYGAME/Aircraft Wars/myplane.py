import pygame

pygame.init()

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, image, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.width, self.height = bg_size[0], bg_size[1]
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, \
                            self.height - self.rect.height - 60
        self.speed = 10

    def moveUp(self):
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.rect.top == 0

    def moveDown(self):
            if self.rect.top < self.height - self.rect.height - 60:
                self.rect.top += self.speed
            else:
                self.rect.top == self.height - self.rect.height - 60

    def moveLeft(self):
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.rect.left == 0

    def moveRight(self):
            if self.rect.left < self.width - self.rect.width:
                self.rect.left += self.speed
            else:
                self.rect.left == self.width - self.rect.width