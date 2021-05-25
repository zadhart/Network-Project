# -*- coding: UTF-8 -*-
import socket
import pygame
from tkinter import *
from client import *


# As mensagens que devem aparecer na tela do jogador tem que seguir essa formatação exata wagner, se não elas não vão
# aparecer no centro
# mensagens = ["  Deu velha!", "Você venceu!", "Você perdeu!"]


def centralize(window, largura, altura):

    largura_screen = window.winfo_screenwidth()
    altura_screen  = window.winfo_screenheight()

    posx = largura_screen/2 - largura/2
    posy = altura_screen/2 - altura/2

    window.geometry("%dx%d+%d+%d" %(largura, altura, posx, posy))


# Control function of the color and direction of the gradient animation
# Parameters: r, g and b value of the color; direction of the gradient effect
def gradient(b_color, color_control):

    if b_color == 255:           # if color r, g and b value are at maximun
        color_control = "down"   # change direction of color_control for decrease the color
    if b_color == 40:            # if color r, g and b value are at the minimum
        color_control = "up"     # change direction of color_control for increase the color
    if color_control == "up":    # if is set to increase
        b_color += 1             # increase one in the color rgb value
    if color_control == "down":  # if is set to decrease
        b_color -= 1             # decrease one in the rgb value

    return (b_color, color_control)


