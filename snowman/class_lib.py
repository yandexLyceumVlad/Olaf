import pygame
import sys
from tkinter import *
from tkinter import messagebox


FPS = 20
WIDTH_SCREEN, HEIGHT_SCREEN = 960, 540
HEIGHT_PANEL = 100
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
        self.vx = (pos[0] - self.x) // 5
        self.vy = (pos[1] - self.y) // 5

    def is_not_in_screen(self):
        x = self.rect.x - self.rect.width // 2
        y = self.rect.y - self.rect.height // 2
        #print(self.rect.x , x, y, WIDTH_SCREEN, HEIGHT_SCREEN)
        return  x > WIDTH_SCREEN or x < 0 or y < 0 or y > HEIGHT_SCREEN - HEIGHT_PANEL

    def update(self):
        if self.move:
            self.vy = self.vy + G
            self.rect = self.rect.move(self.vx, self.vy)



class Olaf(pygame.sprite.Sprite):
    level_pos = [350, 300, 250, 150]
    def __init__(self):
        super().__init__(target_group)
        self.new()

    def new(self):
        self.index_parts = 0
        self.load_part_of_olaf(0)
        self.speed = 0
        self.move = False
        self.count_move = 0
        self.count = 50

    def load_part_of_olaf(self, level):
        try:
            self.image = load_image("images/body" + str(self.index_parts) + ".png")
            # вычисляем маску
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(700, Olaf.level_pos[level])
            self.index_parts += 1
        except:
            print("не могу подгрузить часть Олафа)")

    def set_sped(self):
        self.move = TRUE
        self.speed = 5

    def update(self):
        if self.move:
            self.rect = self.rect.move(self.speed, 0)
            self.count_move += 1
            if self.count_move > self.count:
                self.count_move = 0
                self.speed = - self.speed



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

PANEL_X, PANEL_Y = 100, 550
class Panel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(target_group)
        self.image = load_image("images/panel.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(panel_x, panel_y)
        self.new(0)

    def draw_text(self, text, pos):
        font = pygame.font.Font(None, 30)
        self.string_rendered = font.render(text, 1, pygame.Color('white'))
        self.text_rect = self.string_rendered.get_rect()
        self.text_rect.x = pos[0]
        self.text_rect.top = pos[1]
        Game.screen.blit(self.string_rendered, self.text_rect)

    def draw_message(self, text, pos):
        font = pygame.font.Font(None, 50)
        self.string_rendered = font.render(text, 1, pygame.Color('yellow'))
        self.text_rect = self.string_rendered.get_rect()
        self.text_rect.x = pos[0]
        self.text_rect.top = pos[1]
        Game.screen.blit(self.string_rendered, self.text_rect)

    def new(self, level):
        self.ammo = [Ammo((i, panel_y)) for i in range(Game.ammo_level[level] - 1)]
        self.draw_text("уровень", (10, 550))
        self.draw_text(str(level + 1), (20, 570))

    def delete_ball(self):
        if len(self.ammo) > 0:
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
    screen = None

    def collide(self):
        if self.barrier == None:
            return False
        else:
            return pygame.sprite.collide_mask(self.ball, self.barrier)

    def __init__(self, screen):
        Game.screen = screen
        self.shoot = 0
        self.hit = 0
        self.level = 0
        self.barrier = None
        self.panel = Panel()
        self.olaf = Olaf()
        self.ball = Ball(self.olaf)
        self.running = True

    def stop(self):
        self.running = False

    def levelup(self):
        self.shoot = 0
        self.hit = 0
        if self.level == 0:
            if self.barrier is not None:
                self.barrier.kill()
                self.barrier = None
            self.olaf.new()
        else:
            self.olaf.load_part_of_olaf(self.level)
        self.panel.delete_all()
        self.panel.new(self.level)
        self.ball.new_ball()


    def blit(self):
        try:
            if self.level < 3:
                self.panel.draw_text("уровень", (10, 550))
                self.panel.draw_text(str(self.level + 1), (20, 580))
                self.panel.draw_text("попаданий", (800, 550))
                self.panel.draw_text(str(self.hit) + " из " + str(Game.hit_level[self.level]), (810, 580))
                #self.panel.draw_text("попаданий", (700, 550))
                #self.panel.draw_message("Вы проиграли", (500, 580))
        except:
            pass

    def Shoot(self, pos):
        self.shoot += 1
        self.ball.set_speed(pos)

    def update(self):
        self.text=""
        if self.level < 3:
            # вылет снежка
            if self.ball.is_not_in_screen() or self.collide():
                # print("Снежок потерян")
                self.ball.set_down()
                # снежок упал
                if self.ball.rect.y > HEIGHT_SCREEN - HEIGHT_PANEL:
                    if self.level == 0:
                        #show_message("Снежок потерян!")
                        self.text = "Снежок потерян!"
                    # закончились выстрелы
                    if self.level < len(Game.ammo_level) and self.shoot == Game.ammo_level[self.level]:
                        #show_message("Увы, вы проиграли!")
                        self.level = 0
                        self.levelup()
                    else:
                        self.panel.delete_ball()
                        self.ball.new_ball()
            # попадание в Олафа
            elif pygame.sprite.collide_mask(self.ball, self.olaf):
                if self.level == 0:
                    #show_message("Попал!")
                    self.text = "Попал!"
                self.hit += 1
                if self.hit == Game.hit_level[self.level]:
                    self.level += 1

                    if self.level == 1:
                        self.barrier = Montain()
                    elif self.level == 2:
                        self.olaf.set_sped()

                    if self.level == 3:
                        self.olaf.load_part_of_olaf(self.level)
                        #show_message("Победа!")
                        self.text = "Победа!"
                        self.end_game()
                        #self.stop()
                    else:
                        self.levelup()
                        #show_message("Переход на следующий уровень!")
                        self.text = "Переход на следующий уровень!"
                        print("Shoot ", self.hit, "Level", self.level)
                else:
                    self.olaf.load_part_of_olaf(self.level)
                    self.panel.delete_ball()
                    self.ball.new_ball()

    def end_game(self):
        self.barrier.kill()
        self.panel.kill()
        self.olaf.count = 150
        self.olaf.speed = -5
        self.olaf.load_part_of_olaf(self.level)


    def show_message(self):
        if self.text != "":
            show_message(self.text)
