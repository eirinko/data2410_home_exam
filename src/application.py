import sys
import argparse
from socket import *
import client
import server
from utils import *
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
parser.add_argument('-s' , '--server', action='store_true', 
                    help="Option used to invoke server mode. Use either server or client mode, not both.")
parser.add_argument('-c' , '--client', action='store_true', 
                    help="Option used to invoke client mode. Use either server or client mode, not both.")
parser.add_argument('-p', '--port', type=int, default=8088, 
                    help="Use this to choose a port. Default port is 8088.")
parser.add_argument('-i', '--ip', type=str, default="127.0.0.1", 
                    help="Use this to choose an IP address (IPv4). Default IP address is 127.0.0.1.")
parser.add_argument('-f', '--file', type=str,
                    help="Use this in the client mode to choose which file to transfer to the server.")
parser.add_argument('-w', '--window', type=int, default=3, 
                    help="Use this in the client mode to change the moving window size. Default is 3.")
parser.add_argument('-d', '--discard', type=int, default=0,
                    help="Use this in the server mode to discard a specific packet. Used in testing.")

args = parser.parse_args()

if not port_ok(args.port):
    print("Invalid port. It must be within the range [1024,65535]")
elif not ip_ok(args.ip):
    print("Invalid IP. It must in this format: 10.1.2.3")
else:
    if args.server and args.client:
        print("You cannot use both server and client at the same time.")
    elif args.server and args.file:
        print("Use the client for sending a file.")
    elif args.server:
        server.serverFunction(args.ip, args.port, args.discard)
    elif args.client and args.file:
        client.clientFunction(args.ip, args.port, args.file, args.window)
    elif args.client:
        print("You must provide filename of the file you want to send.")
    else:
        print("You should run either in server or client mode.")

if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    #main()