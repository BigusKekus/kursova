import pygame
from model.config import ENEMY_WIDTH, ENEMY_HEIGHT, BOSS_WIDTH, BOSS_HEIGHT, RED
class Enemy:
    def __init__(self, x, y, is_boss=False):
        self.is_boss = is_boss
        if self.is_boss:
            self.rect = pygame.Rect(x, y, BOSS_WIDTH, BOSS_HEIGHT)
            self.health = 5
        else:
            self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.color = RED

class BossEnemy(Enemy):
    def __init__(self, x, y, boss_health):
        super().__init__(x, y, is_boss=True)
        self.health = boss_health

