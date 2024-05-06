from socket import *
from header import *

header_format = '!HHH'
sequence_number = 0
acknowledgment_number = 0



def clientFunction(ip, port):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Connection Establishment Phase:")
    
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
    print(flags)
    if (Header.syn_flag(flags) and Header.ack_flag(flags)):
        print("SYN-ACK packet is received")
        
        #After SYN-ACK is received, send an ACK:
        flags = 4
        ackheader = Header(sequence_number,acknowledgment_number,flags,header_format)
        data = b''
        packet = ackheader.create_packet(ackheader.get_header(),data)
        clientSocket.sendto(packet, (ip, port))
        print("ACK packet is sent")
        
        #Send file
        
        
    else:
        print("No SYN-ACK packet received.")
    #message = input('Input lowercase sentence:')
    #   opened_file = file.open("rb")
    
    #clientSocket.sendto(message.encode(), (ip, port))
    #modifiedMessage, serverAddress = clientSocket.recvfrom(1000)
    #print (modifiedMessage.decode())
    clientSocket.close()