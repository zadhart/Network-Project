# -*- coding: UTF-8 -*-
import socket
import pygame
from tkinter import *
from client import *
from socket import AF_INET, SOCK_STREAM


# Function that draws the waiting room layout before the match starts
# Parameter: pygame window
def waiting_room(window, user):
    other_player = False
    simbol = ""
    font1 = pygame.font.SysFont('comicsans', 39) # font definition for text elements
    
    wait_message = ["Esperando por jogador.", "Esperando por jogador..",
                    "Esperando por jogador..."]  # message list for text animation
    x = 0                                        # text animation aux var

    # redes
    msg = "newUser " + user  # message for be sent to the server
    ip = "127.0.0.1"         # localhost ip
    port = 69                # port of the conection to the server
    who = None               
    # creating socket
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)     # setting timeout for stop conflicts with pygame
    s.connect((ip, port))  # connecting socket
    # print("connected")   #  
    s.send(msg.encode())   # socket sends message to the server

    while not other_player:   # waiting for another player joing the the server
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
                    s.close()
                    return False, None, None  # return to the main menu
        try:
            data = s.recv(1024).decode().split()  # receiving message and split into a string list 
            
            if len(data) > 1:  # if there is a message
                # print(data[0])
                if data[0] == "begin" or data[0] == "OKbegin": # other player connected
                    other_player = True  # stoping waiting loop for start the match
                
                # determinating players symbols at the client-side
                if data[1] == user:
                    simbol = "X"
                if data[2] == user:
                    simbol = "O"
                print(simbol)
        except socket.timeout:
            pass

    return True, s, simbol  # returning other player state, socket and the symbol


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
    x = 0             # aux var of rgb values for building inset gradient animation

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
    font_user = pygame.font.SysFont('comicsans', 30)            # font element declaration
    text = font_user.render(user, True, (color, color, color))  # rendering the username with the font element
    window.blit(text, (10, 10))  # blitting username in the board

    for i in range(1, 3):   # looping for draw the lines of the board
        pygame.draw.line(window, (color, color, color), (0, i * size), (width, i * size), 3)
        pygame.draw.line(window, (color, color, color), (i * size, 0), (i * size, height), 3)

    for i in range(3):      # looping for draw each value of the board squares
        font = pygame.font.SysFont('comicsans', 100)  # font element of the symbols
        for j in range(3):
            # getting the x and y coordinates of the table for draw the text elements (X, O)
            x = j * size
            y = i * size

            # conditional for checking the values of the original matrix
            if matriz[i][j] == 1:  # if the value in the matrix position = 1 (player 1), draw an X
                mark = font.render('X', True, (color, color, color))
                window.blit(mark, (x + 75, y + 75))

            if matriz[i][j] == 2:  # if the value in the matrix position = 2 (player 2), draw an O
                mark = font.render('O', True, (color, color, color))
                window.blit(mark, (x + 75, y + 75))


