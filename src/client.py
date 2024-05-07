from socket import *
from header import *
import datetime

header_format = '!HHH'
finflag = 2
ackflag = 4
finackflag = 6
synflag = 8
synackflag = 12

def successful_handshake(clientSocket, ip, port):
    sequence_number = 0
    acknowledgment_number = 0
    synheader = Header(sequence_number,acknowledgment_number,synflag,header_format)
    data = b''
    packet = synheader.create_packet(synheader.get_header(),data)
    clientSocket.sendto(packet, (ip, port))
    print("SYN packet is sent")
    
    #Check if a SYN-ACK is received.
    synackpacket, serverAddress = clientSocket.recvfrom(1000)
    header, data = Header.unpack_packet(synackpacket,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    
    if (Header.syn_flag(flags) and Header.ack_flag(flags)):
        print("SYN-ACK packet is received")
        
        #After SYN-ACK is received, send an ACK:
        ackheader = Header(sequence_number,acknowledgment_number,ackflag,header_format)
        data = b''
        packet = ackheader.create_packet(ackheader.get_header(),data)
        clientSocket.sendto(packet, (ip, port))
        print("ACK packet is sent")
        return True
    else:
        print("No SYN-ACK packet received.")
        return False

def connection_teardown(clientSocket, ip, port):
    print("Connection Teardown:")
    seq = 0
    ack = 0
    data = b''
    finheader = Header(seq,ack,finflag,header_format)
    packet = finheader.create_packet(finheader.get_header(),data)
    clientSocket.sendto(packet,(ip,port))
    print("FIN packet is sent")
    
    #Check if a FIN-ACK is received.
    finackpacket, serverAddress = clientSocket.recvfrom(1000)
    header, data = Header.unpack_packet(finackpacket,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    if flags == finackflag:
        print("FIN ACK packet is received")
        clientSocket.close()
        print("Connection Closes")

def clientFunction(ip, port, file, window):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Connection Establishment Phase:")
    
    if successful_handshake(clientSocket, ip, port):
        opened_file = open(file,"rb")
        data = opened_file.read(994)
        seq = 1
        ack = 0
        print("Data Transfer:")
        while data:
            #Now it just sends all the information without waiting for acks. 
            synheader = Header(seq,ack,synflag,header_format)
            packet = synheader.create_packet(synheader.get_header(),data)
            
            clientSocket.sendto(packet,(ip,port))
            print(f"{datetime.datetime.now()} -- packet with seq = {seq} is sent")
            
            data = opened_file.read(994)
            seq+=1
        opened_file.close()
        print("DATA Finished")
        
        #After sending all the data, we stop the connection. 
        connection_teardown(clientSocket, ip, port)
        print("Connection stopped")
    else:
        print("The handshake was unsuccessful.")
    clientSocket.close()