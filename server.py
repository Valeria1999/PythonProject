import socket
import threading
import random
import sys
import clientIdentityClass

LOCALHOST = "127.0.0.1"
PORT = 1887
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("[ SERVER ] Let's go")
print("[ SERVER ] Waiting for client's requests ...")



def gameServerOneClient(clientIdentity):
    
    number = random.randint(0,50)
    print("[ SERVER ]", clientIdentity.name,"has to guess the number",number)
    clientIdentity.sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
    plGuess = clientIdentity.sockCl.recv(2048)
    playerGuess = int(plGuess.decode())
    print("[",clientIdentity.name,"] I guess : " ,playerGuess)

    clientQuit = False
    attempts = 0
    while True:
        attempts = attempts + 1
        if playerGuess<number:
            clientIdentity.sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
        if playerGuess>number:
            clientIdentity.sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
        if playerGuess==number:
            clientIdentity.score.append(attempts)
            bestScore = min(clientIdentity.score)
            msg = "ok"+str(bestScore)
            clientIdentity.sockCl.send(bytes(msg,'UTF-8'))             
            print("[ SERVER ] PLayer",clientIdentity.name,"guessd the number in",str(attempts),"attempts")
            break

        playerThink = clientIdentity.sockCl.recv(2048)
        num = playerThink.decode()
        if num.isdigit():
            print("[",clientIdentity.name,"] I guess : " ,int(num))
            playerGuess = int(num)
        else:
            clientQuit = True
            print("[",clientIdentity.name,"] I have to go. Bye!\n")
            break

    if clientQuit == False:
        clientIdentity.score.append(attempts)
        playerByeMsg = clientIdentity.sockCl.recv(2048)




