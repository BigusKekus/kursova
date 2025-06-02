import pygame
from model.config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED
from model.bullet import Bullet

class Player:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2,
                                SCREEN_HEIGHT - PLAYER_HEIGHT - 10,
                                PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    def update(self):
        pass
    def shoot(self):
        bullet_x = self.rect.centerx - 1  # підгонка до ширини кулі
        bullet_y = self.rect.y + self.rect.height * 0.01  # або ручне число
        return Bullet(bullet_x, bullet_y, -10)

    def reset_position(self):
        self.rect.x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
