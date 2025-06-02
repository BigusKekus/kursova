import pygame
import random
from model.config import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, BOSS_WIDTH, BOSS_HEIGHT
from model.enemy import Enemy, BossEnemy
from view.ui import Button
import sys

class GameController:
    def create_enemies(self):
        self.enemies.clear()
        self.bosses.clear()
        if self.level % 5 == 0:
            boss_health = 15 + self.level
            boss_x = SCREEN_WIDTH // 2 - BOSS_WIDTH // 2
            boss_y = 100
            boss = BossEnemy(boss_x, boss_y, boss_health)
            self.bosses.append(boss)
        else:
            PADDING = 50
            enemy_count = 5 + self.level
            for _ in range(enemy_count):
                x = random.randint(PADDING, SCREEN_WIDTH - ENEMY_WIDTH - PADDING)
                y = random.randint(50, 200)
                self.enemies.append(Enemy(x, y))

    def __init__(self, player, bullet_speed, font, state_manager):
        self.player = player
        self.bullets = []
        self.enemies = []
        self.bosses = []
        self.enemy_direction = 1
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.paused_time = 0
        self.pause_start = None
        self.final_time = None
        self.bullet_speed = bullet_speed
        self.last_shot_time = 0
        self.shoot_delay = 500
        self.font = font
        self.level = 1
        self.state_manager = state_manager
        self.next_level_start_time = None
        self.menu_buttons = [
            Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 40, "Play", self.font, self.start_game),
            Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40, "Guide", self.font, self.show_guide),
            Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 100, 40, "Exit", self.font, lambda: sys.exit())
        ]
        self.pause_buttons = [
            Button(SCREEN_WIDTH // 2 - 75, 350, 150, 40, "Return", font, self.resume_game),
            Button(SCREEN_WIDTH // 2 - 75, 410, 150, 40, "Restart", font, self.start_game),
            Button(SCREEN_WIDTH // 2 - 75, 470, 150, 40, "Menu", font, self.return_to_menu),
        ]
        self.game_over_buttons = [
            Button(SCREEN_WIDTH // 2 - 60, 400, 120, 40, "Retry", self.font, self.start_game),
            Button(SCREEN_WIDTH // 2 - 60, 460, 120, 40, "Menu", self.font, self.return_to_menu)
        ]
        self.guide_buttons = [
            Button(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 100, 120, 40, "Back", self.font, self.return_to_menu)
        ]

        self.create_enemies()

    def start_game(self):
        self.bullets.clear()
        self.enemies.clear()
        self.bosses.clear()
        self.level = 1
        self.score = 0
        self.create_enemies()
        self.start_time = pygame.time.get_ticks()
        self.final_time = None
        self.paused_time = 0
        self.pause_start = None
        self.state_manager.set_playing()

    def pause_game(self):
        if self.pause_start is None:
            self.pause_start = pygame.time.get_ticks()
        self.state_manager.set_paused()

    def resume_game(self):
        if self.pause_start:
            self.paused_time += pygame.time.get_ticks() - self.pause_start
            self.pause_start = None
        self.state_manager.set_playing()
    def set_game_over(self):
        if self.pause_start:
            self.paused_time += pygame.time.get_ticks() - self.pause_start
            self.pause_start = None
        if self.final_time is None:
            self.final_time = pygame.time.get_ticks()
        self.state_manager.set_game_over()

    def return_to_menu(self):
        self.state_manager.set_main_menu()

    def show_guide(self):
        self.state_manager.set_guide()

    def get_formatted_time(self):
        if self.final_time is not None:
            elapsed_time = (self.final_time - self.start_time - self.paused_time) // 1000
        elif self.pause_start is not None:
            elapsed_time = (self.pause_start - self.start_time - self.paused_time) // 1000
        else:
            now = pygame.time.get_ticks()
            elapsed_time = (now - self.start_time - self.paused_time) // 1000

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return f"{minutes:02}:{seconds:02}"
    def update(self):
        if self.state_manager.is_next_level():
            now = pygame.time.get_ticks()
            if now - self.next_level_start_time >= 750:
                self.level += 1
                self.bullets.clear()
                self.create_enemies()
                self.state_manager.set_playing()
            return
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.rect.bottom > 0]

        for enemy in self.enemies[:]:
            enemy.rect.x += self.enemy_direction
            if enemy.rect.bottom >= SCREEN_HEIGHT or enemy.rect.colliderect(self.player.rect):
                self.set_game_over()
                return
            if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
                self.enemy_direction *= -1
                for e in self.enemies:
                    e.rect.y += 20
                break

        for boss in self.bosses[:]:
            boss.rect.x += self.enemy_direction
            if boss.rect.bottom >= SCREEN_HEIGHT or boss.rect.colliderect(self.player.rect):
                self.set_game_over()
                return
            if boss.rect.right >= SCREEN_WIDTH or boss.rect.left <= 0:
                self.enemy_direction *= -1
                for b in self.bosses:
                    b.rect.y += 25
                break

        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.score += 10
                    break

        for bullet in self.bullets[:]:
            for boss in self.bosses[:]:
                if bullet.rect.colliderect(boss.rect):
                    boss.health -= 1
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if boss.health <= 0:
                        self.bosses.remove(boss)
                        self.score += 50
                        self.shoot_delay = max(100, self.shoot_delay - 50)
                    break

        if not self.enemies and not self.bosses:
            self.state_manager.set_next_level()
            self.next_level_start_time = pygame.time.get_ticks()
    def shoot_bullet(self):
        if not self.state_manager.is_playing():
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            bullet = self.player.shoot()
            self.bullets.append(bullet)
            self.last_shot_time = current_time



