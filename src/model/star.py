import random
import pygame
from model.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.randint(1, 3)
        self.radius = random.randint(1, 2)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

def generate_starfield(count):
    return [Star() for _ in range(count)]