# Match's control function
# Parameters: game loop variable; board matrix; turn control variable; pygame window
def jogo_da_velha(game, matriz, window, s, symbol, user):
    draw = False    # draw control local variable
    turn = False    # aux turn control variable for allow player's move
    valid = True    # aux turn control variable for validate player's move
    mensagem = "  Deu velha!"
    user_s = user + "("+symbol+")"  # username string with it signs for
    s.settimeout(0.25)              # setting socket timeout

    while game:   # main loop of the game
        draw_game(matriz, window, 255, user_s)  # drawning the board and the elements within
        pygame.display.update()                 # updating the window

        for event in pygame.event.get():   # event's looping
            if event.type == pygame.QUIT:  # if user close the window, terminate the game and the connection
                game = False
                s.close()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP and turn:  # if user mouse click the board
                pos = pygame.mouse.get_pos()        # getting mouse position
                x = pos[1]//200                     # calculating the board x coordinate of the mouse position
                y = pos[0]//200                     # calculating the board y coordinate of the mouse position
                matriz, valid = modify(matriz, x, y, symbol)  # modifing the board matrix with the given position
                game_board = convert_output(matriz)      # converting the board matrix for string to send to server
                print_matrix(matriz)                     # print matrix for control
                draw_game(matriz, window, 255, user_s)   # redrawning the board
                pygame.display.update()                  # updating the display

                if valid:          # if move is valid
                    turn = False   # changing control turn variable for alternate the moves
                    s.send(play_game(game_board, symbol).encode())  # sending the message to the server

        try:
            data = s.recv(1024).decode().split()  # trys recieve server's message
            # print(data)
            if (len(data) > 0):   # if there'is a message
                if (data[0] == "yourTurn" and data[1] == symbol):
                    turn = True   # settig turn control variable for allow playe's move
                    matriz = convert_input(data[2])         # converting message's board string to board matrix
                    draw_game(matriz, window, 255, user_s)  # redrawning the board
                    pygame.display.update()                 # updating the display
                    
                    if (velha(data[2])):  # if there's a draw
                        game = False      # stop running the match
                        s.send(play_game(data[2], symbol).encode())  # send the message to the server
                        
                if (data[0] == "youWin"):      # if player win
                    mensagem = "Você venceu!"  # setting message of the result window
                    game = False               # stop running the match
                    
                if (data[0] == "youLoose"):          # if player loose
                    mensagem = "Você perdeu!"        # setting message of the result window
                    matriz = convert_input(data[1])  # converting message's board string to board matrix
                    game = False                     # stop running the match
                    draw_game(matriz, window, 255, user_s)  # redrawning the board

        except:
            if symbol == "X" and matriz == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]:
                turn = True
            pass

    s.close()
    # board gradient animation of the match's end
    color_board = 255
    while color_board > 30:
        draw_game(matriz, window, color_board, user_s)  # redrawing the board with the new color
        color_board -= 1                                # decreasing the color value for the gradient effect
        pygame.display.update()                         # updating the display

    r = result(matriz, window, mensagem, user_s)        # calling the result display function
    return r                                            # return


# Function that draws the username autentication window
def username_aut():
    color1 = "black"    # first color
    color2 = "white"    # second color
    fonte = "Times 12"  # font
    aut_window = Tk()   # generating tkinter's window
    aut_window['bg'] = color1                   # declaring window's background color
    aut_window.title('Autentication')           # declaring window's title
    # login_window.iconbitmap('aut_icon.ico')
    centralize(aut_window, 420, 100)            # centralizing window's position

    # creating and griding autentication frame
    frame_aut = Frame(aut_window, bg = color1)
    frame_aut.grid(row = 0, column = 1, ipadx = 10, padx = 10, ipady = 10, pady =10)

    # crating window's elements
    username_entry  = Entry(frame_aut, font = fonte)
    label_us  = Label(frame_aut, font = fonte, bg = color1, fg = color2,
                       text = "Nome de Usuário:")
    submitbtn = Button(frame_aut, font = fonte, fg = color2, bg = color1,
                       text = 'Login', command = lambda: main(aut_window, True, username_entry.get()))
    friendly_message = Label(aut_window, font = fonte, bg = color1, fg = color2,
                       text = "Por favor digite um nome de usuário sem espaçamentos.")

    # griding elements to the window
    label_us.grid (row = 0, column = 0, ipadx=10, padx=1)
    username_entry.grid (row = 0, column = 1, ipadx=1, padx=1)
    submitbtn.grid(row = 0, column = 2, ipadx=10, padx=10)
    friendly_message.grid(row = 1, column = 1)

    aut_window.mainloop()  # main loop of the current window


# Main function with the running main loop
# Parameter: main loop control variable
def main(autenticate_window, running, user):
    if user:  # only starts the game with a valid username
        autenticate_window.destroy()               # close autentication window
        win = pygame.display.set_mode((600, 600))  # generating pygame display window
        color_control = "down"                     # control var for the gradient animation of main menu
        b_color = 255                              # default maximun rgb value for start the gradient effect

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
                        waiting_aux, s, simbol = waiting_room(win, user)  # calling of the waiting run function

                        if waiting_aux:     # if waiting room not cancelled start a new match
                            running = jogo_da_velha(True, matriz, win, s, simbol, user)


pygame.init()    # pygame initialization
username_aut()   # call of the initial function

