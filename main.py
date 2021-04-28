import pygame
from class_lib import load_image, Ball, Game, balls_group, WIDTH_SCREEN, HEIGHT_SCREEN, FPS, Olaf, Panel, target_group
from screen_saver import start_screen


pygame.init()

panel_height = 100
start_screen()
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN + panel_height))
clock = pygame.time.Clock()
running = True


fon = load_image("images/fon.jpg")
olaf = Olaf()
ball = Ball(olaf)

game = Game(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball.set_speed(event.pos)
            game.update()
    balls_group.update(olaf)
    target_group.update()

    screen.fill("black")
    screen.blit(fon, (0, 0))
    game.blit()
    #screen.blit(game.panel.string_rendered, game.panel.text_rect)

    target_group.draw(screen)
    balls_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)