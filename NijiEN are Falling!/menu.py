import pygame

pygame.init()

# set up the display
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Main Menu")

# set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# main menu loop
menu_loop = True
while menu_loop: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_loop = False

    game_display.fill(WHITE)

    # draw the menu text
    title_font = pygame.font.SysFont('Arial', 40)
    title_text = title_font.render("Main Menu", True, BLACK)
    game_display.blit(title_text, (DISPLAY_WIDTH/2 - title_text.get_width()/2, 200))

    # draw the buttons
    play_font = pygame.font.SysFont('Arial', 30)
    play_text = play_font.render("Play", True, WHITE)
    play_rect = pygame.Rect(DISPLAY_WIDTH/2 - play_text.get_width()/2, 300, play_text.get_width(), play_text.get_height())
    pygame.draw.rect(game_display, GREEN, play_rect)
    game_display.blit(play_text, (DISPLAY_WIDTH/2 - play_text.get_width()/2, 300))

    settings_text = play_font.render("Settings", True, WHITE)
    settings_rect = pygame.Rect(DISPLAY_WIDTH/2 - settings_text.get_width()/2, 400, settings_text.get_width(), settings_text.get_height())
    pygame.draw.rect(game_display, BLUE, settings_rect)
    game_display.blit(settings_text, (DISPLAY_WIDTH/2 - settings_text.get_width()/2, 400))

    pygame.display.update()

pygame.quit()