# Function that draws the waiting room layout before the match starts
# Parameter: pygame window
def waiting_room(window, user):
    other_player = False
    simbol = ""
    font1 = pygame.font.SysFont('comicsans', 39)
    x = 0
    wait_message = ["Esperando por jogador.", "Esperando por jogador..",
                    "Esperando por jogador..."]
    # Rafa aqui vc tem que pegar o nome do usuário direto da tela do tKinter e colocar nessa parte do input
    msg = "newUser " + user

    # Rafa isso aqui serve para saber o ip da máquina que está rodando o servidor
    ip = "192.168.0.107"

    # Vc pode mudar a porta mas tem que colocar a msm porta no codigo do servidor
    port = 69

    # Esse who é importante eu acho mas nn está sendo utilizado mas é melhor nn tirar
    who = None

    # Essa parte cria o socket e conecta com o servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.001)

    s.connect((ip, port))
    print("connected")

    # This send the user name
    s.send(msg.encode())

    while not other_player:
        window.fill((0, 0, 0))
        text1 = font1.render(wait_message[x//300], True, (255, 255, 255))
        text2 = font1.render('Pressione C para retornar ao Menu Principal',
                             True, (255, 255, 255))
        window.blit(text1, (150, 250))
        window.blit(text2, (20, 420))
        x = (x + 1) % 900
        pygame.display.update()
        for event in pygame.event.get():      # event looping
            if event.type == pygame.QUIT:     # if user close the window
                pygame.quit()                 # finish execution
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:   # if user press C key
                    return False, None        # return to the main menu
        try:
            data = s.recv(1024).decode().split()
            if len(data) > 1:
                print(data[0])
                if data[0] == "begin" or data[0] == "OKbegin":
                    other_player = True
                if data[1] == user:
                    simbol = "X"
                if data[1] != user:
                    simbol = "O"
                print(simbol)
        except:
            pass


    return True, s, simbol


# Function that draws the layout of the main menu window
# Parameters: pygame window; r, g and b dynamic values for gradient effect
def draw_menu(window, blink_color):
    window.fill((0, 0, 0))

    # Creating the font elements for the text of the main menu
    font0 = pygame.font.Font("Fonts\8-bit Arcade In.ttf", 90)  # local font
    font1 = pygame.font.SysFont('comicsans', 40)               # system font
    font2 = pygame.font.SysFont('comicsans', 1000)             # system font

    # Text elements of the main menu

    # background hash symbol
    text0 = font2.render('#', True, (10, 10, 10))
    # title of the game
    text1 = font0.render('Jogo da Velha', True, (255, 255, 255))
    # instruction for start a new match
    text2 = font1.render('Pressione a tecla de Espaço para iniciar', True,
                         (blink_color, blink_color, blink_color))
    text3 = font1.render('uma nova partida.', True,
                         (blink_color, blink_color, blink_color))

    # Drawning the window's text elements
    window.blit(text0, (100, 0))
    window.blit(text1, (20, 255))
    window.blit(text2, (25, 400))
    window.blit(text3, (175, 430))
    return


# Function that draws the layout of the window with the result of the match
# Parameters: board matrix; pygame window; message with the resulf of the match
def result(matriz, window, message, user):
    # local var declarations
    font1 = pygame.font.SysFont('comicsans', 80)  # font element
    font2 = pygame.font.SysFont('comicsans', 39)  # font element
    g_color = 255     # initial gradient color
    g_direc = "down"  # initial gradient direction
    x = 0  # aux var for rgb values for building inset gradient animation

    while True:  # main loop of the result window
        g_color, g_direc = gradient(g_color, g_direc)  # updating color and direction of the gradient animation
        draw_game(matriz, window, 10, user)   # redrawing the table with a soft color for background

        # text elements
        text1 = font1.render(message, True, (x, x, x))
        text2 = font2.render('Pressione R para retornar ao Menu Principal',
                           True, (g_color, g_color, g_color))

        # drawning text elements in the window
        window.blit(text1, (120, 275))
        window.blit(text2, (20, 420))

        pygame.display.update()               # updating the display

        for event in pygame.event.get():      # event looping

            if event.type == pygame.QUIT:     # if user close the window
                return False                  # finish execution
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:   # if user press R key
                    return True               # return to the main menu

        if x != 255:  # conditional for the raising gradient effect of the result message
            x += 1


# Function that draws the interactive board of each match
# Parameters: board matrix; pygame window; r, g and b value of the board and its elements
def draw_game(matriz, window, color, user):
    window.fill((0, 0, 0))  # filling the display with a black (rgb(0,0,0)) background
    height = 600            # window's height
    width = 600             # window's width
    size = 200              # size of each side of the squares of the board
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render(user, True, (color, color, color))
    window.blit(text, (10, 10))

    for i in range(1, 3):   # looping for draw the lines of the board
        pygame.draw.line(window, (color, color, color), (0, i * size), (width, i * size), 3)
        pygame.draw.line(window, (color, color, color), (i * size, 0), (i * size, height), 3)

    for i in range(3):      # looping for draw each value of the board squares
        font = pygame.font.SysFont('comicsans', 100)  # font element of the values
        for j in range(3):
            # getting the x and y coordinates of the table for draw the text elements (X, O)
            x = j * size
            y = i * size

            # conditional for checking the values of the original matrix
            if matriz[i][j] == 1:  # if the value in the matrix position = 1, draw an X
                mark = font.render('X', True, (color, color, color))
                window.blit(mark, (x + 75, y + 75))

            if matriz[i][j] == 2:  # if the value in the matrix position = 2, draw an O
                mark = font.render('O', True, (color, color, color))
                window.blit(mark, (x + 75, y + 75))


# Match's control function
# Parameters: game loop variable; board matrix; turn control variable; pygame window
def jogo_da_velha(game, matriz, vez, window, s, simbol, user):
    draw = False  # draw control local variable
    turn = False
    data = None
    valid = True
    mensagem = "  Deu velha!"
    user_s = user + "("+simbol+")"
    s.settimeout(0.000001)

    while game:   # main loop of the game
        draw_game(matriz, window, 255, user_s)  # drawning the board and the elements within
        pygame.display.update()         # updating the window

        for event in pygame.event.get():   # event's looping
            if event.type == pygame.QUIT:  # if user close the window, terminate the game
                game = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and turn:  # if user mouse click the board
                pos = pygame.mouse.get_pos()        # getting mouse position
                x = pos[1]//200                     # calculating the board x coordinate of the mouse position
                y = pos[0]//200                     # calculating the board y coordinate of the mouse position
                matriz, vez, valid = modify(matriz, vez, x, y, simbol)  # modifing the board matrix with the given variables
                game_board = convert_output(matriz)
                print_matrix(matriz)                     # print matrix for control
                draw_game(matriz, window, 255, user_s)           # redrawning the board
                pygame.display.update()                  # updating the display

                if valid:
                    turn = False
                    s.send(play_game(game_board, simbol).encode())
                    if (velha(game_board)):
                        game = False
                        s.close()
        try:
            data = s.recv(1024).decode().split()
            print(data)
            if (len(data) > 0):
                if (data[0] == "yourTurn" and data[1] == simbol):
                    turn = True
                    print("F")
                    matriz = convert_input(data[2])
                    draw_game(matriz, window, 255, user_s)  # redrawning the board
                    pygame.display.update()
                    if (velha(data[2])):
                        game = False
                        s.send(play_game(data[2], simbol).encode())
                        s.close()
                if (data[0] == "youWin"):
                    mensagem = "Você venceu!"
                    game = False
                    s.close()
                if (data[0] == "youLoose"):
                    mensagem = "Você perdeu!"
                    game = False
                    s.close()

        except:
            # print("ops")
            pass


    # board gradient animation of the match's end
    color_board = 255
    while color_board > 10:
        draw_game(matriz, window, color_board, user_s)  # redrawing the board with the new color
        color_board -= 1                        # decreasing the color value for the gradient effect
        pygame.display.update()                 # updating the display

    r = result(matriz, window, mensagem, user_s)
    return r


# Function that draws the username autentication window
def username_aut():
    color1 = "black"
    color2 = "white"
    fonte = "Times 12"
    login_window = Tk()
    login_window['bg'] = color1
    login_window.title('Autentication')
    # login_window.iconbitmap('login_icon.ico')
    centralize(login_window, 420, 100)

    frame_login = Frame(login_window, bg = color1)
    frame_login.grid(row = 0, column = 1, ipadx = 10, padx = 10, ipady = 10, pady =10)
    username_entry  = Entry(frame_login, font = fonte,)
    label_us  = Label(frame_login, font = fonte, bg = color1, fg = color2,
                       text = "Nome de Usuário:")
    submitbtn = Button(frame_login, font = fonte, fg = color2, bg = color1,
                       text = 'Login', command = lambda: main(login_window, True, username_entry.get()))
    friendly_message = Label(login_window, font = fonte, bg = color1, fg = color2,
                       text = "Por favor digite um nome de usuário sem espaçamentos.")

    label_us.grid (row = 0, column = 0, ipadx=10, padx=1)
    username_entry.grid (row = 0, column = 1, ipadx=1, padx=1)
    submitbtn.grid(row = 0, column = 2, ipadx=10, padx=10)
    friendly_message.grid(row = 1, column = 1)

    login_window.mainloop()


# Main function with the running main loop
# Parameter: main loop control variable
def main(autenticate_window, running, user):
    if user:  # only starts the game with a valid username
        autenticate_window.destroy()  # close autentication window
        win = pygame.display.set_mode((600, 600))  # generating pygame display window
        color_control = "down"  # control var for the gradient animation of main menu
        b_color = 255           # default maximun rgb value for start the gradient effect

        while(running):  # main looping
            # generating the main menu window
            draw_menu(win, b_color)
            # updating color value and direction of the gradient animation
            b_color, color_control = gradient(b_color, color_control)
            # updating the display window
            pygame.display.update()

            for event in pygame.event.get():   # event looping
                if event.type == pygame.QUIT:  # if the user closes the window
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # if user press space key
                        matriz = [[0, 0, 0],         # generating the unset board matrix of the match
                                  [0, 0, 0],
                                  [0, 0, 0]]
                        waiting_aux, s, simbol = waiting_room(win, user)
                        if waiting_aux:        # calling of the waiting run function
                            running = jogo_da_velha(True, matriz, 1, win, s, simbol, user)  # starting a new match


pygame.init()  # pygame initialization
username_aut()
# main(True)     # call of the main function
