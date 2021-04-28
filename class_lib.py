import pygame
import sys
from tkinter import *
from tkinter import messagebox


FPS = 20
WIDTH_SCREEN, HEIGHT_SCREEN = 960, 540
allsprite_group = pygame.sprite.Group()
balls_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()
# ускорение свободного падения
G = 1

def terminate():
    pygame.quit()
    sys.exit()

def show_message(text):
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo('Информация', text)

def load_image(file_name):
    try:
        image = pygame.image.load(file_name)
        image = image.convert_alpha()
        return image
    except:
        print("НЕ возможно подгрузить картинку")

class Ball(pygame.sprite.Sprite):
    def __init__(self, obj):
        super().__init__(balls_group)
        self.image = load_image("images/ball0.png")
        self.new_ball()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


    def new_ball(self):
        self.x, self.y = (50, 450)
        self.vx = 0
        self.vy = 0
        self.move = False
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x - self.rect.width // 2, self.y - self.rect.height // 2)

    def set_down(self):
        self.vx = 0
        self.vy = 20

    def set_speed(self, pos):
        self.move = True
        self.vx = self.x - pos[0]
        self.vy = self.y - pos[1]

    def is_in_screen(self):
        x = self.rect.x - self.rect.width // 2
        y = self.rect.y - self.rect.height // 2
        #print(self.rect.x , x, y, WIDTH_SCREEN, HEIGHT_SCREEN)
        return  x > WIDTH_SCREEN or x < 0 or y < 0 or y > HEIGHT_SCREEN

    def check_collble_objects(self):
        for obj in Ball.collable_objects:

                return True

    def update(self, obj):
        if self.move:
            self.vy = self.vy + G
            self.rect = self.rect.move(self.vx, self.vy)
            if self.is_in_screen() or Game.collide(self):
                #print("Снежок потерян")
                self.set_down()
                if self.rect.y > HEIGHT_SCREEN:
                    if Game.level == 0:
                        show_message("Снежок потерян!")
                    self.new_ball()

            if pygame.sprite.collide_mask(self, obj):
                if Game.level == 0:
                    show_message("Попал!")
                Game.hit += 1
                obj.load_part_of_olaf()
                self.new_ball()


class Olaf(pygame.sprite.Sprite):
    level_pos = [350, 300, 250]
    def __init__(self):
        super().__init__(target_group)
        self.index_parts = 0
        self.load_part_of_olaf()

    def load_part_of_olaf(self):
        try:
            self.image = load_image("images/body" + str(self.index_parts) + ".png")
            # вычисляем маску
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(700, Olaf.level_pos[Game.level])
            self.index_parts += 1
        except:
            print("не могу подгрузить часть Олафа)")

class Montain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(target_group)
        self.x, self.y = 300, 250
        self.image = load_image("images/barrier.png")
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

panel_x, panel_y = 200, 550

class Ammo(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(target_group)
        self.image = load_image("images/ball0.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(panel_x + pos[0] * self.rect.width, pos[1])


class Panel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(target_group)
        self.image = load_image("images/panel.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(panel_x, panel_y)
        self.new()

    def draw_text(self, text, pos):
        font = pygame.font.Font(None, 30)
        self.string_rendered = font.render(text, 1, pygame.Color('white'))
        self.text_rect = self.string_rendered.get_rect()
        self.text_rect.x = pos[0]
        self.text_rect.top = pos[1]
        Game.screen.blit(self.string_rendered, self.text_rect)

    def new(self):
        self.ammo = [Ammo((i, panel_y)) for i in range(Game.ammo_level[Game.level] - 1)]
        self.draw_text("уровень", (10, 550))

    def delete_ball(self):
        self.ammo.pop().kill()

    def delete_all(self):
        for i in self.ammo:
            self.delete_ball()

    def update(self):
        pass
        # for i in self.ammo:
        #     i.update()


class Game():
    ammo_level = [5, 5, 3]
    hit_level = [2, 3, 1]
    hit = 0
    barrier = None
    screen = None
    level = 0

    def collide(ball):
        print("Стоит барьер", Game.barrier)
        if Game.barrier == None:
            return False
        else:
            return pygame.sprite.collide_mask(ball, Game.barrier)

    def __init__(self, screen):
        Game.screen = screen
        self.shoot = 0
        self.panel = Panel()

    def levelup(self):
        self.shoot = 0
        self.panel.delete_all()
        self.panel.new()

    def blit(self):
        ##Game.screen.blit(self.panel.string_rendered, self.panel.text_rect)
        self.panel.draw_text("уровень", (10, 550))

    def update(self):
        self.shoot += 1
        self.panel.delete_ball()
        print("Shoot ", Game.hit, Game.level)
        if Game.hit == Game.hit_level[self.level]:
            Game.level += 1
            if Game.level == 1:
                Game.barrier = Montain()
            self.levelup()
            show_message("Переход на слудующий уровень!")
        else:
            if self.shoot == Game.ammo_level[Game.level]:
                show_message("Увы, вы проиграли!")
                Game.level = 0
                self.levelup()



