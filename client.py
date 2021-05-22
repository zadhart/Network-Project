import socket

def play_game(game, who):
    newgame = str(input("Digite o jogo: "))

    return str("play " + who + " " + newgame)



def run_client():
    msg = "newUser " + input("Username:")

    my_ip = socket.gethostbyname(socket.gethostname())
    ip = '192.168.0.18'
    port = 69
    who = None

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ip, port))
    print("connected")

    # This send the user name
    s.send(msg.encode())

    while True:

        data = s.recv(1024).decode().split()
        if (len(data) > 0):

            if (data[0] == "finished"):
                s.close()
                break

            elif (data[0] == "yourTurn"):
                print(data[2])
                s.send(play_game(data[2], data[1]).encode())

            elif (data[0] == "youWin"):
                print("Nice Job")

            elif (data[0] == "youLoose"):
                print("GG EASY NOOOOOB")

            elif (data[0] == "begin"):
                print(data[1] + " vs " + data[2])
                print("game: " + data[3])


run_client()

