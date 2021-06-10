import pygame
from class_lib import load_image, Ball, Game, balls_group, WIDTH_SCREEN, HEIGHT_SCREEN, FPS, Olaf, Panel, target_group
from class_lib import HEIGHT_PANEL
from screen_saver import start_screen


pygame.init()


start_screen()
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN + HEIGHT_PANEL))
pygame.display.set_caption('Собери Олафа')
clock = pygame.time.Clock()
running = True


fon = load_image("images/fon.jpg")
game = Game(screen)

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop()
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.Shoot(event.pos)

    balls_group.update()
    target_group.update()


    screen.fill("black")
    screen.blit(fon, (0, 0))
    game.update()
    game.blit()

    target_group.draw(screen)
    balls_group.draw(screen)
    game.show_message()

    pygame.display.flip()


    clock.tick(FPS)