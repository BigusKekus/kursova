import pygame
from model.config import BULLET_WIDTH, BULLET_HEIGHT, RED

class Bullet:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x - BULLET_WIDTH // 2, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.color = RED
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

