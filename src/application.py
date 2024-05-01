import sys
import argparse
from socket import *


#For defining server and client functions, I'm using a modified version of code from the obligatory assignment 2.
def functionServer():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a server socket
    server_port = 8000
    server_ip = '127.0.0.1'
    serverSocket.bind((server_ip, server_port))
    serverSocket.listen(1)

    while True:
        #Establish the connection print('Ready to serve...') connectionSocket, addr = 
        try:
            print("Ready to serve...")
            connectionSocket, addr = serverSocket.accept()
            
            #Receiving message from client
            message = connectionSocket.recv(1024).decode()
            
            #File to be opened
            filename = message.split()[1]
            
            #Opening the file and reading it to outputdata
            f = open(filename[1:])
            outputdata = f.read()

            #Send one HTTP header line into socket
            encoding = 'ascii'
            connectionSocket.send(bytes('HTTP/1.0 200 OK\r\n', encoding))
            connectionSocket.send(bytes('Content-Type: text/html\r\n\r\n', encoding))

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode()) 
            connectionSocket.send("\r\n".encode())
            #Close client socket
            connectionSocket.close()
            #Could add break to stop the server after loading once.
            break
        except IOError:
            #Send response message for file not found
            encoding = 'ascii'
            connectionSocket.send(bytes('HTTP/1.0 404 Not Found\r\n', encoding))
            
            #Close client socket
            connectionSocket.close()
            
    serverSocket.close()
    sys.exit()#Terminate the program after sending the corresponding data
    
def functionClient():
    try:
        #Creating a socket with TCP and a two-way byte stream
        clientSocket = socket(AF_INET,SOCK_STREAM)
        
        #connect to the server and the given IP and Port
        clientSocket.connect((args.ip, args.port))
        
        #Creating a HTTP GET method
        request_header = f"GET / HTTP/1.0\r\nHost: {args.ip}:/{args.port}\r\n{args.filename}\r\n\r\n"
        
        #Sending the GET request to the server
        clientSocket.send(bytes(request_header,"ascii"))
        result = ""
        while True:
            #Read data from the socket
            received_line = clientSocket.recv(1024).decode()
            if not received_line:
                break
            result += received_line
        #The result is printed to the terminal to easily check it.
        print(result)
        #Closing the client socket and the connection
        clientSocket.close()
    except error as e:
        print(f"Something happened {e}")


#Used the code from args.py in oblig 1, with modifications:
parser = argparse.ArgumentParser(description='simple args')

#Adding arguments to the parser:
parser.add_argument('-s' , '--server', type=bool, action='store_true')
parser.add_argument('-c' , '--client', type=bool, action='store_true')
parser.add_argument('-p', '--port', type=int, default=8088) 
parser.add_argument('-i', '--ip', type=str, default="10.0.1.2")
#Added -f
#parser.add_argument('-f', '--file', type=str, required=True)
#Added -w
parser.add_argument('-w', '--window', type=int, default=3) 
#Added -d
parser.add_argument('-d', '--discard', type=int) #Make sure you change the value to an infinitely large 
#number after your first check in order to avoid skipping seq=11 all the time.

args = parser.parse_args()

#Setting up to test if the IP address is in the correct format
test_ip = args.ip.split(".")
notinrange = False
for number in test_ip:
    if int(number) not in range (0,256): # Assuming we want inclusive 0 and inclusive 255. 
        notinrange = True

#First check for the range of the port, assuming we want inclusive 1024 and inclusive 65535.
if args.port not in range(1024,65536):
    print("Invalid port. It must be within the range [1024,65535]")
#Then check for the format of the IP address. 
#If it doesn't contain 4 numbers or the numbers are out of range you get a error message.
elif len(test_ip)!=4 or notinrange:
    print("Invalid IP. It must in this format: 10.1.2.3")
else:
    #Testing if both server and client have been chosen:
    if args.server and args.client:
        print("You cannot use both at the same time")
    elif args.server:
        functionServer()
        print(f"The server is running with IP address = {args.ip} and port address = {args.port}")
    elif args.client:
        functionClient()
        print(f"The client is running with IP address = {args.ip} and port address = {args.port}")
    else:
        print("You should run either in server or client mode")

# Need to add tests for the new arguments. 
# Should always pass a file name, sliding window has a default and discard is optional.
