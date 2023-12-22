import pygame, os, sys
import pygame_menu
import sqlite3
from pygame_menu import Theme, Menu

pygame.init()
pygame.display.set_caption('The Labyrinth of Jupiter')

value = 15
size = WIDTH, HEIGHT = 1200, 650
screen = pygame.display.set_mode(size)
start_sprite = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
IS_PAUSED = False
Is_Jump = False
CLOCK = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load('data/sounds/intro.wav')


def update_data_bd(id, name_row, new_value):
    # Подключение к БД
    con = sqlite3.connect('data/bd/bd_for_game.db')
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    if name_row == 'Cord_person':
        cur.execute("""UPDATE GameBD
        Set Cord_person = ?
        where id = ?""", (new_value, id))
        con.commit()
    if name_row == 'Cord_Up_line':
        cur.execute("""UPDATE GameBD
        Set Cord_Up_line = ?
        where id = ?""", (new_value, id))
        con.commit()
    if name_row == 'Cord_Down_line':
        cur.execute("""UPDATE GameBD
        Set Cord_Down_line = ?
        where id = ?""", (new_value, id))
        con.commit()
    if name_row == 'Cord_Right_line':
        cur.execute("""UPDATE GameBD
        Set Cord_Right_line = ?
        where id = ?""", (new_value, id))
        con.commit()
    if name_row == 'Cord_Left_line':
        cur.execute("""UPDATE GameBD
        Set Cord_Left_line = ?
        where id = ?""", (new_value, id))
        con.commit()
    if name_row == 'Count_level':
        cur.execute("""UPDATE GameBD
        Set Count_level = ?
        where id = ?""", (new_value, id))
        con.commit()
    con.close()


def get_data_bd(id, name_row):
    # Подключение к БД
    con = sqlite3.connect('data/bd/bd_for_game.db')
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    tmp_result = cur.execute(f"""SELECT {name_row} FROM GameBD
    WHERE id = {id}""")
    result = ''
    count = 0
    for i in tmp_result:
        count += 1
        if count == 1:
            result = i
    result = result[0].split(', ')
    con.close()
    return result


def load_check_game(id=3):
    # синхронизация 1 и id индекса БД
    update_data_bd(1, 'Cord_person', ', '.join(get_data_bd(id, 'Cord_person')))
    update_data_bd(1, 'Cord_Up_line', ', '.join(get_data_bd(id, 'Cord_Up_line')))
    update_data_bd(1, 'Cord_Down_line', ', '.join(get_data_bd(id, 'Cord_Down_line')))
    update_data_bd(1, 'Cord_Right_line', ', '.join(get_data_bd(id, 'Cord_Right_line')))
    update_data_bd(1, 'Cord_Left_line', ', '.join(get_data_bd(id, 'Cord_Left_line')))


def load_image(name, colorkey=None):
    fullname = os.path.join('data/image', name)
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
    return image


def clearLvL():
    if walls and walls:
        walls.mask.clear()
        walls.image.set_alpha(0)
    if traps and traps:
        traps.mask.clear()
        traps.image.set_alpha(0)
    if details and details:
        details.mask.clear()
        details.image.set_alpha(0)
    if end and end:
        end.mask.clear()
        end.image.set_alpha(0)
    if check_point and check_point.mask:
        check_point.mask.clear()
        check_point.image.set_alpha(0)


