from socket import *
from header import *

import time
import utils

g_start_time = None
end_time = None

'''Function listening for initiation of a three-way handshake: It receives the parameter serverSocket.
Once it receives something over UDP, it unpacks and checks the flags. If it received a SYN-flag it will
send back a SYN-ACK-packet over UDP. In the end it waits for a new packet with ACK-flag.
If it receives an ACK-flag the connection is established and it returns True. Otherwise, return False.'''
def successful_handshake(serverSocket):
    clientAddress, _, data, _, _, flags = utils.receive_packet(serverSocket)
    
    #Only proceed with handshake if the SYN-flag is activated.
    if (flags == SYNFLAG):
        global g_start_time
        g_start_time = time.time()
        
        print("SYN packet is received")
        header = Header(flags=SYNACKFLAG)
        data = b''
        packet = utils.create_packet(header.get_header(), data)
        serverSocket.sendto(packet,clientAddress)
        print("SYN-ACK packet is sent")
        clientAddress, header, data, _, _, flags = utils.receive_packet(serverSocket)
        
        #Only proceed with handshake if the ACK-flag is activated.
        if (flags == ACKFLAG):
            print("ACK packet is received")
            print("Connection established")
            return True
        else:
            print("No ACK received.")
            return False
    else:
        print("No SYN received.")
        return False


'''Function completing the connection teardown, after initiated by client.
Parameters: server socket and client address. Returns nothing.'''
def connection_teardown(serverSocket, clientAddress):
    #Create FIN-ACK packet.
    header = Header(flags=FINACKFLAG)
    data = b''
    packet = utils.create_packet(header.get_header(),data)
    
    #Sending FIN-ACK packet to confirm connection teardown
    serverSocket.sendto(packet,clientAddress)
    print("FIN ACK packet is sent\n")


'''Function for initiating server, connecting to a client, 
receiving packets and assembling data to a file and tearing down connection.
It starts a UDP socket, and uses a three-way handshake to connect
with the client. Will listen for packets until it receives a packet with a FIN-flag, 
then it will stop the connection. 
If it receives a packet out of order, it will send the ACK for the last in-order packet. 
The data from the packets (that are not part of handshake and connection teardown) 
will be assembled into a file.'''
def serverFunction(ip, port, discard):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    
    #Creating a file where data from the received packets can be appended.
    file = open("result.jpg","wb")
    
    if successful_handshake(serverSocket):
        last_seq_acked = 0
        
        while True:
            out_of_order = False
            try:
                serverSocket.settimeout(0.5)
                clientAddress, header, data, seq, ack, flags = utils.receive_packet(serverSocket)
                
                if flags == FINFLAG:
                    print("FIN packet is received")
                    connection_teardown(serverSocket, clientAddress)
                    
                    #Stopping the timer.
                    end_time = time.time()
                    utils.print_throughput(g_start_time, end_time)
                    
                    print("Connection closes")
                    serverSocket.close()
                    break
                
                if seq == discard:
                    discard = -1
                    out_of_order = True
                    
                elif seq == last_seq_acked+1:
                    print(f"{utils.timestamp()} -- packet {seq} is received")
                    file.write(data)
                    last_seq_acked = seq
                    
                else: 
                    out_of_order = True
                    print(f"{utils.timestamp()} -- out-of-order packet {seq} is received")
                    
            except TimeoutError as e:
                #TODO: This is never in the print.
                print(f"{utils.timestamp()} -- Exception: {e}")
            
            #Create and send ACK packet.
            #TODO: Check if I need these try, except here. 
            try:
                if not out_of_order:
                    header = Header(ack=last_seq_acked,flags=ACKFLAG)
                    data = b''
                    packet = utils.create_packet(header.get_header(),data)
                    serverSocket.sendto(packet,clientAddress)
                    print(f"{utils.timestamp()} -- sending ack for the received {last_seq_acked}")

            except TimeoutError as e:
                print(f"Tried to send ACK for packet {last_seq_acked}, but failed: {e}")