from socket import *

def clientFunction(ip, port):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = input('Input lowercase sentence:')
    clientSocket.sendto(message.encode(), (ip, port))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print (modifiedMessage.decode())
    clientSocket.close()