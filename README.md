# Projeto Final de Redes

Este repositório é referente ao projeto final 
da disciplina de Redes de Computadores da 
Universidade Federal de Alagoas, ministrada 
pelo professor Leandro Sales de Melo.
<br><br>
O projeto consiste em um jogo da velha com conceitos de rede 
implementados.
A implementação da conexão foi feita usando funções primitivas
de bibliotecas nativas do python: sockets e thread. Enquanto
a interface gráfica e interatividade do jogo foram feitas usando
as bibliotecas pygame e tkinter.

<br>
Autoria do projeto

* Rafael Emílio Lima Alves
* Wagner Anthony de Medeiros Silva
<br>

## Execução do projeto

### Pré requisitos
* Biblioteca pygame instalada na máquina;
* Biblioteca tkinter instalada na máquina;
* Todas as máquinas com instâncias abertas 
  estarem conectadas na mesma rede local;

<br>
### Instruções
Para executar o projeto primeiro é necessário o 
download desse repositório compactado e a descompactação
do mesmo nas máquinas nas quais você pretende execultá-lo.
<br><br>
Após isso, deve ser executado o arquivo **server.py**, dando início
ao servidor. (O servidor deve ser execultado apenas uma vez e 
em uma das máquinas conectadas na rede local).
<br><br>
Com o servidor em execução, deve ser executado o arquivo main.py.
A execução do mesmo pode ser feito de variadas formas, mas a mais 
aconselhável é através do terminal ou de uma IDE como o pycharm.
<br><br>
Após iniciar quantas instâncias forem necessárias da **main.py** 
nas máquinas, irá aparecer uma janela solicitando um nome de usuário
que **não deve conter espaçamento**. Após autenticar um nome de usuário
válido com o servidor aberto, a janela do menu inicial do jogo será gerada.
<br><br>
Para iniciar uma partida, deve ser pressionada a **tecla espaço** na janela
do menu principal do jogo. Então o usuário será direcionado à uma sala de
espera até que o segundo jogador conecte, quando isso ocorrer a partida
terá início. 
<br><br>
A marcação no tabuleiro é feita usando o **mouse**, basta que o jogador **clique
com o botão esquerdo** na casa onde deseja demarcar seu símbolo. A partida 
inicia com o movimento do jogador "X", após ele fazer um movimento válido, 
a vez passará para o jogador "O" e assim consecutivamente até o fim da partida.
É válido citarque o jogador só pode fazer seu movimento na sua vez, pois nesse 
jogo não há o conceito de "pre-move".
<br><br>
O fim da partida ocorre em caso de vitória de um dos jogadores ou empate, em qualquer
dessas circunstâncias o jogador será direcionado à tela do resultado da partida.
Para iniciar uma nova partida basta retroceder ao menu principal pressionando 
a **tecla R** e após isso repetir todo o processo.
<br>
## Referências
- [Documentação da biblioteca Threading](https://docs.python.org/3/library/threading.html)
- [Documentação da biblioteca Sockets](https://docs.python.org/3/library/socket.html)
- [Documentação da biblioteca Tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
- [Site principal com documentação do Pygame](https://www.pygame.org/docs/)

