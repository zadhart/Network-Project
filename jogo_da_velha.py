# -*- coding: UTF-8 -*-
# Function that print a matrix
# Parameter: board matrix
def print_matrix(matrix):
    for i in matrix:  # for each row in the matrix
        print(i)      # print the row


# Function that checks the elements of matrix's diagonals
# Parameter: board matrix
# Return: True if one of the diagonals is fill with 1 or 2; False otherwise
def check_diag(m):
    if m[1][1] == 0:  # if the central position is unset for any value, than any of the diags is fill
        return False  # there is no winner
    # if all values of the primary diagonal are equal there is a winner
    if m[0][0] == m[1][1] and m[1][1] == m[2][2]:
        return True  # there is a winner
    # if all values of the secondary diagonal are equal there is a winner
    if m[0][2] == m[1][1] and m[1][1] == m[2][0]:
        return True  # there is a winner


# Function that checks the elements of matrix's columns
# Parameter: board matrix
# Return: True if one of the columns is fill with 1 or 2; False otherwise
def check_column(m):
    i = 0   # colum index variable
    while i <= 2:  # checking each column of the matrix
        # if the first element of the column isn't unset and all the elements of the column are equal
        if m[0][i] != 0 and m[0][i] == m[1][i] and m[1][i] == m[2][i]:
            return True  # there is a winner
        i += 1  # increasing the column index value

    return False  # there is no winner


# Function that checks the elements of matrix's rows
# Parameter: board matrix
# Return: True if one of the rows is fill with 1 or 2; False otherwise
def check_row(matrix):
    for i in matrix:                  # for loop checking each row in the matrix
        sum = i[0] + i[1] + i[2]      # sum of the elements of each row
        if sum % 3 == 0 and sum > 0:  # if sum divisible by 3 and greater than 0, the values of the row may be equal
            if i[0] == i[1]:          # if at least two values of the row are equal, than all the three are equal
                return True           # there is a winner

    return False  # there is no winner


# Function that write new values in the matrix given a position
# Parameters: board matrix; turn control variable; x coordinate; y coordinate
# Return: the board matrix and turn control variable
def modify(m, v, x, y):
    if m[x][y] == 0:     # if the given position of the matrix is unset
        if v % 2 == 0:   # if player 2 turn
            m[x][y] = 2  # write 2 as the new value of the given position

        else:            # if player 1 turn
            m[x][y] = 1  # write 1 as the new value of the given position
        return m, v + 1  # return the new board matrix and the turn control variable increased

    else:                # if the position is set with a value different from zero an illegal position
        print("Inválido, informe novas coordenadas")
        return m, v      # return the matrix and the turn control var without modifications


# Function for checking the match result
# Parameters: board matrix; turn control variable
# Return: Game loop running control value; Draw result control value
def check(m, v):
    if check_row(m) or check_diag(m) or check_column(m):  # there's a winner by row, column or diagonals
        print('alguém venceu')
        # match finished with a winner
        return (False, False)

    elif v == 10:                                         # there's no winner, therefore it's a draw
        print('deu velha')
        # match finished with draw
        return (False, True)

    # match not finished: no winners and board still not completely fill
    return (True, False)