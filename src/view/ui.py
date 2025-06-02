import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, action, color=(200, 200, 200), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


def draw_text_centered(screen, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text_surface, text_rect)