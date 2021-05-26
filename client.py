import socket


# This function returns a message, that will be sent to the server
def play_game(game, who):

    return str("play " + who + " " + game)


# This function converts the board matrix returns and returns the board string for be sent to the server
def convert_output(matrix):
    output = ""
    for i in matrix:    # checks each row
        for j in i:     # checks each column of the row
            if j == 1:
                output = output + "5"  # in the string the X = 5, but in the matrix X = 1
            else:
                output = output + str(j)
    # print(output)
    return output


# This function converts the board string of the server message and returns the board matrix
def convert_input(string):
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    i = 0
    while i < 9:
        if string[i] == "5":
            matrix[i//3][i%3] = 1  # in the string the X = 5, but in the matrix X = 1
        else:
            matrix[i//3][i%3] = int(string[i])
        i += 1  # increasing index value

    return matrix


# This function prints the Matrix
def print_matrix(matrix):
    for i in matrix:  # for each row in the matrix
        print(i)      # print the row


# This function writes new values in the matrix given a valid position
def modify(m, x, y, sim):
    if m[x][y] == 0:     # if the given position of the matrix is unset
        if sim == "X":   # if player 2 turn
            m[x][y] = 1  # write 2 as the new value of the given position
        else:            # if player 1 turn
            m[x][y] = 2  # write 1 as the new value of the given position
        return m, True   # return the new board matrix and the validate control variable set as True

    else:                # if the position is set with a value different from zero an illegal position
        print("Inválido, informe novas coordenadas")
        return m, False  # return the matrix and the validate control var set as false


# This function checks if the match ended up with a draw
def velha(string):
    if(len(string) > 0):      # if there's a string
        for i in string:      # loop for check each position of the string
            if i == "0":      # if there's at least one unset value at the board
                return False  # than the board is not completely filled, therefore it's not a draw

        return True           # if the board is completely set, it's a draw


# This function centralize the tkinter window given its width and height
def centralize(window, largura, altura):

    largura_screen = window.winfo_screenwidth()   # getting the width and height of the screen
    altura_screen  = window.winfo_screenheight()

    posx = largura_screen/2 - largura/2           # calculating windows position
    posy = altura_screen/2 - altura/2

    # declaring windows width, height and position in the center of the screen
    window.geometry("%dx%d+%d+%d" %(largura, altura, posx, posy))


# This function controls the color and direction of the gradient animation
def gradient(g_color, color_control):

    if g_color == 255:           # if color r, g and b value are at maximun
        color_control = "down"   # change direction of color_control for decrease the color
    if g_color == 40:            # if color r, g and b value are at the minimum
        color_control = "up"     # change direction of color_control for increase the color
    if color_control == "up":    # if is set to increase
        g_color += 1             # increase one in the color rgb value
    if color_control == "down":  # if is set to decrease
        g_color -= 1             # decrease one in the rgb value

    return (g_color, color_control)
