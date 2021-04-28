import pygame


def load_image(file_name):
    try:
        image = pygame.image.load(file_name)
    except pygame.error as message:
        print('Cannot load image:', file_name)
    image = image.convert_alpha()
    return image

# подготовка экрана
screen = pygame.display.set_mode((950, 540))
clock = pygame.time.Clock()
running = True
allsprite_group = pygame.sprite.Group()
balls_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()

# класс снежок
class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(balls_group, allsprite_group)
        self.image = load_image("images/ball_small.png")
        self.x, self.y = pos
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)
        print(self.x, self.y)

    def update(self):
        pass
        #self.rect = self.rect.move(0, 5)
        #print("ud", self.x, self.y)

# класс Олаф
class Olaf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(target_group)
        self.image = load_image("images/olaf_small.png")
        self.x, self.y = pos
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)


#загрузка фона и снежка
fon = load_image("images/fon.jpg")
screen.blit(fon, (0, 0))

b = Ball((50, 400))
olaf = Olaf((700, 300))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Ball(event.pos)
    #screen.fill("white")
    screen.blit(fon, (0, 0))
    balls_group.update()
    balls_group.draw(screen)
    target_group.draw(screen)
    pygame.display.flip()
    clock.tick(10)