class Walls(pygame.sprite.Sprite):
    def __init__(self, lvl=1):
        if lvl == 1:
            image1 = load_image("wals_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        else:
            image1 = load_image("wals2_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем стены
        self.rect.bottom = HEIGHT


class Background(pygame.sprite.Sprite):
    image1 = load_image("background_for game.png")
    image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем фон
        self.rect.bottom = HEIGHT


class Teleport(pygame.sprite.Sprite):
    def __init__(self):
        image1 = load_image("teleport_for game.png")
        self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем фон
        self.rect.bottom = HEIGHT


class CheckPoint(pygame.sprite.Sprite):
    image1 = load_image("check_point1_for game.png")
    image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = CheckPoint.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем чекпоинт
        self.rect.bottom = HEIGHT


class End_level(pygame.sprite.Sprite):
    def __init__(self, lvl=1):
        if lvl == 1:
            image1 = load_image("exit_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        else:
            image1 = load_image("exit2_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем чекпоинт
        self.rect.bottom = HEIGHT


class Details(pygame.sprite.Sprite):
    def __init__(self, lvl=1):
        if lvl == 1:
            image1 = load_image("details_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        else:
            image1 = load_image("details2_for game.png")
            print(1)
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем детали
        self.rect.bottom = HEIGHT


class Traps(pygame.sprite.Sprite):

    def __init__(self, lvl=1):
        if lvl == 1:
            image1 = load_image("traps_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        else:
            image1 = load_image("traps2_for game.png")
            self.image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = HEIGHT


class Start(pygame.sprite.Sprite):
    image1 = load_image("start.png")
    image = pygame.transform.scale(image1, (screen.get_width(), screen.get_height()))

    def __init__(self, *group):
        super().__init__(start_sprite)
        self.image = Start.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = screen.get_width()

    def update(self, v):
        if self.rect.y > 0:
            self.rect.y = screen.get_height() - v


class Down(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("up_down_line.png"), (30, 5))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 130
        self.rect.y = 626


class Up(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("up_down_line.png"), (35, 5))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 125
        self.rect.y = 532


class Borders(pygame.sprite.Sprite):
    def __init__(self, img, n):
        super().__init__(all_sprites)
        if n == 1:
            self.add(vertical_borders)
            self.image = img
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = 110
            self.rect.y = 550
        elif n == 2:
            self.add(horizontal_borders)
            self.image = img
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = 170
            self.rect.y = 550


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, walls, trap, down, up, left, right, exit_lvl, check=0, teleport=0,):
        super().__init__(hero_sprite)
        self.jump_now = False
        self.all_col = [down, up, left, right]
        self.walls = walls
        self.trap = trap
        self.teleport = teleport
        self.check = check
        self.exit_lvl = exit_lvl
        self.jumpCount = 8
        self.all_anim = []
        self.all_mask = []
        self.n = 0
        self.fps_1 = 0
        self.fps_2 = 0
        self.sheet = sheet
        self.sheet_fps()
        self.cur_frame = 0
        self.image = self.all_anim[0][self.cur_frame]

    def sheet_fps(self):
        for i in range(len(self.sheet)):
            self.frames = []
            self.masks = []
            if i == 0:
                self.cut_sheet(self.sheet[i], 4, 1)
            if i == 1:
                self.cut_sheet(self.sheet[i], 8, 1)
            if i == 2:
                self.cut_sheet(self.sheet[i], 8, 1, 1)
            if i == 3:
                self.cut_sheet(self.sheet[i], 5, 1)
            if i == 4:
                self.cut_sheet(self.sheet[i], 5, 1, 1)
            if i == 5:
                self.cut_sheet(self.sheet[i], 2, 1)
            self.rect.x, self.rect.y = 100, 529
            self.all_anim.append(self.frames)
            self.all_mask.append(self.masks)

    def cut_sheet(self, sheet, columns, rows, rev=0):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                sh = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                self.frames.append(sh)
                self.masks.append(pygame.mask.from_surface(sh))
        if rev:
            self.frames = self.frames[::-1]
            self.masks = self.masks[::-1]

    def update(self, *args):
        global IS_PAUSED
        global Is_Jump
        keystate = pygame.key.get_pressed()
        collide = [pygame.sprite.collide_mask(self.walls, self.all_col[0]),
                   pygame.sprite.collide_mask(self.walls, self.all_col[1]),
                   pygame.sprite.collide_mask(self.walls, self.all_col[2]),
                   pygame.sprite.collide_mask(self.walls, self.all_col[3])]
        if set(collide[1:]) and (collide[0] is not None):
            self.n = 0
        if keystate[pygame.K_SPACE] and keystate[pygame.K_a] and Is_Jump:
            self.n = 4
            self.cur_frame = 0
        if keystate[pygame.K_SPACE] and (keystate[pygame.K_d] or not keystate[pygame.K_d]) and Is_Jump:
            self.cur_frame = 0
            self.n = 3
        if self.jump_now:
            self.n = 5
            self.cur_frame = 0
        if keystate[pygame.K_d] and not Is_Jump:
            self.n = 1
        if keystate[pygame.K_a] and not Is_Jump:
            self.n = 2
        if self.fps_1 == 6:
            if self.n == 3 or self.n == 4:
                self.animation()
            self.fps_1 = 0
        if self.fps_2 == 4:
            if self.n == 0 or self.n == 1 or self.n == 2:
                self.animation()
            self.fps_2 = 0

        self.fps_1 += 1
        self.fps_2 += 1

    def animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.all_anim[self.n])
        self.image = self.all_anim[self.n][self.cur_frame]

    def plus_col(self, cords, pl, q):
        if q == 'x':
            if pl == '+':
                for i in self.all_col:
                    i.rect.x += cords
            elif pl == '-':
                for i in self.all_col:
                    i.rect.x -= cords
        elif q == 'y':
            if pl == '+':
                for i in self.all_col:
                    i.rect.y += cords
            elif pl == '-':
                for i in self.all_col:
                    i.rect.y -= cords

    def move(self):
        global Is_Jump
        boost = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            boost = 7
        if keystate[pygame.K_a] and not pygame.sprite.collide_mask(self.walls, self.all_col[2]):
            self.rect.x -= (7 + boost)
            self.plus_col(7 + boost, '-', 'x')
        if keystate[pygame.K_d] and not pygame.sprite.collide_mask(self.walls, self.all_col[-1]):
            self.rect.x += (7 + boost)
            self.plus_col(7 + boost, '+', 'x')
        if pygame.sprite.collide_mask(self, self.trap):
            die_menu()
        if self.check and pygame.sprite.collide_mask(self, self.check):
            load_check_game(3)
        if self.teleport and pygame.sprite.collide_mask(self, self.teleport):
            teleporter()

        if pygame.sprite.collide_mask(self, self.exit_lvl):
            clearLvL()
            if get_data_bd(1, 'Count_level')[0] == '1':
                load_level_2()
            elif get_data_bd(1, 'Count_level')[0] == '2':
                win_menu()
        if not pygame.sprite.collide_mask(self.walls, self.all_col[0]):
            if self.all_col[0].rect.y < 630 and not Is_Jump:
                self.jump_now = True
                self.rect.y += 17
                self.plus_col(17, '+', 'y')
        else:
            self.jump_now = False

    def jump(self):
        global Is_Jump
        if Is_Jump and not self.jump_now:
            if self.jumpCount >= -4:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                if not pygame.sprite.collide_mask(self.walls, self.all_col[1]):
                    self.rect.y -= self.jumpCount ** 2 * neg
                    self.plus_col(self.jumpCount ** 2 * neg, '-', 'y')
                self.jumpCount -= 3
            else:
                Is_Jump = False
                self.jump_now = True
                self.jumpCount = 8
        else:
            Is_Jump = False


def terminate():
    pygame.quit()
    sys.exit()


def flip(fps):
    global CLOCK
    CLOCK.tick(fps)
    pygame.display.flip()


image = pygame.transform.scale(load_image("hero1.png"), (400, 100))
all = [image,
        pygame.transform.scale(load_image("hero_run1.png"), (800, 100)),
        pygame.transform.scale(pygame.transform.flip(load_image("hero_run1.png"), True, False), (800, 100)),
        pygame.transform.scale(load_image("hero_jump1.png"), (560, 115)),
        pygame.transform.scale(pygame.transform.flip(load_image("hero_jump1.png"), True, False), (560, 115)),
        load_image("hero_falls.png")]

down = Down()
up = Up()
left = Borders(pygame.transform.scale(load_image("left_right_line.png"), (5, 60)), 1)
right = Borders(pygame.transform.scale(load_image("left_right_line.png"), (5, 60)), 2)
background = Background()
check_point = 0
teleport = 0

if get_data_bd(1, 'Count_level')[0] == '1':
    end = End_level()
    details = Details()
    traps = Traps()
    check_point = CheckPoint()
    walls = Walls()
    hero = Hero(all, walls, traps, down, up, left, right, end, check=check_point)
if get_data_bd(1, 'Count_level')[0] == '2':
    end = End_level(2)
    details = Details(2)
    traps = Traps(2)
    teleport = Teleport()
    walls = Walls(2)
    hero = Hero(all, walls, traps, down, up, left, right, end, teleport=teleport)


def game():
    global IS_PAUSED
    global Is_Jump
    FPS = 42
    jupiter = load_image("jupiter1.jpg")
    fon = pygame.transform.scale(jupiter, (screen.get_width(), screen.get_height()))
    game_menu.disable()
    event = 0

    while True:
        events = pygame.event.get()
        if down.rect.y > 626:
            down.rect.y = 626
            up.rect.y = 532
            left.rect.y = 550
            right.rect.y = 550
            hero.rect.y = 529
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    IS_PAUSED = not IS_PAUSED
                    if game_menu.is_enabled():
                        game_menu.disable()
                    else:
                        game_menu.enable()
                if event.key == pygame.K_SPACE:
                    Is_Jump = not Is_Jump
        screen.fill('white')
        if not IS_PAUSED:
            all_sprites.draw(screen)
            all_sprites.update(event)
            hero_sprite.draw(screen)
            hero_sprite.update(event)
            hero.move()
            hero.jump()
            flip(FPS)
        if game_menu.is_enabled():
            screen.blit(fon, (0, 0))
            game_menu.update(events)
            game_menu.draw(screen)
            flip(FPS)


def start_screen():
    x_pos = 0
    v = 800
    Start(start_sprite)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    running = False
        screen.fill('black')
        x_pos += v * CLOCK.tick() / 1000
        start_sprite.update(x_pos)
        start_sprite.draw(screen)
        flip(60)
    main_menu()


def main_menu():
    global menu
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.15)
    running = True
    jupiter = load_image("jupiter1.jpg")
    fon = pygame.transform.scale(jupiter, (screen.get_width(), screen.get_height()))
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        menu.update(events)
        menu.draw(screen)
        flip(20)


def die_menu():
    global d_menu
    running = True
    died = load_image("died.png")
    fon = pygame.transform.scale(died, (screen.get_width(), screen.get_height()))
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        d_menu.update(events)
        d_menu.draw(screen)
        flip(20)


def win_menu():
    global w_menu
    running = True
    win = load_image("win.png")
    fon = pygame.transform.scale(win, (screen.get_width(), screen.get_height()))
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        w_menu.update(events)
        w_menu.draw(screen)
        flip(20)


def volume_change(val):
    if val >= 0:
        pygame.mixer.music.set_volume(val / 100)


def last_position(id=1):
    tmp = get_data_bd(id, 'Cord_person')
    hero.rect.x, hero.rect.y = int(tmp[0]), int(tmp[1])

    tmp = get_data_bd(id, 'Cord_Up_line')
    up.rect.x, up.rect.y = int(tmp[0]), int(tmp[1])

    tmp = get_data_bd(id, 'Cord_Down_line')
    down.rect.x, down.rect.y = int(tmp[0]), int(tmp[1])

    tmp = get_data_bd(id, 'Cord_Left_line')
    left.rect.x, left.rect.y = int(tmp[0]), int(tmp[1])

    tmp = get_data_bd(id, 'Cord_Right_line')
    right.rect.x, right.rect.y = int(tmp[0]), int(tmp[1])
    game()


def teleporter():
    if get_data_bd(1, 'Count_level')[0] == '2':
        hero.rect.x, hero.rect.y = int(get_data_bd(5, 'Cord_person')[0]), int(get_data_bd(5, 'Cord_person')[1])

        up.rect.x, up.rect.y = int(get_data_bd(5, 'Cord_Up_line')[0]), int(get_data_bd(5, 'Cord_Up_line')[1])

        down.rect.x, down.rect.y = int(get_data_bd(5, 'Cord_Down_line')[0]), int(get_data_bd(5, 'Cord_Down_line')[1])

        left.rect.x, left.rect.y = int(get_data_bd(5, 'Cord_Left_line')[0]), int(get_data_bd(5, 'Cord_Left_line')[1])

        right.rect.x, right.rect.y = int(get_data_bd(5, 'Cord_Right_line')[0]),\
                                     int(get_data_bd(5, 'Cord_Right_line')[1])


def start_new_game(id=2):
    global walls, traps, details, end, teleport, check_point
    # синхронизация 1 и id индекса БД
    update_data_bd(1, 'Cord_person', ', '.join(get_data_bd(id, 'Cord_person')))
    update_data_bd(1, 'Cord_Up_line', ', '.join(get_data_bd(id, 'Cord_Up_line')))
    update_data_bd(1, 'Cord_Down_line', ', '.join(get_data_bd(id, 'Cord_Down_line')))
    update_data_bd(1, 'Cord_Right_line', ', '.join(get_data_bd(id, 'Cord_Right_line')))
    update_data_bd(1, 'Cord_Left_line', ', '.join(get_data_bd(id, 'Cord_Left_line')))
    update_data_bd(1, 'Count_level', ', '.join(get_data_bd(id, 'Count_level')))

    background = Background()
    end = End_level()
    details = Details()
    traps = Traps()
    check_point = CheckPoint()
    walls = Walls()
    if hero:
        hero.walls = walls
        hero.trap = traps
        hero.check = check_point
        hero.exit_lvl = end
    # перемещение персонажа на нужные координаты
    last_position()


def load_level_2(id=4):
    # создание новой карты(рисование недостающих объектов)
    update_data_bd(1, 'Cord_person', ', '.join(get_data_bd(id, 'Cord_person')))
    update_data_bd(1, 'Cord_Up_line', ', '.join(get_data_bd(id, 'Cord_Up_line')))
    update_data_bd(1, 'Cord_Down_line', ', '.join(get_data_bd(id, 'Cord_Down_line')))
    update_data_bd(1, 'Cord_Right_line', ', '.join(get_data_bd(id, 'Cord_Right_line')))
    update_data_bd(1, 'Cord_Left_line', ', '.join(get_data_bd(id, 'Cord_Left_line')))
    update_data_bd(1, 'Count_level', ', '.join(get_data_bd(id, 'Count_level')))
    hero.rect.x, hero.rect.y = int(get_data_bd(id, 'Cord_person')[0]), \
                               int(get_data_bd(id, 'Cord_person')[1])
    up.rect.x, up.rect.y = int(get_data_bd(id, 'Cord_Up_line')[0]), \
                           int(get_data_bd(id, 'Cord_Up_line')[1])
    down.rect.x, down.rect.y = int(get_data_bd(id, 'Cord_Down_line')[0]), \
                               int(get_data_bd(id, 'Cord_Down_line')[1])
    left.rect.x, left.rect.y = int(get_data_bd(id, 'Cord_Right_line')[0]), \
                               int(get_data_bd(id, 'Cord_Right_line')[1])
    right.rect.x, right.rect.y = int(get_data_bd(id, 'Cord_Left_line')[0]), \
                                 int(get_data_bd(id, 'Cord_Left_line')[1])

    end = End_level(2)
    details = Details(2)
    traps = Traps(2)
    teleport = Teleport()
    walls = Walls(2)
    hero.teleport = teleport
    hero.exit_lvl = end
    hero.walls = walls
    hero.trap = traps



font = pygame_menu.font.FONT_8BIT
mytheme = Theme(background_color=(36, 36, 36),
                selection_color=(0, 255, 10),
                title_background_color=(0, 100, 0),
                title_font_shadow=False,
                widget_padding=25,
                widget_font=font)
game_menu = Menu(height=400,
                 title='Pause',
                 width=600,
                 theme=mytheme)
game_menu.add.text_input('Volume ', input_type=pygame_menu.locals.INPUT_INT, default=value,
                         maxchar=2, onreturn=volume_change)
game_menu.add.button('Quit the game', pygame_menu.events.EXIT)

menu = Menu(height=400,
            title='MENU',
            width=600,
            theme=mytheme)
menu.add.button('Start new game', start_new_game)
menu.add.button('Last checkpoint', last_position)
menu.add.button('Quit the game', pygame_menu.events.EXIT)

mytheme2 = Theme(background_color=(83, 55, 122),
                 selection_color=(255, 165, 0),
                 title_background_color=(255, 165, 0),
                 widget_font_color=(255, 255, 255),
                 title_font_shadow=False,
                 widget_padding=25,
                 widget_font=font)
d_menu = Menu(height=400,
              title='Checkpoints',
              width=600,
              theme=mytheme2)
d_menu.add.button('Last checkpoint', last_position)
d_menu.add.button('Quit the game', pygame_menu.events.EXIT)

mytheme3 = Theme(background_color=(53, 94, 59),
                 selection_color=(24, 167, 181),
                 title_background_color=(24, 167, 181),
                 widget_font_color=(255, 165, 0),
                 title_font_shadow=False,
                 widget_padding=25,
                 widget_font=font)
w_menu = Menu(height=400,
              title='',
              width=600,
              theme=mytheme3)
# отключено по тех. причинам
# w_menu.add.button('Start new game', start_new_game)
w_menu.add.button('Quit the game', pygame_menu.events.EXIT)

start_screen()