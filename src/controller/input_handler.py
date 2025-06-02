import pygame
import sys

def handle_input(player, state_manager, game_controller, events):
    keys = pygame.key.get_pressed()
    if state_manager.is_playing():
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_SPACE]:
            game_controller.shoot_bullet()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if state_manager.is_playing():
                state_manager.set_paused()
            elif state_manager.is_paused():
                state_manager.set_playing()