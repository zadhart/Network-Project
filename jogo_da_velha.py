# -*- coding: UTF-8 -*-
def print_matrix(matrix):
    for i in matrix:
        print(i)


def check_diag(m):
    if m[1][1] == 0:
        return False
    if m[0][0] == m[1][1] and m[1][1] == m[2][2]:
        return True
    if m[0][2] == m[1][1] and m[1][1] == m[2][0]:
        return True


def check_column(matrix):
    i = 0
    while i <= 2:
        if matrix[0][i] != 0:
            if matrix[0][i] == matrix[1][i] and matrix[1][i] == matrix[2][i]:
                return True
        i += 1
    return False


def check_row(matrix):
    for i in matrix:
        sum = i[0] + i[1] + i[2]
        if sum % 3 == 0 and sum > 0:
            if i[0] == i[1]:
                return True
    return False


def modify(m, v, x, y):
    if m[x][y] == 0:
        if v % 2 == 0:
            m[x][y] = 2
        else:
            m[x][y] = 1
    else:
        print("Inválido, informe novas coordenadas")
        return m, v-1
    return m, v


def check(m, v):
    if v == 10:
        print('deu velha')
        return False
    if check_row(m):
        print('venceu')
        return False
    if check_column(m):
        print('venceu')
        return False
    if check_diag(m):
        print('venceu')
        return False
    return True