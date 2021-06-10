from class_lib import WIDTH_SCREEN, HEIGHT_SCREEN, load_image, terminate, FPS
import pygame

screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption('Собери Олафа')
clock = pygame.time.Clock()

def start_screen():
    fon = pygame.transform.scale(load_image('images/zastavka.png'), (WIDTH_SCREEN, HEIGHT_SCREEN))
    screen.blit(fon, (0, 0))

    running_screen_save = True
    while running_screen_save:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_screen_save = False
            elif event.type == pygame.KEYDOWN or \
                     event.type == pygame.MOUSEBUTTONDOWN:
                running_screen_save = False
        pygame.display.flip()
        clock.tick(FPS)
    print("Заставка закрыта")
