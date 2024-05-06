from socket import *
from header import *

header_format = '!HHH'
sequence_number = 0
acknowledgment_number = 0

def successful_handshake(clientSocket, ip, port):
    #Sending SYN flag.
    flags = 8 #Change this to something that makes more sense? Instead of 8, have syn_flag_active()
    synheader = Header(sequence_number,acknowledgment_number,flags,header_format)
    data = b''
    packet = synheader.create_packet(synheader.get_header(),data)
    clientSocket.sendto(packet, (ip, port))
    print("SYN packet is sent")
    
    #Check if a SYN-ACK is received.
    synackpacket, serverAddress = clientSocket.recvfrom(1000)
    #synackpacket = coded_synackpacket.decode()
    
    header, data = Header.unpack_packet(synackpacket,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    
    if (Header.syn_flag(flags) and Header.ack_flag(flags)):
        print("SYN-ACK packet is received")
        
        #After SYN-ACK is received, send an ACK:
        flags = 4
        ackheader = Header(sequence_number,acknowledgment_number,flags,header_format)
        data = b''
        packet = ackheader.create_packet(ackheader.get_header(),data)
        clientSocket.sendto(packet, (ip, port))
        print("ACK packet is sent")
        return True
    else:
        print("No SYN-ACK packet received.")
        return False
    
def clientFunction(ip, port, file):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Connection Establishment Phase:")
    
    if successful_handshake(clientSocket, ip, port):
        opened_file = open(file,"rb")
        data = opened_file.read(994)
        while data:
            #Send data. 
            clientSocket.sendto(data,(ip,port))
        file.close()
    else:
        print("The handshake was unsuccessful.")
    clientSocket.close()