import copy
import pygame
import random
from numpy import np

WIDTH = 1500
HEIGHT = 1000
FPS = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test GoL")


def draw_cells(cells, paused):
    if not paused:
        color = (255, 255, 255)
    else:
        color = (250, 250, 200)
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            if cells[i][j] == 1:
                x = i*10
                y = j*10
                pygame.draw.rect(WIN, color, (x, y, 10, 10))


def draw_data(data,step):
    for i in range(len(data)):
        for j in range(len(data[0])):
            val = 255*(data[i][j]/step)
            color = (val,val,val)
            x = i*10
            y = j*10
            pygame.draw.rect(WIN, color, (x, y, 10, 10))


def draw_fdata(fdata,step):
    for i in range(len(fdata)):
        for j in range(len(fdata[0])):
            val = 255*(fdata[i][j]/step)
            color = (val,val,val)
            x = i*10
            y = j*10
            pygame.draw.rect(WIN, color, (x, y, 10, 10))


def draw_grid(paused):
    if not paused:
        color = (0, 0, 0)
    else:
        color = (50, 50, 100)
    for i in range(HEIGHT//10):
        pygame.draw.line(WIN, color, (0, i*10), (WIDTH, i*10))
    for i in range(WIDTH//10):
        pygame.draw.line(WIN, color, (i*10, 0), (i*10, HEIGHT))


def add_cell(x, y, cells, click, right_click):
    if click:
        cells[x//10][y//10] = 1
    elif right_click:
        cells[x // 10][y // 10] = 0
    return cells


def count_alive(cells, x, y):
    return cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1]


def update_cells(cells,num_type,data,fdata):
    new_cells = copy.deepcopy(cells)
    data = copy.deepcopy(data)
    fdata = copy.deepcopy(fdata)
    for i in range(0, len(cells)-1):
        for j in range(0, len(cells[0])-1):
            alive = count_alive(cells, i, j)
            if num_type[alive] == 1:
                new_cells[i][j] = 0
            elif num_type[alive] ==2:
                new_cells[i][j] = 1
            data[i][j]+= cells[i][j]
            if new_cells[i][j] != cells[i][j]:
                fdata[i][j]+=1
    return new_cells, data, fdata


def update(x, y, cells, paused, click, right_click,num_type,analyse,data, step,frequency,fdata):
    if click or right_click:
        cells = add_cell(x, y, cells, click, right_click)

    if not paused:
        cells, data,fdata = update_cells(cells, num_type, data,fdata)

        if analyse and not paused:
            draw_data(data,step)

        elif frequency and not paused:
            draw_fdata(fdata,step)

        else:
            WIN.fill((0, 0, 0))
            draw_cells(cells, paused)
            draw_grid(paused)

    else:
        WIN.fill((50, 50, 100))
        draw_cells(cells, paused)
        draw_grid(paused)
    return cells, data, fdata


def main():
    clock = pygame.time.Clock()
    run = True
    paused = False
    #random.randint(0,1)
    #cells = np.zeros(shape=(WIDTH,HEIGHT))
    #data = np.zeros(shape=(WIDTH,HEIGHT))
    #fdata = np.zeros(shape=(WIDTH,HEIGHT))
    cells = [[0 for j in range(1,(HEIGHT//10)-1)] for i in range(1,(WIDTH//10)-1)]
    data = [[0 for j in range(1,(HEIGHT//10)-1)] for i in range(1,(WIDTH//10)-1)]
    fdata = [[0 for j in range(1, (HEIGHT // 10) - 1)] for i in range(1, (WIDTH // 10) - 1)]
    click = False
    right_click = False
    num_type = []
    step = 1

    analyse = False
    frequency = False

    for i in range(0,9):
        num_type.append(random.randint(1,3))
    print(num_type)
    #num_type=[1, 1, 3, 2, 1, 1, 1, 1, 1]
    #1 die, 2 born, 3 maintain

    '''
    [3, 2, 2, 3, 1, 3, 1, 1, 2]
    [3, 2, 2, 3, 3, 1, 3, 1, 1]
    check with p [1, 2, 2, 2, 2, 3, 1, 1, 1]
    #fractal [2, 2, 3, 3, 3, 3, 1, 1, 3], [3, 2, 3, 3, 1, 1, 1, 1, 3],[1, 2, 3, 1, 3, 3, 3, 2, 2]  [3, 2, 2, 3, 3, 1, 3, 1, 1]
    #psuedo random ? [3, 2, 3, 1, 2, 3, 2, 2, 3], [1, 2, 2, 1, 3, 2, 2, 3, 1]
    #[2, 2, 2, 1, 3, 3, 2, 2, 1]
    #[1, 2, 3, 1, 3, 1, 3, 3, 2]
    [2, 2, 1, 3, 3, 3, 2, 2, 1]
    [2, 1, 3, 1, 3, 3, 3, 1, 3]
    # land generator [3, 3, 2, 3, 3, 2, 1, 1, 2],[3, 2, 2, 1, 3, 1, 3, 1, 3]
    #still life [3, 2, 3, 1, 3, 1, 2, 2, 3], [1, 3, 2, 3, 3, 3, 1, 1, 2], [2, 2, 2, 3, 2, 1, 1, 3, 3] [2, 1, 1, 3, 2, 2, 3, 3, 1]
    #pulsars [2, 1, 2, 3, 2, 1, 3, 2, 3], [1, 1, 2, 3, 3, 3, 1, 2, 1], [3, 3, 2, 3, 2, 1, 3, 2, 3] [2, 1, 1, 1, 2, 1, 2, 2, 3], [2, 3, 3, 3, 2, 1, 3, 2, 2]
    #cool pulsars [2, 3, 1, 1, 2, 2, 2, 2, 1] [2, 2, 2, 1, 2, 1, 1, 1, 3] [2, 1, 3, 3, 3, 1, 3, 3, 2]
    #fill function [3, 1, 3, 3, 2, 3, 3, 2, 2]
    #organic growth [3, 1, 3, 2, 3, 3, 2, 2, 2] [1, 2, 3, 1, 3, 2, 2, 3, 3] [1, 1, 1, 2, 3, 3, 3, 2, 1]
    #triangles [1, 2, 3, 2, 3, 2, 3, 1, 1]
    [3, 3, 3, 2, 3, 2, 2, 1, 3]
    #fractal growth[1, 2, 3, 3, 2, 2, 1, 1, 2], [1, 2, 3, 3, 2, 3, 2, 3, 3], [3, 2, 3, 3, 3, 2, 2, 1, 1], [1, 2, 2, 3, 2, 3, 2, 3, 1] [3, 2, 2, 3, 1, 3, 3, 3, 2]
    #fractal growth 2 [3, 2, 2, 3, 3, 1, 3, 1, 1] [1, 2, 3, 3, 2, 2, 2, 3, 2] [1, 2, 3, 3, 3, 1, 3, 1, 2] [1, 2, 3, 3, 3, 2, 3, 1, 2]
    #strange growth [3, 2, 1, 1, 1, 1, 2, 1, 1], [3, 2, 2, 3, 2, 1, 2, 2, 2] [2, 1, 3, 2, 2, 2, 3, 1, 1] [1, 2, 2, 3, 2, 3, 3, 2, 2] [3, 3, 2, 3, 3, 2, 2, 2, 3]
    #anthill growth [3, 1, 2, 1, 1, 2, 2, 2, 3], [3, 1, 2, 2, 2, 3, 1, 3, 3]
    swag [2, 1, 3, 1, 1, 3, 3, 3, 3], [2, 3, 1, 2, 3, 1, 2, 2, 2], [3, 1, 2, 3, 3, 2, 2, 3, 3]
    #into da matrix [2, 3, 2, 3, 3, 2, 2, 3, 1], [2, 1, 3, 3, 1, 3, 1, 1, 1], [2, 1, 2, 3, 2, 2, 3, 1, 1]
    #root [1, 2, 3, 2, 3, 3, 3, 3, 2]
    #grid [1, 3, 2, 2, 2, 3, 2, 3, 1]
    # hypno pulsar [3, 1, 2, 2, 2, 2, 2, 2, 1], [1, 1, 2, 2, 2, 2, 2, 3, 1]
    #random swag [3, 3, 3, 3, 2, 1, 2, 1, 2], [2, 1, 2, 3, 1, 3, 3, 2, 2]
    #maze growth [3, 2, 3, 3, 3, 1, 1, 1, 3], [1, 3, 3, 2, 3, 1, 3, 1, 1]
    #smoke [1, 3, 2, 3, 3, 1, 2, 2, 3]
    #prison growth [3, 1, 3, 2, 2, 2, 3, 1, 3] [3, 2, 2, 2, 3, 3, 1, 1, 1]
    #inverse fracticle growth [2, 3, 3, 1, 1, 3, 3, 1, 3] [2, 2, 3, 3, 3, 3, 3, 1, 3]
    #1x1 [3, 2, 1, 3, 1, 3, 3, 3, 1]
    
    #tumor growth [3, 3, 2, 1, 1, 2, 2, 3, 1]
    #conways simulation [3, 1, 3, 2, 1, 1, 1, 3, 3]
    #complete fractaql [1, 2, 3, 3, 3, 3, 3, 1, 3]
    #theyre in my walls [2, 1, 2, 3, 3, 1, 1, 1, 1] [3, 2, 2, 2, 3, 2, 2, 1, 1]
    #worms [2, 2, 1, 1, 1, 1, 3, 1, 1]
    swuare worms [1, 3, 1, 2, 3, 3, 2, 1, 1]
    still life maze [1, 3, 3, 2, 3, 3, 1, 1, 2]
    still life city [1, 3, 2, 3, 3, 3, 3, 3, 1]
    perfect cell [1, 1, 3, 3, 2, 2, 2, 1, 3]
    perfect grid [1, 3, 2, 2, 2, 2, 2, 3, 1]
    true organic [1, 1, 3, 2, 1, 3, 1, 1, 1]
    fractal teleportation to pulsar [2, 1, 1, 2, 1, 3, 1, 1, 3]
    [2, 3, 1, 1, 1, 3, 3, 3, 1]
    [2, 2, 2, 3, 3, 1, 2, 1, 3]
    [3, 3, 3, 2, 1, 2, 3, 1, 3]
    chaos avoidance [3, 1, 3, 2, 3, 2, 1, 1, 1]
    [2, 2, 3, 2, 3, 1, 2, 3, 2]
    '''

    while run:
        x, y = pygame.mouse.get_pos()
        clock.tick(FPS)
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and event.button == 3:
                if right_click:
                    right_click = False
                else:
                    right_click = True
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and event.button == 1:
                if click:
                    click = False
                else:
                    click = True
            if event.type == pygame.KEYUP:
                if pressed[pygame.K_SPACE]:
                    if not paused:
                        paused = True
                    else:
                        paused = False
                elif pressed[pygame.K_o]:
                    if frequency:
                        frequency = False
                    if not analyse:
                        analyse = True
                    else:
                        analyse = False
                elif pressed[pygame.K_p]:
                    if analyse:
                        analyse = False
                    if not frequency:
                        frequency = True
                    else:
                        frequency = False
            if right_click and click:
                right_click = False
                click = False

        cells, data, fdata = update(x, y, cells, paused, click, right_click,num_type,analyse,data,step,frequency,fdata)
        pygame.display.update()
        step += 1
    pygame.quit()


if __name__ == '__main__':
    main()
