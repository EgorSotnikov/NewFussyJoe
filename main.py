import pygame
import sys
import os
from pygame import transform

pygame.init()
size = width, height = 1500, 750
screen = pygame.display.set_mode(size)


FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if name == "Grass_Tile.png" or name == "Floor_Tile.png" or name == 'Can.png' or name == 'Work.png' or \
            name == 'Clear.png':
        return pygame.transform.scale(image, (75, 75))
    if name == "NewCow.png":
        return pygame.transform.scale(image, (180, 90))
    if name == "Cowshed.png":
        return pygame.transform.scale(image, (600, 300))
    if name == "TableEmpty.png":
        return pygame.transform.scale(image, (200, 100))
    if name[0:8] == "TableDoc":
        return pygame.transform.scale(image, (200, 100))
    if name[0:4] == "Home":
        return pygame.transform.scale(image, (750, 375))
    return image


def start_screen():
    intro_text = ["Правила игры:",
                  "с каждой секундой увеличивается кол-во молока в корове,",
                  "документов на столе и воды в ванне. Для перемещения используйте",
                  "стрелки. Чтобы подоить корову, подписать документ или слить",
                  "воду из ванны встаньте на нужную кнопку и нажмите 'Пробел'.",
                  "Если заполненность коровы/стола/ванны достигнет 12,",
                  "то игра закончится. Ваша задача - продержаться максимально долго.",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('Start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def finish_screen(cause, t):
    end_text = [cause, f"Вы продержались {t} секунд.", "Игра Егора Сотникова"]
    fon = pygame.transform.scale(load_image('Start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 200
    for line in end_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                global running
                running = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('floor', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                x_p, y_p = x, y
            elif level[y][x] == 'v':
                Tile('grass', x, y)
                x_c, y_c = x, y
            elif level[y][x] == '^':
                Tile('grass', x, y)
                x_cs, y_cs = x, y
            elif level[y][x] == '-':
                Tile('floor', x, y)
                x_t, y_t = x, y
            elif level[y][x] == '[':
                Tile('can', x, y)
            elif level[y][x] == '+':
                Tile('floor', x, y)
                x_h, y_h = x, y
            elif level[y][x] == '*':
                Tile('ht', x, y)
            elif level[y][x] == '|':
                Tile('work', x, y)
            elif level[y][x] == ':':
                x_cl, y_cl = x, y
            elif level[y][x] == '0':
                Tile('score', x, y)
    # вернем игрока, корову, а также размер поля в клетках
    return Home(x_h, y_h), Cow(x_c, y_c), Cowshed(x_cs, y_cs), Table(x_t, y_t), \
           ClearButton(x_cl, y_cl), Player(x_p, y_p), x, y


tile_images = {
    'floor': load_image('Floor_Tile.png'),
    'grass': load_image('Grass_Tile.png'),
    'can': load_image('Can.png'),
    'ht': load_image('HomeTile.png'),
    'work': load_image('Work.png'),
    'score': load_image('Score.png')
}
clear_image = load_image('Clear.png')
cow_image = load_image('NewCow.png')
cowshed_image = load_image('Cowshed.png')
table_image = load_image('TableDoc0.png')
home_image = load_image('Home1.png')
player_image = load_image('mar.png')

player = None
tile_width = tile_height = 75
tiles_group = pygame.sprite.Group()
cow_group = pygame.sprite.Group()
cowshed_group = pygame.sprite.Group()
table_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
home_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


milk_button = 0
work_button = 0
clear_button = 0
milk_level = 0
work_level = 0
bath_level = 0
time_level = 0


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Cow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cow_group, all_sprites)
        self.iter, self.size_x, self.size_y = 1, 180, 90
        self.image = cow_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 35, tile_height * pos_y - 15)

    def ani(self, *args):
        global milk_level
        if self.iter % 120 == 0 and milk_level != 12:
            self.rect.x -= 0.025 * self.size_x
            self.rect.y -= 0.05 * self.size_y
            self.size_x *= 1.05
            self.size_y *= 1.05
            self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            milk_level += 1
        elif self.iter % 120 == 0 and milk_level == 12:
            global status
            status = "Корова лопнула!"
        self.iter += 1

    def update(self, *args):
        global milk_level
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_SPACE and milk_level != 0 and milk_button == 1:
                self.rect.x += 0.05 * self.size_x
                self.rect.y += 0.1 * self.size_y
                self.size_x /= 1.1
                self.size_y /= 1.1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
                milk_level -= 1


class Cowshed(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cowshed_group, all_sprites)
        self.image = cowshed_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 50)


class Table(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(table_group, all_sprites)
        self.image = table_image
        self.iter = 1
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 35)

    def ani(self):
        global work_level
        if self.iter % 120 == 0 and work_level < 12:
            work_level += 1
        elif self.iter % 120 == 0 and work_level == 12:
            global status
            status = "Слишком много документов!"
        self.image = load_image(f'TableDoc{work_level}.png')
        self.iter += 1

    def update(self, *args):
        global work_level
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_SPACE and work_level != 0 and work_button == 1:
                work_level -= 1
                self.image = self.image = load_image(f'TableDoc{work_level}.png')


class Home(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(table_group, all_sprites)
        self.image = home_image
        self.iter = 1
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 37.5)

    def ani(self):
        global bath_level
        if self.iter % 120 == 0 and bath_level + 1 < 13:
            bath_level += 1
        elif self.iter % 120 == 0 and bath_level == 12:
            global status
            status = "Ванную затопило!"
        self.image = load_image(f'Home{bath_level + 1}.png')
        self.iter += 1

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            global bath_level
            if args[0].key == pygame.K_SPACE and bath_level + 1 != 1 and clear_button == 1:
                bath_level -= 1
                self.image = self.image = load_image(f'Home{bath_level + 1}.png')


class ClearButton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cowshed_group, all_sprites)
        self.image = clear_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 5)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25, tile_height * pos_y + 15)

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_RIGHT:
                self.rect.x += tile_width
            elif args[0].key == pygame.K_LEFT:
                self.rect.x -= tile_width
            elif args[0].key == pygame.K_UP:
                self.rect.y -= tile_height
            elif args[0].key == pygame.K_DOWN:
                self.rect.y += tile_height
        global milk_button
        if self.rect.x == 475 and self.rect.y == 390:
            milk_button = 1
        else:
            milk_button = 0
        global work_button
        if self.rect.x == 1075 and self.rect.y == 240:
            work_button = 1
        else:
            work_button = 0
        global clear_button
        if self.rect.x == 1150 and self.rect.y == 465:
            clear_button = 1
        else:
            clear_button = 0


home, cow, cowshed, table, clear, player, level_x, level_y = generate_level(load_level('level.txt'))
status = ''
clock = pygame.time.Clock()
start_screen()
while status == '':
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(event)
    cow.ani()
    table.ani()
    home.ani()
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    score_line = f'Time: {time_level // 60} Cow: {milk_level}  Work: {work_level}  Bath: {bath_level}'
    font = pygame.font.Font(None, 60)
    string_rendered = font.render(score_line, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 25
    intro_rect.height = 50
    intro_rect.x = 450
    screen.blit(string_rendered, intro_rect)
    time_level += 1
    pygame.display.flip()
    clock.tick(60)
finish_screen(status, time_level // 60)
pygame.quit()
