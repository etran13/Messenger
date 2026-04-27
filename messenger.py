#Ellie Tran, CSC 376, etran13@depaul.edu

import sys
import socket
import threading

def send(socket):
    print("Starting send")
    while True:
        print("Sending loop entered")
        messageToSend = input("") #Block until input is recieved
        socket.sendall(messageToSend) #Send the message using the socket connection that was passed in

def recieve(socket):
    print("Starting recieve")
    data = None
    while True:
        print("Recv loop entered")
        data = socket.recv(1024) #block until recieved
        if not data: #Check if the message is empty; exit if so
            sys.exit()
        print(f"Recieved: {data.decode()}")

if __name__ == "__main__":
    #Check command line arguments; if -l present do server setup before creating client socket
    hostIP = '10.56.2.249' #The host IP of server VM
    #hostIP = 'localhost'
    portNum = 8080 #Set a default port number
    argument1 = sys.argv[1]
    conn = None
    if argument1 == "-l": #If user has specified that program should be used as server
        try:
            portNum = int(sys.argv[2])
        except:
            pass #Just keep the default number if it errors
        #Do server setup by creating a TCP/IP server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initialServer:
            initialServer.bind((hostIP, portNum))
            initialServer.listen()
            print(f"Server listening on address {hostIP}, port {portNum}")

            conn, addr = initialServer.accept() #Block until a client connects
            print(conn)

    else: #Client setup
        portNum = int(argument1) 
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(conn)
        conn.connect((hostIP, portNum)) 

    #Start chat loop by spawning in sending thread and recieving/printing thread
    recieve(conn) #Begin recieving
    sendingThread = threading.Thread(target=send, args=(conn))
    sendingThread.start() #Begin sending
