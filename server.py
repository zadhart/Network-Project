import socket
from threading import Thread

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

        data = "yourTurn O " + game
        players_data["playerO"]["connection"].send(data.encode())
        response = players_data["playerO"]["connection"].recv(1024).decode().split()

        if (response[0] == "play"):
            game = response[2]


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
            break

    playerX = player_queue[0]
    playerO = player_queue[1]
    players_data = {"playerO": clients[playerO], "playerX": clients[playerX]}

    player_queue.pop(0)
    player_queue.pop(0)

    playgame(playerX, playerO, players_data)

run_server()





