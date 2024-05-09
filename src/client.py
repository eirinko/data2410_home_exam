from socket import *
from header import *
import datetime
from server import receive_packet

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
    try:
        serverAddress, header, data, seq, ack, flags = receive_packet(clientSocket)
        
        if (Header.syn_flag(flags) and Header.ack_flag(flags)):
            print("SYN-ACK packet is received")
            
            #After SYN-ACK is received, send an ACK:
            ackheader = Header(sequence_number,acknowledgment_number,ackflag,header_format)
            data = b''
            packet = ackheader.create_packet(ackheader.get_header(),data)
            clientSocket.sendto(packet, (ip, port))
            print("ACK packet is sent")
            print("Connection established\n")
            return True
        else:
            print("No SYN-ACK packet received.")
            return False
    except Exception as e:
        print(f"Timeout exception: {e}.")
        clientSocket.close()

def connection_teardown(clientSocket, ip, port):
    print("Connection Teardown:\n")
    seq = 0
    ack = 0
    data = b''
    finheader = Header(seq,ack,finflag,header_format)
    packet = finheader.create_packet(finheader.get_header(),data)
    clientSocket.sendto(packet,(ip,port))
    print("FIN packet is sent")
    
    #Check if an ACK is received.
    try:
        serverAddress, header, data, seq, ack, flags = receive_packet(clientSocket)
        
        if flags == ackflag:
            print("ACK packet is received")
            clientSocket.close()
            print("Connection Closes")
            
    except TimeoutError as e:
        print(f"Didn't receive an ACK for the FIN. Exception: {e}")

def prepare_packets(file):
    seq = 1
    ack = 0
    opened_file = open(file,"rb")
    data = opened_file.read(994)
    packets = []
    while data:
        synheader = Header(seq,ack,synflag,header_format)
        packet = synheader.create_packet(synheader.get_header(),data)
        packets.append(packet)
        data = opened_file.read(994)
        seq+=1
    return packets

def clientFunction(ip, port, file, window):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Connection Establishment Phase:\n")
    
    if successful_handshake(clientSocket, ip, port):
        #Creating a list of all the packets that will be sent
        packets = prepare_packets(file)
        lowest_seq = 1
        highest_seq = window
        
        print("Data Transfer:\n")
        #TODO: Add sliding window information to the printed string.
        for i in range(lowest_seq-1,highest_seq): #To reflect index of packets
            seq = i+1
            clientSocket.sendto(packets[i],(ip,port))
            print(f"{datetime.datetime.now().time()} -- packet with seq = {seq} is sent, sliding window ...")
        while True:
            #TODO: What if the cumulative window size of file is smaller than window size?
            try:
                #What happens if an ACK disappear? 
                serverAddress, header, data, seq, ack, flags = receive_packet(clientSocket)
                if (ack==lowest_seq):
                    print(f"{datetime.datetime.now().time()} -- ACK for packet = {ack} is received")
                    lowest_seq+=1
                    if (len(packets)>highest_seq):
                        clientSocket.sendto(packets[highest_seq],(ip,port))
                        highest_seq+=1
                        print(f"{datetime.datetime.now().time()} -- packet with seq = {highest_seq} is sent")
                    elif (len(packets)==ack):
                        print("DATA Finished\n")
                        connection_teardown(clientSocket,ip,port)
                        break
                else:
                    clientSocket.sendto(packets[ack],(ip,port))
                    print(f"{datetime.datetime.now().time()} -- packet with seq = {seq} is sent")
                    #TODO: def sendPacket(packet), but might be to many variations?
            except Exception as e:
                print(f"Wasn't able to receive any acks. Exception: {e}")
    else:
        print("The handshake was unsuccessful.")