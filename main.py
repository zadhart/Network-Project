# jogo da velha
# -*- coding: UTF-8 -*-
from jogo_da_velha import modify, check, print_matrix
import pygame


def draw_menu(window, blink_color):
    window.fill((0, 0, 0))
    font0 = pygame.font.Font("Fonts\8-bit Arcade In.ttf", 90)
    font1 = pygame.font.SysFont('comicsans', 40)
    font2 = pygame.font.SysFont('comicsans', 1000)
    mark0 = font0.render('Jogo da Velha', True, (255, 255, 255))
    mark1 = font1.render('Pressione a tecla de Espaço para iniciar', True, (blink_color, blink_color, blink_color))
    mark2 = font2.render('#', True, (10, 10, 10))
    mark3 = font1.render('uma nova partida.', True, (blink_color, blink_color, blink_color))
    window.blit(mark2, (100, 0))
    window.blit(mark0, (20, 255))
    window.blit(mark1, (25, 400))
    window.blit(mark3, (160, 430))
    return


def restart(matriz, window, r):
    while r:
        draw_game(matriz, window, 100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True


def draw_game(matriz, window, color):
    window.fill((0, 0, 0))
    height = 600
    width = 600
    size = 200
    for i in range(1, 3):
        pygame.draw.line(window, (color, color, color), (0, i * size), (width, i * size), 3)
        pygame.draw.line(window, (color, color, color), (i * size, 0), (i * size, height), 3)
    for i in range(3):
        font = pygame.font.SysFont('comicsans', 100)
        for j in range(3):
            x = j * size
            y = i * size
            if matriz[i][j] == 1:
                mark = font.render('X', True, (color, color, color))
                window.blit(mark, (x + 75, y + 75))
            if matriz[i][j] == 2:
                mark = font.render('O', True, (color, color, color))
                window.blit(mark, (x + 75, y + 75))


def jogo_da_velha(game, matriz, vez, window):
    while game:
        draw_game(matriz, window, 255)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[1]//200
                y = pos[0]//200
                matriz, vez = modify(matriz, vez, x, y)
                print_matrix(matriz)
                vez += 1
                print(vez)
                draw_game(matriz, window, 255)
                pygame.display.update()
                game = check(matriz, vez)
        # print_matrix(matriz)
    r = restart(matriz, window, True)
    return r


def main(running):
    win = pygame.display.set_mode((600, 600))
    color_control = "up"
    b_color = 255
    while(running):
        draw_menu(win, b_color)
        if b_color == 255:
            color_control = "down"
        if b_color == 40:
            color_control = "up"
        if color_control == "up":
            b_color += 1
        if color_control == "down":
            b_color -= 1
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    running = jogo_da_velha(True, matriz, 1, win)


pygame.init()
main(True)
