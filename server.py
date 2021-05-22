import socket
import threading

def checkgame(game):

    #Check the diagonals of the matrix and return a winner
    if(int(game[0]) + int(game[4]) + int(game[8]) == 6):
        return("O")

    elif(int(game[2]) + int(game[4]) + int(game[6]) == 6):
        return("O")

    elif (int(game[0]) + int(game[4]) + int(game[8]) == 15):
        return ("X")

    elif (int(game[2]) + int(game[4]) + int(game[6]) == 15):
        return ("X")

    #Check the columns of the matrix and return a winner
    elif (int(game[0]) + int(game[3]) + int(game[6]) == 6):
        return ("O")

    elif (int(game[1]) + int(game[4]) + int(game[7]) == 6):
        return ("O")

    elif (int(game[2]) + int(game[5]) + int(game[8]) == 6):
        return ("O")

    elif (int(game[0]) + int(game[3]) + int(game[6]) == 15):
        return ("X")

    elif (int(game[1]) + int(game[4]) + int(game[7]) == 15):
        return ("X")

    elif (int(game[2]) + int(game[5]) + int(game[8]) == 15):
        return ("X")

    #Check the rows of the matrix and return a winner
    elif (int(game[0]) + int(game[1]) + int(game[2]) == 6):
        return ("O")

    elif (int(game[3]) + int(game[4]) + int(game[5]) == 6):
        return ("O")

    elif (int(game[6]) + int(game[7]) + int(game[8]) == 6):
        return ("O")

    elif (int(game[0]) + int(game[1]) + int(game[2]) == 15):
        return ("X")

    elif (int(game[3]) + int(game[4]) + int(game[5]) == 15):
        return ("X")

    elif (int(game[6]) + int(game[7]) + int(game[8]) == 15):
        return ("X")

    #If there's no winner, then return false
    else:
        return (False)


def playgame(playerX, playerO, players_data):
    game = "000000000"

    data = ""

    data = "begin " + str(playerX) + " " + str(playerO) + " " + game
    players_data["playerX"]["connection"].send(data.encode())
    players_data["playerO"]["connection"].send(data.encode())

    while True:
        data = "yourTurn X " + game
        players_data["playerX"]["connection"].send(data.encode())
        response = players_data["playerX"]["connection"].recv(1024).decode().split()

        if(response[0] == "play"):
            game = response[2]

            check = checkgame(str(game))
            if(check != False):

                if(check == "X"):
                    data = "youWin"
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                    data = "youLoose"
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                else:
                    data = "youWin"
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                    data = "youLoose"
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                break

        data = "yourTurn O " + game
        players_data["playerO"]["connection"].send(data.encode())
        response = players_data["playerO"]["connection"].recv(1024).decode().split()

        if (response[0] == "play"):
            game = response[2]

            check = checkgame(str(game))
            if (check != False):

                if (check == "X"):
                    data = "youWin"
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                    data = "youLoose"
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                else:
                    data = "youWin"
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                    data = "youLoose"
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                break



def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    port = 69

    clients = {}
    games = {}
    player_queue = []

    s.bind(('', port))

    s.listen(5)
    print("socket is listening")

    while True:
        if (len(player_queue) < 2):
            c, addr = s.accept()
            name = c.recv(1024).decode().split()[1]
            clients[name] = {"userName": name, "addr": addr, "connection": c}

            print('Got connection from', addr)

            clients[name]["connection"].send('OK'.encode())

            player_queue.append(str(name))
            print(player_queue)

        else:
            playerX = player_queue[0]
            playerO = player_queue[1]
            players_data = {"playerO": clients[playerO], "playerX": clients[playerX]}

            player_queue.pop(0)
            player_queue.pop(0)

            threading.Thread(target=playgame, args=(playerX, playerO, players_data)).start()
            #playgame(playerX, playerO, players_data)

            print("Created a new thread")

run_server()





