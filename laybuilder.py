import numpy as np
import os
import pygame
import ast

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
YELLANGE = (255, 192, 0)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 225)
LIGHT_BLUE = (135, 208, 250)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
GREEN = (64, 255, 64)
LIGHT_GREEN = (128, 255, 128)
BLACK = (0, 0, 0)
BROWN = (96, 38, 0)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
PURPLE = (128, 0, 128)
PINK = (255, 20, 147)
PEACH = (240, 128, 128)
RASPBERRY = (220, 20, 60)
TURQUOISE = (0, 128, 128)
COLORS = [WHITE, RASPBERRY, RED, YELLOW, YELLANGE, ORANGE, LIGHT_GREEN, GREEN, TURQUOISE, LIGHT_BLUE, BLUE, GREY, DARK_GREY, BROWN, PEACH, PINK, PURPLE]

FULL_WINDOW = 1920, 1080
FPS = 60
filename = 'test5'
INTERFACE_CORDS = FULL_WINDOW[0] - 760, 100
GAP_BTW_LINES = 42
MAP_SIZE = [20, 20, 20]  # Y, Z, X
TILE_SIZE = min([FULL_WINDOW[1]//MAP_SIZE[1], FULL_WINDOW[0]//MAP_SIZE[2]])
MAP_Y_OFFSET = (FULL_WINDOW[1] - TILE_SIZE * MAP_SIZE[1]) // 2

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)
font24 = pygame.font.SysFont('calibri', 24)
bck = pygame.transform.scale(pygame.image.load('bck.png').convert_alpha(), FULL_WINDOW)
interface = True
settings = False
grid = True
ghost = True
active_text_field = None
text_fields = [[220, 20, 500, 40, filename, 'Имя файла:', 60, 25],
               [220, 20+GAP_BTW_LINES, 55, 40, str(MAP_SIZE[2]), 'X', 185, 25+GAP_BTW_LINES],
               [220, 20+GAP_BTW_LINES*2, 55, 40, str(MAP_SIZE[1]), 'Z', 185, 25+GAP_BTW_LINES*2],
               [220, 20+GAP_BTW_LINES*3, 55, 40, str(MAP_SIZE[0]), 'Y', 185, 25+GAP_BTW_LINES*3]]
cur_colors = []
cur_color = COLORS[0]
counts = []
toggleoff = font.render('ВЫКЛ', True, RED)
toggleon = font.render('ВКЛ', True, GREEN)
cl = 0
ticks = 0
tilemap = np.zeros(MAP_SIZE, 'int')


def load():
    if filename+'.npy' not in os.listdir('.'):
        return
    global tilemap
    global text_fields
    global MAP_SIZE
    global TILE_SIZE
    global MAP_Y_OFFSET
    global counts
    global cur_colors
    tilemap = np.load(filename+'.npy')
    MAP_SIZE = list(tilemap.shape)
    TILE_SIZE = min([FULL_WINDOW[1] // MAP_SIZE[1], INTERFACE_CORDS[0] // MAP_SIZE[2]])
    MAP_Y_OFFSET = (FULL_WINDOW[1] - TILE_SIZE * MAP_SIZE[1]) // 2
    text_fields = [[220, 20, 500, 40, filename, 'Имя файла:', 60, 25],
                   [220, 20 + GAP_BTW_LINES, 55, 40, str(MAP_SIZE[2]), 'X', 185, 25 + GAP_BTW_LINES],
                   [220, 20 + GAP_BTW_LINES * 2, 55, 40, str(MAP_SIZE[1]), 'Z', 185, 25 + GAP_BTW_LINES * 2],
                   [220, 20 + GAP_BTW_LINES * 3, 55, 40, str(MAP_SIZE[0]), 'Y', 185, 25 + GAP_BTW_LINES * 3]]
    if filename + '.txt' in os.listdir('.'):
        data = ast.literal_eval(open(filename + '.txt', 'r', encoding='utf-8').read())
        counts = []
        cur_colors = []
        for i in data['blocks']:
            cur_colors.append(COLORS[i['index']])
            text_fields.append([220, text_fields[-1][1] + GAP_BTW_LINES, 500, 40, i['block'], '', 176,
                                text_fields[-1][7] + GAP_BTW_LINES])
            counts.append(i['count'])


def clamp(i, mn, mx):
    return max(mn, (min(i, mx)))


def valid_tpos(pos):
    if not -1 < pos[0] < MAP_SIZE[1]:
        return False
    if not -1 < pos[1] < MAP_SIZE[2]:
        return False
    return True


def apply_text():
    idx = active_text_field
    if idx == 0:
        global filename
        filename = text_fields[idx][4]
    elif idx == 1:
        if text_fields[idx][4].isdigit():
            change_size(int(text_fields[idx][4]), 2)
    elif idx == 2:
        if text_fields[idx][4].isdigit():
            change_size(int(text_fields[idx][4]), 1)
    elif idx == 3:
        if text_fields[idx][4].isdigit():
            change_size(int(text_fields[idx][4]), 0)


def change_size(new, axis):
    if new < 1:
        return
    global tilemap
    global TILE_SIZE
    global MAP_Y_OFFSET
    global cl
    diff = new - MAP_SIZE[axis]
    if diff > 0:
        if axis == 0:
            tilemap = np.concatenate((tilemap, np.zeros((diff, MAP_SIZE[1], MAP_SIZE[2]), 'int')), axis=axis)
        if axis == 1:
            tilemap = np.concatenate((tilemap, np.zeros((MAP_SIZE[0], diff, MAP_SIZE[2]), 'int')), axis=axis)
        if axis == 2:
            tilemap = np.concatenate((tilemap, np.zeros((MAP_SIZE[0], MAP_SIZE[1], diff), 'int')), axis=axis)
    while diff < 0:
        tilemap = np.delete(tilemap, -1, axis=axis)
        diff += 1
    MAP_SIZE[axis] = new
    TILE_SIZE = min([FULL_WINDOW[1] // MAP_SIZE[1], INTERFACE_CORDS[0] // MAP_SIZE[2]])
    MAP_Y_OFFSET = (FULL_WINDOW[1] - TILE_SIZE * MAP_SIZE[1]) // 2
    if axis == 0 and cl >= MAP_SIZE[axis]:
        cl = MAP_SIZE[axis] - 1


def cut_flip_rotate():
    ta = np.copy(tilemap)
    for i in range(3):
        if i:
            ta = np.rot90(ta, axes=(0, i))
        while not np.any(ta[0]):
            ta = np.delete(ta, 0, axis=0)
        while not np.any(ta[-1]):
            ta = np.delete(ta, -1, axis=0)
        if i:
            ta = np.rot90(ta, axes=(i, 0))
    ta = np.rot90(ta, k=3, axes=(1, 2))
    return [ta.tolist()] + list(ta.shape)


def save():
    file = open(filename+'.txt', 'w', encoding='utf-8')
    data = {'blocks': [{'index': i, 'block': d[4], 'count': counts[i]} for i, d in enumerate(text_fields[4:])]}
    file.write(str(data))
    file.close()
    file = open(filename+'.lua', 'w', encoding='utf-8')
    tilemap_array, y, z, x = cut_flip_rotate()
    file.write('\n'.join([f'y = {y}', f'z = {z}', f'x = {x}',
                          'data = '+str(tilemap_array).replace('[', '{').replace(']', '}'),
                          'blocks = '+str([d[4] for d in text_fields[4:]]).replace('[', '{').replace(']', '}')]))
    file.write('\n\n')
    luacode = open('code.lua', 'r', encoding='utf-8').read()
    file.write(luacode)
    file.close()


def count_resources():
    data = {i: 0 for i, d in enumerate(text_fields[4:])}
    for y in range(MAP_SIZE[0]):
        for i in range(MAP_SIZE[1]):
            for j in range(MAP_SIZE[2]):
                if tilemap[y][i][j]:
                    data[tilemap[y][i][j] - 1] += 1
    return data


load()
while True:
    sc.fill(WHITE)
    sc_ghost = pygame.Surface(FULL_WINDOW, pygame.SRCALPHA, 32)
    pos = pygame.mouse.get_pos()
    tpos = (pos[1]-MAP_Y_OFFSET)//TILE_SIZE, pos[0]//TILE_SIZE
    pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    ticks += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if active_text_field is not None and not settings:
                if event.key == pygame.K_BACKSPACE:
                    text_fields[active_text_field][4] = text_fields[active_text_field][4][:-1]
                else:
                    text_fields[active_text_field][4] += event.unicode
            else:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_g:
                    grid = not grid
                if event.key == pygame.K_j:
                    ghost = not ghost
                if event.key == pygame.K_h:
                    interface = not interface
                if event.key == pygame.K_b:
                    np.save(filename, tilemap)
                    save()
                if event.key == pygame.K_v:
                    settings = not settings
                if event.key == pygame.K_p:
                    tilemap = np.zeros(MAP_SIZE, 'int')
                if event.key == pygame.K_a:
                    cl = clamp(cl-1, 0, MAP_SIZE[0]-1)
                if event.key == pygame.K_d:
                    cl = clamp(cl+1, 0, MAP_SIZE[0]-1)
                if event.key == pygame.K_q:
                    cur_color = COLORS[clamp(COLORS.index(cur_color)-1, 0, len(COLORS)-1)]
                if event.key == pygame.K_e:
                    cur_color = COLORS[clamp(COLORS.index(cur_color)+1, 0, len(COLORS)-1)]
        if event.type == pygame.MOUSEBUTTONDOWN and not settings:
            if active_text_field is not None:
                apply_text()
                active_text_field = None
            for i in text_fields:
                if INTERFACE_CORDS[0]+i[0] < pos[0] < INTERFACE_CORDS[0]+i[0]+i[2] and INTERFACE_CORDS[1]+i[1] < pos[1] < INTERFACE_CORDS[1]+i[1]+i[3]:
                    active_text_field = text_fields.index(i)
            lbs = (INTERFACE_CORDS[0]+text_fields[0][0]+410, INTERFACE_CORDS[1]+text_fields[0][1], 90, text_fields[0][3])  # load button sizes
            if lbs[0] < pos[0] < lbs[0]+lbs[2] and lbs[1] < pos[1] < lbs[1]+lbs[3]:
                load()

    if not settings and valid_tpos(tpos):
        if pressed[0]:
            tilemap[cl][tpos[0]][tpos[1]] = COLORS.index(cur_color)+1
            if cur_color not in cur_colors:
                cur_colors.append(cur_color)
                text_fields.append([220, text_fields[-1][1]+GAP_BTW_LINES, 500, 40, '', '', 176, text_fields[-1][7]+GAP_BTW_LINES])
        if pressed[2]:
            tilemap[cl][tpos[0]][tpos[1]] = 0

    if ticks % 60 == 0:
        counts = count_resources()
        counts = [counts[i] for i, d in enumerate(text_fields[4:])]

    sc.blit(bck, (0, 0))

    if grid:
        for i in range(0, MAP_SIZE[1]+1):
            pygame.draw.aaline(sc, DARK_GREY, (0, MAP_Y_OFFSET+i*TILE_SIZE), (TILE_SIZE*MAP_SIZE[2], MAP_Y_OFFSET+i*TILE_SIZE))
        for i in range(1, MAP_SIZE[2]+1):
            pygame.draw.aaline(sc, DARK_GREY, (i*TILE_SIZE, MAP_Y_OFFSET), (i*TILE_SIZE, MAP_Y_OFFSET+TILE_SIZE*MAP_SIZE[1]))

    for i in range(MAP_SIZE[1]):
        for j in range(MAP_SIZE[2]):
            if tilemap[cl][i][j]:
                pygame.draw.rect(sc, COLORS[tilemap[cl][i][j]-1], (j*TILE_SIZE+1, MAP_Y_OFFSET+i*TILE_SIZE+1, TILE_SIZE-1, TILE_SIZE-1))
            if ghost and cl > 0 and tilemap[cl-1][i][j]:
                pygame.draw.rect(sc_ghost, COLORS[tilemap[cl-1][i][j] - 1], (j * TILE_SIZE + 1, MAP_Y_OFFSET+i * TILE_SIZE + 1, TILE_SIZE - 1, TILE_SIZE - 1))
    if ghost and cl > 0:
        sc_ghost.set_alpha(128)
        sc.blit(sc_ghost, (0, 0))

    if interface:
        sc.blit(font.render(str(tpos), True, WHITE), (FULL_WINDOW[0] - 160, 10))
        sc.blit(font.render(str(int(clock.get_fps())), True, WHITE), (FULL_WINDOW[0] - 50, 10))
        sc.blit(font.render('Help: [V]', True, WHITE), (FULL_WINDOW[0] - 125, 50))

    for i in text_fields:
        pygame.draw.rect(sc, WHITE, (INTERFACE_CORDS[0]+i[0], INTERFACE_CORDS[1]+i[1], i[2], i[3]))
        pygame.draw.rect(sc, BLACK, (INTERFACE_CORDS[0]+i[0], INTERFACE_CORDS[1]+i[1], i[2], i[3]), 3)
        if i[5]:
            sc.blit(font.render(i[5], True, WHITE), (INTERFACE_CORDS[0]+i[6], INTERFACE_CORDS[1]+i[7]))
        else:
            sc.blit(font.render(str(counts[text_fields.index(i)-4]), True, GREEN), (INTERFACE_CORDS[0] + i[6] - 13 - (12*len(str(counts[text_fields.index(i)-4]))), INTERFACE_CORDS[1] + i[7]))
            pygame.draw.rect(sc, cur_colors[text_fields.index(i)-4], (INTERFACE_CORDS[0]+i[6], INTERFACE_CORDS[1]+i[7], 30, 30))
        sc.blit(font.render(i[4], True, BLACK), (INTERFACE_CORDS[0]+i[0]+5, INTERFACE_CORDS[1]+i[1]+5))
    pygame.draw.rect(sc, GREEN, (INTERFACE_CORDS[0]+text_fields[0][0]+410, INTERFACE_CORDS[1]+text_fields[0][1], 90, text_fields[0][3]))
    pygame.draw.rect(sc, BLACK, (INTERFACE_CORDS[0]+text_fields[0][0]+410, INTERFACE_CORDS[1]+text_fields[0][1], 90, text_fields[0][3]), 3)
    sc.blit(font.render('Load', True, BLACK), (INTERFACE_CORDS[0]+text_fields[0][0]+425, INTERFACE_CORDS[1]+text_fields[0][1]+5))

    PARAMS_BASE = FULL_WINDOW[0]-700, 15
    sc.blit(font.render('Текущий слой: [A][D]', True, WHITE), (PARAMS_BASE[0], PARAMS_BASE[1]))
    sc.blit(font.render(str(cl), True, GREEN), (PARAMS_BASE[0] + 270, PARAMS_BASE[1]))
    sc.blit(font.render('Текущий цвет: [Q][E]', True, WHITE), (PARAMS_BASE[0], PARAMS_BASE[1] + 40))
    pygame.draw.rect(sc, cur_color, (PARAMS_BASE[0] + 268, PARAMS_BASE[1] + 40, 30, 30))

    if settings:
        SETTINGS_SIZE = 560, 610
        SETTINGS_CORDS = FULL_WINDOW[0]-SETTINGS_SIZE[0]-100, 400
        WRITINGS_BASE = SETTINGS_CORDS[0]+20, SETTINGS_CORDS[1]+20
        pygame.draw.rect(sc, DARK_GREY, SETTINGS_CORDS+SETTINGS_SIZE)
        pygame.draw.rect(sc, BLACK, SETTINGS_CORDS+SETTINGS_SIZE, 3)
        sc.blit(font.render('Рисовать: [ЛКМ]', True, WHITE), WRITINGS_BASE)
        sc.blit(font.render('Стирать: [ПКМ]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+40))
        sc.blit(font.render('Сетка: [G]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+120))
        sc.blit(toggleon if grid else toggleoff, (WRITINGS_BASE[0]+130, WRITINGS_BASE[1]+120))
        sc.blit(font.render('Параметры в углу: [H]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+160))
        sc.blit(toggleon if interface else toggleoff, (WRITINGS_BASE[0]+285, WRITINGS_BASE[1]+160))
        sc.blit(font.render('Призрачный режим: [J]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1] + 200))
        sc.blit(toggleon if ghost else toggleoff, (WRITINGS_BASE[0] + 305, WRITINGS_BASE[1] + 200))
        sc.blit(font.render('Сохранение: [B]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+320))
        sc.blit(font.render('Выход: [Esc]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+360))
        sc.blit(font.render('Заполнение:', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+440))
        sc.blit(font.render('Очистить: [P]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+480))

    pygame.display.flip()
    clock.tick(FPS)



