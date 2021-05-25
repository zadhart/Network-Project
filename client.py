import socket
from jogo_da_velha import convert_output


# This function return a message, that will be sent to the server
def play_game(game, who):

    return str("play " + who + " " + game)


def convert_output(matrix):
    output = ""
    for i in matrix:
        for j in i:
            if j == 1:
                output = output + "5"
            else:
                output = output + str(j)
    print(output)
    return output


def convert_input(string):
    matrix = [[0,0,0],[0,0,0], [0,0,0]]
    i = 0
    while i < 9:
        if string[i] == "5":
            matrix[i//3][i%3] = 1
        else:
            matrix[i//3][i%3] = int(string[i])
        i+=1

    return matrix


def print_matrix(matrix):
    for i in matrix:  # for each row in the matrix
        print(i)      # print the row


# Function that write new values in the matrix given a position
# Parameters: board matrix; turn control variable; x coordinate; y coordinate
# Return: the board matrix and turn control variable
def modify(m, v, x, y, sim):
    if m[x][y] == 0:     # if the given position of the matrix is unset
        if sim == "X":     # if player 2 turn
            m[x][y] = 1  # write 2 as the new value of the given position
        else:            # if player 1 turn
            m[x][y] = 2  # write 1 as the new value of the given position
        return m, v + 2, True  # return the new board matrix and the turn control variable increased

    else:                # if the position is set with a value different from zero an illegal position
        print("Inválido, informe novas coordenadas")
        return m, v, False      # return the matrix and the turn control var without modifications


def velha(string):
    if(len(string) > 0):
        for i in string:
            if i == "0":
                return False
        return True


