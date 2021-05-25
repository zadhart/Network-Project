import socket
import threading


# This function search the game for a winner
def checkgame(game):
    if (game == "000000000"):
        return False
    # Check the diagonals of the matrix and return a winner
    elif(int(game[0]) + int(game[4]) + int(game[8]) == 6):
        return("O")

    elif(int(game[2]) + int(game[4]) + int(game[6]) == 6):
        return("O")

    elif (int(game[0]) + int(game[4]) + int(game[8]) == 15):
        return ("X")

    elif (int(game[2]) + int(game[4]) + int(game[6]) == 15):
        return ("X")

    # Check the columns of the matrix and return a winner
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

    # Check the rows of the matrix and return a winner
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

    # If there's no winner, then return false
    else:
        return (False)


#This function handles the game between two players
def playgame(playerX, playerO, players_data):

    game = "000000000" #Initialize the game

    data = ""

    #Send the game to the players
    data = "begin " + str(playerX) + " " + str(playerO) + " " + game
    players_data["playerX"]["connection"].send(data.encode())
    players_data["playerO"]["connection"].send(data.encode())

    while True:
        #Send the data of the to player X
        data = "yourTurn X " + game
        players_data["playerX"]["connection"].send(data.encode())

        #Getting the response of player X
        response = players_data["playerX"]["connection"].recv(1024).decode().split()

        #If the code of message is "play", then make the move
        if(response[0] == "play"):

            #Get the game from the response
            game = response[2]

            check = checkgame(str(game)) #Check the game for a winner

            #Check if someone won
            if(check != False):

                #Check if the player X won
                if(check == "X"):
                    #Send "youWin" for the winner, and closes the socket
                    data = "youWin"
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                    #Send "youLoose" for the loser, and closes the socket
                    data = "youLoose " + str(game)
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                #Check if the player O won
                else:
                    #Send "youWin" for the winner, and closes the socket
                    data = "youWin"
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                    #Send "youLoose" for the loser, and closes the socket
                    data = "youLoose " + str(game)
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                #If someone won, then finish the thread
                break

        #Sen the data of the game to player O
        data = "yourTurn O " + game

        # Get the response from player O
        players_data["playerO"]["connection"].send(data.encode())
        response = players_data["playerO"]["connection"].recv(1024).decode().split()

        #If the code of message is "play", then make the move
        if (response[0] == "play"):

            #Get the game from the response
            game = response[2]

            check = checkgame(str(game)) #Check the game for a winner

            #Check if someone won
            if (check != False):

                #Check if the player X won
                if (check == "X"):

                    #Send "youWin" for the winner, and closes the socket
                    data = "youWin"
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                    #Send "youLoose" for the loser, and closes the socket
                    data = "youLoose " + str(game)
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                #Check if the player O won
                else:
                    #Send "youWin" for the winner, and closes the socket
                    data = "youWin"
                    players_data["playerO"]["connection"].send(data.encode())
                    players_data["playerO"]["connection"].close()

                    #Send "youLoose" for the loser, and closes the socket
                    data = "youLoose " + str(game)
                    players_data["playerX"]["connection"].send(data.encode())
                    players_data["playerX"]["connection"].close()

                #If someone won, then finish the thread
                break


#This function will wait for new players
def run_server():

    #Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    #Uses the port 69
    port = 69

    #Create the queue of players, and some control variables
    clients = {}
    games = {}
    player_queue = []

    #Make the socket listen on the given port
    s.bind(('', port))
    s.listen(10)
    print("socket is listening")

    #Make the server listen for new players
    while True:
        if (len(player_queue) < 2):
            #Acept new connections and get their names
            c, addr = s.accept()
            name = c.recv(1024).decode()
            #The server will only accept players, when the name lenght is bigger than 0
            if(len(name) > 0):
                #Get the game from the message
                name = name.split()[1]

                #Saves the name and the connection for future use
                clients[name] = {"userName": name, "addr": addr, "connection": c}

                print('Got connection from', addr)

                #Send a response for the client
                clients[name]["connection"].send('OK'.encode())

                #Put the player on the player queue
                player_queue.append(str(name))
                print(player_queue)

        #If there's 2 players on the queue then, make the players play with each other
        else:
            #Get the name of the players from te queue
            playerX = player_queue[0]
            playerO = player_queue[1]

            #Get the data of the players from the database
            players_data = {"playerO": clients[playerO], "playerX": clients[playerX]}

            #Removes the players from the queue
            player_queue.pop(0)
            player_queue.pop(0)

            #Start a new thread of the function playgame, with the data of the players
            threading.Thread(target=playgame, args=(playerX, playerO, players_data)).start()

            print("Created a new thread")

#Runs the server
run_server()
