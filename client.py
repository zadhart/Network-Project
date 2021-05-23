import socket

#This function return a message, that will be sent to the server
#Rafa essa função vc pode só colocar junto com suas putras funções onde quer que vc coloque
# o código da run_client()s
def play_game(game, who):

    #Rafa aqui vc tem que colocar a matrix depois da jogada convertida em uma string para enviar para o servidor
    #tipo 000000000 lembre que 2 = O e 5 = X
    #vc pode apagar esse input e passar a matrix direto como parametro da função
    game = str(input("Digite o jogo: "))

    #Aqui ele vai retornar a mensagem formatada tipo: play X 000050000
    return str("play " + who + " " + game)


def run_client():
    #Rafa aqui vc tem que pegar o nome do usuário direto da tela do tKinter e colocar nessa parte do input
    msg = "newUser " + input("Username:")

    #Rafa isso aqui serve para saber o ip da máquina que está rodando o servidor
    ip = str(input("Digite o ip do servidor: "))

    #Vc pode mudar a porta mas tem que colocar a msm porta no codigo do servidor
    port = 69

    #Esse who é importante eu acho mas nn está sendo utilizado mas é melhor nn tirar
    who = None

    #Essa parte cria o socket e conecta com o servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ip, port))
    print("connected")

    # This send the user name
    s.send(msg.encode())

    while True:
        #O cliente sempre está pronto para receber uma mensagem do servidor, e ele vai transformar a mensagem em uma
        #lista de strings
        data = s.recv(1024).decode().split()

        #Se a lista é maior do que 0 então o cliente realmente recebeu uma mensagem
        if (len(data) > 0):
            #Se a mensagem é yourTurn ele vai chamar a função que pede para o usuário fazer a jogada
            #A mensagem enviada pelo servidor é tipo: yourTurn X 000000000
            if (data[0] == "yourTurn"):
                print(data[2])
                s.send(play_game(data[2], data[1]).encode())

            #Aqui vc só tem que mostrar a tela de vitoria quando o servidor mandar essa mensagem
            #E depois encerre o jogo como vc bem entender
            elif (data[0] == "youWin"):
                print("Nice Job")
                s.close()
                break

            #Msm coisa só que dessa vez mostre a tela de derrota
            elif (data[0] == "youLoose"):
                print("GG EASY NOOOOOB")
                s.close()
                break

            #Essa mensagem vc pode usar como uma verificação para sair da tela de espera e começar o jogo
            #A mensagem enviada é tipo: begin Fulano Cicrano 000000000
            elif (data[0] == "begin"):
                print(data[1] + " vs " + data[2])
                print("game: " + data[3])

#Isso aqui chama a função que roda o client, vc pode tirar se quiser
#mas vai precisar copiar o código da run_client() para um função do seu código
run_client()

