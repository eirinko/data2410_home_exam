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
    #Create ACK packet.
    header = Header(flags=ACKFLAG)
    data = b''
    packet = utils.create_packet(header.get_header(),data)
    
    #Sending ACK packet to confirm connection teardown
    serverSocket.sendto(packet,clientAddress)
    print("ACK packet is sent\n")


'''Function for initiating server: starting a UDP socket and using a three-way handshake to connect
with the client. Will listen for packets until it receives a packet with a FIN-flag, then it will stop the connection.
If it receives a packet out of order, it will send the ACK for the last in-order packet. 
The data from the packets will be appended to the result.jpg file. 
It sends and resends ACK packets based on the last in-order packet received.'''
def serverFunction(ip, port, discard):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    
    #Creating a file where data from the received packets can be appended.
    file = open("result.jpg","wb")
    
    if successful_handshake(serverSocket):
        last_seq_acked = 0
        while True:
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
                
                if seq==discard:
                    discard=-1
                elif seq==last_seq_acked+1:
                    print(f"{utils.timestamp()} -- packet {seq} is received")
                    file.write(data)
                    last_seq_acked=seq
                else: 
                    print(f"{utils.timestamp()} -- out-of-order packet {seq} is received")
            except Exception as e:
                print(f"Exception: {e}")
            
            #Create and send ACK packet.
            try:
                header = Header(ack=last_seq_acked,flags=ACKFLAG) # header.create_packet_ack_header(last_seq_acked)
                data = b''
                packet = utils.create_packet(header.get_header(),data)
                serverSocket.sendto(packet,clientAddress)
                print(f"{utils.timestamp()} -- sending ack for the received {last_seq_acked}")
            except Exception as e:
                print(f"Tried to send ACK for packet {last_seq_acked}, but failed: {e}")