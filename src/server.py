from socket import *
from header import *
import datetime

header_format = '!HHH'
sequence_number = 0
acknowledgment_number = 0

def successful_handshake(serverSocket):
    #Three-way handshake
    #Starting with checking the flags of the received packet
    packet, clientAddress = serverSocket.recvfrom(1000)
    header, data = Header.unpack_packet(packet,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    if (Header.syn_flag(flags)):
        print("SYN packet is received")
        synackflag = 12
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

#Not done yet.
def tear_down_connection():
    return False

def serverFunction(ip, port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    print ('The server is ready to receive')
    
    file = open("result.jpg","wb")
    
    if successful_handshake(serverSocket):
        while True:
            packet, clientAddress = serverSocket.recvfrom(1000)
            header, data = Header.unpack_packet(packet,header_format)
            seq, ack, flags = Header.parse_header(header_format, header)
            
            if Header.fin_flag(flags):
                break
            
            file.write(data)
            print(f"{datetime.datetime.now()} packet {seq} is received")
            
            #Create ACK packet.
            flag = 4 #ACK flag set.
            header = Header(seq,seq,flag,header_format)
            data = b''
            packet = header.create_packet(header.get_header(),data)
            #Send ACK packet.
            serverSocket.sendto(packet,clientAddress)
            print(f"{datetime.datetime.now()} sending ack for the received {seq}")
            
        tear_down_connection()
        serverSocket.close()