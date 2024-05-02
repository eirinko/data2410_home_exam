from socket import *

def clientFunction(ip, port, file):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Connection Establishment Phase:")
    message = input('Input lowercase sentence:')
    #opened_file = file.open("rb")
    
    clientSocket.sendto(message.encode(), (ip, port))
    modifiedMessage, serverAddress = clientSocket.recvfrom(1000)
    print (modifiedMessage.decode())
    clientSocket.close()