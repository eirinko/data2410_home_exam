from socket import *
from header import *
import datetime

header_format = '!HHH'

finflag = 2
ackflag = 4
finackflag = 6
synflag = 8
synackflag = 12

def successful_handshake(serverSocket):
    #Three-way handshake
    #Starting with checking the flags of the received packet
    packet, clientAddress = serverSocket.recvfrom(1000)
    header, data = Header.unpack_packet(packet,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    if (Header.syn_flag(flags)):
        print("SYN packet is received")
        sequence_number = 0
        acknowledgment_number = 0
        headerObject = Header(sequence_number,acknowledgment_number,synackflag,header_format)
        data = b''
        packet = headerObject.create_packet(headerObject.get_header(),data)
        serverSocket.sendto(packet,clientAddress)
        print("SYN-ACK packet is sent")
        
        #Checking the flags of the next received packet.
        packet, clientAddress = serverSocket.recvfrom(1000)
        header, data = Header.unpack_packet(packet,header_format)
        seq, ack, flags = Header.parse_header(header_format, header)
        if (Header.ack_flag(flags)):
            print("ACK packet is received")
            print("Connection established")
            return True
        else:
            print("No ACK received.")
            return False
    else:
        print("No SYN received.")
        return False

def connection_teardown(serverSocket, clientAddress):
    #Create FIN-ACK packet.
    header = Header(0,0,finackflag,header_format)
    data = b''
    packet = header.create_packet(header.get_header(),data)
    
    #Sending FIN-ACK packet before closing connection
    serverSocket.sendto(packet,clientAddress)
    serverSocket.close()

def serverFunction(ip, port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    print ('The server is ready to receive')
    file = open("result.jpg","wb")
    #Go-Back-N function:
    #The receiver receives frames in order, sending an ACK for each one. 
    #If it receives a frame out of order, it discards 
    #it and re-sends an ACK for the last correct frame.
    if successful_handshake(serverSocket):
        while True:
            packet, clientAddress = serverSocket.recvfrom(1000)
            header, data = Header.unpack_packet(packet,header_format)
            seq, ack, flags = Header.parse_header(header_format, header)
            
            if Header.fin_flag(flags):
                connection_teardown(serverSocket, clientAddress)
                break
            
            file.write(data)
            print(f"{datetime.datetime.now()} packet {seq} is received")
            
            #Create SYN-ACK packet.
            header = Header(seq,seq,synackflag,header_format)
            data = b''
            packet = header.create_packet(header.get_header(),data)
            
            #Send SYN-ACK packet.
            serverSocket.sendto(packet,clientAddress)
            print(f"{datetime.datetime.now()} sending ack for the received {seq}")