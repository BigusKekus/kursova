import pygame
from model.config import WHITE, SCREEN_HEIGHT, SCREEN_WIDTH
import os
import sys


class Renderer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.load_images()

    def load_images(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        assets_path = os.path.join(base_path, "..", "assets", "images")
        self.player_image = pygame.image.load(os.path.join(assets_path, "player.png")).convert_alpha()
        self.enemy_image = pygame.image.load(os.path.join(assets_path, "enemy.png")).convert_alpha()
        self.boss_image = pygame.image.load(os.path.join(assets_path, "boss.png")).convert_alpha()

    def load_images(self):
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
        self.player_image = pygame.image.load(os.path.join(assets_path, "player.png")).convert_alpha()
        self.enemy_image = pygame.image.load(os.path.join(assets_path, "enemy.png")).convert_alpha()
        self.boss_image = pygame.image.load(os.path.join(assets_path, "boss.png")).convert_alpha()

    def draw_background(self, stars):
        self.screen.fill((0, 0, 0))
        for star in stars:
            star.draw(self.screen)

    def draw_entities(self, player, enemies, bullets, bosses):
        self.screen.blit(self.player_image, self.player_image.get_rect(center=player.rect.center))
        for enemy in enemies:
            self.screen.blit(self.enemy_image, self.enemy_image.get_rect(center=enemy.rect.center))
        for boss in bosses:
            self.screen.blit(self.boss_image, self.boss_image.get_rect(center=boss.rect.center))
            hp_text = self.font.render(str(boss.health), True, WHITE)
            hp_rect = hp_text.get_rect(center=(boss.rect.centerx, boss.rect.top - 10))
            self.screen.blit(hp_text, hp_rect)

        for bullet in bullets:
            pygame.draw.rect(self.screen, bullet.color, bullet.rect)

    def draw_ui(self, score, timer, level):
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        timer_text = self.font.render(f"Time: {timer}", True, WHITE)
        level_text = self.font.render(f"Level: {level}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))
        self.screen.blit(level_text, ((SCREEN_WIDTH - level_text.get_width()) // 2, 10))
    def draw_message(self, message):
        text = self.font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(text, text_rect)

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self.screen)

    def draw_game_over_stats(self, score, timer, level):
        lines = [
            f"Score: {score}",
            f"Time: {timer}",
            f"Level: {level}"
        ]
        for i, line in enumerate(lines):
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 40))
            self.screen.blit(text, text_rect)

    def draw_guide(self):
        guide_lines = [
            "GUIDE",
            "Use arrow keys to move.",
            "Press SPACE to shoot.",
            "Press ESC to pause",
            "Avoid enemy, don`t let them touch you.",
            "Destroy all enemies to win.",
        ]
        for i, line in enumerate(guide_lines):
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            self.screen.blit(text, text_rect)

    def update_display(self):
        pygame.display.flip()

    def render(self, state_manager, game_controller, stars):
        self.draw_background(stars)
        if state_manager.is_main_menu():
            self.draw_message("SPACE INVADERS")
            self.draw_buttons(game_controller.menu_buttons)
        elif state_manager.is_playing():
            self.draw_entities(
                game_controller.player,
                game_controller.enemies,
                game_controller.bullets,
                game_controller.bosses
            )
            self.draw_ui(
                game_controller.score,
                game_controller.get_formatted_time(),
                game_controller.level
            )
        elif state_manager.is_paused():
            self.draw_message("PAUSED")
            self.draw_buttons(game_controller.pause_buttons)

        elif state_manager.is_game_over():
            self.draw_message("GAME OVER")
            self.draw_game_over_stats(
                game_controller.score,
                game_controller.get_formatted_time(),
                game_controller.level
            )
            self.draw_buttons(game_controller.game_over_buttons)
        elif state_manager.is_guide():
            self.draw_guide()
            self.draw_buttons(game_controller.guide_buttons)
        elif state_manager.is_next_level():
            self.draw_message("NEXT LEVEL")
        self.update_display()



