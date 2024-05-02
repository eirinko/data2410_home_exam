from socket import *
def serverFunction(ip, port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    print ('The server is ready to receive')
    while True:
        message, clientAddress = serverSocket.recvfrom(1000)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(),clientAddress)