sessionTwoPlayers = []
def gameServerTwoClients():

    if len(sessionTwoPlayers)%2==1:
        print("[ SERVER ] Waiting opponent player for",sessionTwoPlayers[0].name )
        sessionTwoPlayers[0].sockCl.send(bytes("1",'UTF-8'))

    elif len(sessionTwoPlayers)%2==0:
        sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Start Game ...",'UTF-8'))
        sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Start Game ...",'UTF-8'))

        print("\n~ Start GAME between :",sessionTwoPlayers[0].name , "and", sessionTwoPlayers[1].name," ~")
        readyP1 = sessionTwoPlayers[0].sockCl.recv(2048)
        readyP2 = sessionTwoPlayers[1].sockCl.recv(2048)
        print(readyP1.decode())


        # player1 give the number | player2 guess the number
        sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Give me an number between [0,50 ]: __",'UTF-8'))
        numberForPlayer2 = sessionTwoPlayers[0].sockCl.recv(2048)
        numberForPL2 = int(numberForPlayer2.decode())
        print("[",sessionTwoPlayers[0].name,"] I give the number : " ,numberForPL2 )

        sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
        Player2Guess = sessionTwoPlayers[1].sockCl.recv(2048)
        player2ThinkTheNumber = int(Player2Guess.decode())
        print("[",sessionTwoPlayers[1].name,"] I guess : " ,player2ThinkTheNumber )

        clientQuit = False
        player2Attepmts = 0
        while True:
            player2Attepmts = player2Attepmts + 1
            if player2ThinkTheNumber<numberForPL2:
                sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
            if player2ThinkTheNumber>numberForPL2:
                sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
            if player2ThinkTheNumber==numberForPL2:
                sessionTwoPlayers[1].sockCl.send(bytes("ok",'UTF-8'))
                sessionTwoPlayers[0].sockCl.send(bytes(str(player2Attepmts),'UTF-8'))                
                print("[ SERVER ] PLayer",sessionTwoPlayers[1].name,"guessd the number in",str(player2Attepmts),"attempts")
                break

            player2think = sessionTwoPlayers[1].sockCl.recv(2048)
            num = player2think.decode()
            if num.isdigit():
                print("[",sessionTwoPlayers[1].name,"] I guess : " ,int(num))
                player2ThinkTheNumber = int(num)
            else:
                print("[",sessionTwoPlayers[1].name,"] I have to go. Bye!\n")
                clientQuit = True
                break

        if clientQuit==True:
            sessionTwoPlayers[0].sockCl.send(bytes('exit','UTF-8'))
            singleClient = sessionTwoPlayers[0] 
            sessionTwoPlayers.pop(0)
            sessionTwoPlayers.pop(0)
            gameServerOneClient(singleClient)
        else:

            sessionTwoPlayers[1].score.append(player2Attepmts)


            # player2 give the number | player1 guess the number
            ready1P1 = sessionTwoPlayers[0].sockCl.recv(2048)
            ready1P2 = sessionTwoPlayers[1].sockCl.recv(2048)
            print(ready1P1.decode())

            sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Give me an number between [0,50] : __",'UTF-8'))
            numberForPlayer1 = sessionTwoPlayers[1].sockCl.recv(2048)
            numberForPL1 = int(numberForPlayer1.decode())
            print("[",sessionTwoPlayers[1].name,"] I give the number : ",numberForPL1 )

            sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
            Player1Guess = sessionTwoPlayers[0].sockCl.recv(2048)
            player1ThinkTheNumber = int(Player1Guess.decode())
            print("[",sessionTwoPlayers[0].name,"] I guess : ",player1ThinkTheNumber )
            
            player1Attepmts = 0
            while True:
                player1Attepmts = player1Attepmts + 1
                if player1ThinkTheNumber<numberForPL1:
                    sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
                
                if player1ThinkTheNumber>numberForPL1:
                    sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
    
                if player1ThinkTheNumber==numberForPL1:
                    sessionTwoPlayers[1].sockCl.send(bytes(str(player1Attepmts),'UTF-8'))                
                    sessionTwoPlayers[0].sockCl.send(bytes("ok",'UTF-8'))
                    print("[ SERVER ] PLayer",sessionTwoPlayers[0].name,"guessed the number in",str(player1Attepmts),"attempts")
                    break

                player1think = sessionTwoPlayers[0].sockCl.recv(2048)
                num1 = player1think.decode()
                if num1.isdigit():
                    print("[",sessionTwoPlayers[0].name,"] I guess : " ,int(num1))
                    player1ThinkTheNumber = int(num1)
                else:
                    print("[",sessionTwoPlayers[0].name,"] I have to go. Bye!\n")
                    clientQuit = True
                    break

            if clientQuit==True:
                sessionTwoPlayers[1].sockCl.send(bytes('exit','UTF-8'))
                singleClient = sessionTwoPlayers[1] 
                sessionTwoPlayers.pop(0)
                sessionTwoPlayers.pop(0)
                gameServerOneClient(singleClient)
            else:
                sessionTwoPlayers[0].score.append(player1Attepmts)

                #Players waiting for results
                waitingPl1 = sessionTwoPlayers[0].sockCl.recv(2048)
                waitingPl2 = sessionTwoPlayers[1].sockCl.recv(2048)
                print(waitingPl1.decode())




class Thread(threading.Thread):
    def __init__(self,clientAdr,sockCl):
        threading.Thread.__init__(self)
        self.sockCl = sockCl
        print ("[ SERVER ] New connection created : ", clientAdr)

    def run(self):
        #ask name
        self.sockCl.send(bytes("[ SERVER ] Hi, What's your name ?",'UTF-8'))
        recvName = self.sockCl.recv(2048)
        clientNichName = recvName.decode()
        print ("[ CLIENT ] My name is ",clientNichName)
        preference = 'none'
        clientIdentity = clientIdentityClass.ClientIdentity(self.sockCl,clientNichName,preference)
        
        #ask preference
        self.sockCl.send(bytes("[ SERVER ] Do you want to play with a friend? y/n",'UTF-8'))
        recvPreference = self.sockCl.recv(2048)
        recvPrefere = recvPreference.decode()
        if recvPrefere=='y':
            print ("[",clientNichName,"] I want to play with a friend! ")
            clientIdentity.preference = 'multiPlayer'
        elif recvPrefere=='n':
            print ("[",clientNichName.upper(),"] I want to play with server! ")
            clientIdentity.preference = 'onePlayer'

while True:  
    server.listen(1)
    acceptClient = server.accept()
    socketCl = acceptClient[0]
    clientAdr = acceptClient[1]
    thread = Thread(clientAdr, socketCl)
    thread.start()
