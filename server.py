import socket

def waitplayers():
    c, addr = s.accept()
    name = c.recv(1024).decode().split()[1]
    clients[name] = {"userName": name, "addr": addr, "connection": c}

    print('Got connection from', addr)

    clients[name]["connection"].send('OK'.encode())

    player_queue.append(str(name))
    print(player_queue)

def playgame():
    game = "000000000"
    playerX = player_queue[0]
    playerO = player_queue[1]

    player_queue.pop(0)
    player_queue.pop(0)

    data = ""

    data = "begin " + str(playerX) + " " + str(playerO) + " " + game
    clients[playerX]["connection"].send(data.encode())
    clients[playerO]["connection"].send(data.encode())

    while True:
        data = "yourTurn X " + game
        clients[playerX]["connection"].send(data.encode())
        response = clients[playerX]["connection"].recv(1024).decode().split()

        if(response[0] == "play"):
            game = response[2]

        data = "yourTurn O " + game
        clients[playerO]["connection"].send(data.encode())
        response = clients[playerO]["connection"].recv(1024).decode().split()

        if (response[0] == "play"):
            game = response[2]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

port = 69

clients = {}
games = {}
player_queue = []

s.bind(('', port))

s.listen(5)
print ("socket is listening")

while True:
    if(len(player_queue) < 2):
        waitplayers()

    else:
        break

playgame()






