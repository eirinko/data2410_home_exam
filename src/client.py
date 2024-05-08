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
    print("Client: SYN packet is sent")
    #Check if a SYN-ACK is received.
    try:
        clientSocket.settimeout(0.5)
        synackpacket, serverAddress = clientSocket.recvfrom(1000)
        header, data = Header.unpack_packet(synackpacket,header_format)
        seq, ack, flags = header.parse_header()
        
        if (Header.syn_flag(flags) and Header.ack_flag(flags)):
            print("Client: SYN-ACK packet is received")
            
            #After SYN-ACK is received, send an ACK:
            ackheader = Header(sequence_number,acknowledgment_number,ackflag,header_format)
            data = b''
            packet = ackheader.create_packet(ackheader.get_header(),data)
            clientSocket.sendto(packet, (ip, port))
            print("Client: ACK packet is sent")
            print("Client: Connection established")
            return True
        else:
            print("Client: No SYN-ACK packet received.")
            return False
    except Exception as e:
        print(f"Client: Timeout exception: {e}.")
        clientSocket.close()

def connection_teardown(clientSocket, ip, port):
    print("Client: Connection Teardown:")
    seq = 0
    ack = 0
    data = b''
    finheader = Header(seq,ack,finflag,header_format)
    packet = finheader.create_packet(finheader.get_header(),data)
    clientSocket.sendto(packet,(ip,port))
    print("Client: FIN packet is sent")
    
    #Check if an ACK is received.
    try:
        clientSocket.settimeout(0.5)
        ackpacket, serverAddress = clientSocket.recvfrom(1000)
        header, data = Header.unpack_packet(ackpacket,header_format)
        seq, ack, flags = header.parse_header()
        
        if flags == ackflag:
            print("Client: FIN packet is received")
            clientSocket.close()
            print("Client: Connection Closes")
            
    except Exception as e:
        print(f"Client: Didn't receive an ACK for the FIN. Exception: {e}")

def clientFunction(ip, port, file, window):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Client: Connection Establishment Phase:")
    
    if successful_handshake(clientSocket, ip, port):
        opened_file = open(file,"rb")
        seq = 1
        ack = 0
        lowest_seq = 1
        highest_seq = window

        #Creating a list of all the packets that will be sent
        data = opened_file.read(994)
        packets = []
        while data:
            synheader = Header(seq,ack,synflag,header_format)
            packet = synheader.create_packet(synheader.get_header(),data)
            packets.append(packet)
            data = opened_file.read(994)
            seq+=1
        print(f"Antall packets: {len(packets)}")
        
        print("Client: Data Transfer:")
        for i in range(lowest_seq-1,highest_seq): #To reflect index of packets
            seq = i+1
            clientSocket.sendto(packets[i],(ip,port))
            print(f"{datetime.datetime.now()} -- packet with seq = {seq} is sent")
            
        while True:
            #TODO: What if the cumulative window size of file is smaller than window size?
            try:
                clientSocket.settimeout(0.5)
                synackpacket, serverAddress = clientSocket.recvfrom(1000)
                header, data = Header.unpack_packet(synackpacket,header_format)
                seq, ack, flags = header.parse_header()
                
                if (ack==lowest_seq):
                    lowest_seq+=1
                    if (len(packets)>highest_seq):
                        highest_seq+=1
                        clientSocket.sendto(packets[highest_seq-1],(ip,port))
                        print(f"{datetime.datetime.now()} -- packet with seq = {highest_seq} is sent")
                    elif (len(packets)==highest_seq):
                        connection_teardown(clientSocket,ip,port)
                        print("Client: Connection stopped")
                        break
                else:
                    #TODO: def from_seq_to_index()
                    clientSocket.sendto(packets[ack],(ip,port))
                    print(f"{datetime.datetime.now()} -- packet with seq = {seq} is sent")
                    #TODO: def sendPacket()
                    
            except Exception as e:
                print(f"Client: Wasn't able to receive any acks. Exception: {e}")
        print("Client: DATA Finished")
    else:
        print("Client: The handshake was unsuccessful.")