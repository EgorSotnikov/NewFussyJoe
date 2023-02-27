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
    if name == "Grass_Tile.png" or name == "Floor_Tile.png":
        return pygame.transform.scale(image, (75, 75))
    if name == "NewCow.png":
        return pygame.transform.scale(image, (180, 90))
    if name == "Cowshed.png":
        return pygame.transform.scale(image, (600, 300))
    if name == "VeryNewTable.png":
        return pygame.transform.scale(image, (200, 100))
    return image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
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
            elif level[y][x] == '/':
                Tile('grass', x, y)
                x_c, y_c = x, y
            elif level[y][x] == '^':
                Tile('grass', x, y)
                x_cs, y_cs = x, y
            elif level[y][x] == '-':
                Tile('floor', x, y)
                x_t, y_t = x, y
    # вернем игрока, корову, а также размер поля в клетках
    return Player(x_p, y_p), Cow(x_c, y_c), Cowshed(x_cs, y_cs), Table(x_t, y_t), x, y


tile_images = {
    'floor': load_image('Floor_Tile.png'),
    'grass': load_image('Grass_Tile.png')
}
cow_image = load_image('NewCow.png')
cowshed_image = load_image('Cowshed.png')
table_image = load_image('VeryNewTable.png')
player_image = load_image('mar.png')

player = None
tile_width = tile_height = 75
tiles_group = pygame.sprite.Group()
cow_group = pygame.sprite.Group()
cowshed_group = pygame.sprite.Group()
table_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
            tile_width * pos_x - 35, tile_height * pos_y + 35)

    def ani(self, *args):
        if self.iter % 300 == 0:
            self.rect.x -= 0.05 * self.size_x
            self.rect.y -= 0.1 * self.size_y
            self.size_x *= 1.1
            self.size_y *= 1.1
            self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        self.iter += 1


class Cowshed(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cowshed_group, all_sprites)
        self.image = cowshed_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Table(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(table_group, all_sprites)
        self.image = table_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 35)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

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


player, cow, cowshed, table, level_x, level_y = generate_level(load_level('level.txt'))
running = True
clock = pygame.time.Clock()
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(event)
    cow.ani()
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
