import sys
import argparse
from socket import *
import client
import server
import inputtest

#Definition of unit tests:
'''
    #Some unit tests
    """
    >>> jfi([10,10,10])
    1.0
    >>> jfi(['bla',10,10])
    bla is not an integer and will not be added
    1.0
    >>> jfi([5,10])
    0.9
    """
'''


#Used the code from args.py in oblig 1, with modifications:
parser = argparse.ArgumentParser(description='simple args')

#Adding arguments to the parser:
parser.add_argument('-s' , '--server', action='store_true')
parser.add_argument('-c' , '--client', action='store_true')
parser.add_argument('-p', '--port', type=int, default=8088) 
parser.add_argument('-i', '--ip', type=str, default="127.0.0.1")
parser.add_argument('-f', '--file', type=str)
parser.add_argument('-w', '--window', type=int, default=3)
parser.add_argument('-d', '--discard', type=int, default=0)
#Make sure you change the value to an infinitely large
#number after your first check, in order to avoid skipping seq=11 all the time.

args = parser.parse_args()

#Setting up to test if the IP address is in the correct format
#test_ip = args.ip.split(".")
#notinrange = False
#for number in test_ip:
#    if int(number) not in range (0,256): # Assuming we want inclusive 0 and inclusive 255. 
#        notinrange = True

if not inputtest.port_ok(args.port):
    print("Invalid port. It must be within the range [1024,65535]")
elif not inputtest.ip_ok(args.ip):
    print("Invalid IP. It must in this format: 10.1.2.3")
else:
    #Testing if both server and client have been chosen:
    if args.server and args.client:
        print("You cannot use both at the same time")
    elif args.server:
        #Run the server:
        server.serverFunction(args.ip,args.port)
        print(f"The server is running with IP address = {args.ip} and port address = {args.port}")
    elif args.client:
        #Run the client:
        client.clientFunction(args.ip, args.port, args.file)
        print(f"The client is running with IP address = {args.ip} and port address = {args.port}. Transferring file: {args.file}.")
    else:
        print("You should run either in server or client mode")

# Need to add tests for the new arguments. 

if __name__ == "__main__":
    import doctest
    doctest.testmod()