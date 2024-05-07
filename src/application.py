import sys
import argparse
from socket import *
import client
import server
from inputtest import *
from header import *

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

if not port_ok(args.port):
    print("Invalid port. It must be within the range [1024,65535]")
elif not ip_ok(args.ip):
    print("Invalid IP. It must in this format: 10.1.2.3")
else:
    if args.server and args.client:
        print("You cannot use both at the same time.")
    elif args.server:
        server.serverFunction(args.ip,args.port)
        print(f"The server is running with IP address = {args.ip} and port address = {args.port}.")
    elif args.client and args.file:
        try:
            client.clientFunction(args.ip, args.port, args.file)
            print(f"The client is running with IP address = {args.ip} and port address = {args.port}. Transferring file: {args.file}.")
            print("Sending file packets.")
        except Exception as e:
            print(f"ClientFunction did not function: {e}")
    elif args.client:
        print("You must provide filename of the file you want to send.")
    else:
        print("You should run either in server or client mode.")

if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    #main()