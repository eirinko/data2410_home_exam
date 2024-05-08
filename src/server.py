from socket import *
from header import *
import datetime
import os

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
        print("Server: SYN packet is received")
        sequence_number = 0
        acknowledgment_number = 0
        headerObject = Header(sequence_number,acknowledgment_number,synackflag,header_format)
        data = b''
        packet = headerObject.create_packet(headerObject.get_header(),data)
        serverSocket.sendto(packet,clientAddress)
        print("Server: SYN-ACK packet is sent")
        
        #Checking the flags of the next received packet.
        packet, clientAddress = serverSocket.recvfrom(1000)
        header, data = Header.unpack_packet(packet,header_format)
        seq, ack, flags = Header.parse_header(header_format, header)
        if (Header.ack_flag(flags)):
            print("Server: ACK packet is received")
            print("Server: Connection established")
            return True
        else:
            print("Server: No ACK received.")
            return False
    else:
        print("Server: No SYN received.")
        return False

def connection_teardown(serverSocket, clientAddress):
    #Create ACK packet.
    header = Header(0,0,ackflag,header_format)
    data = b''
    packet = header.create_packet(header.get_header(),data)
    
    #Sending ACK packet before closing connection
    serverSocket.sendto(packet,clientAddress)
    serverSocket.close()

def serverFunction(ip, port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    print ('The server is ready to receive')
    file = open("result.jpg","wb")
    #Go-Back-N function:
    #The receiver receives frames in order, sending an ACK for each one. 
    #If it receives a frame out of order, it discards it
    #and re-sends an ACK for the last correct frame.
    if successful_handshake(serverSocket):
        last_seq_acked = 0
        while True:
            try:
                serverSocket.settimeout(0.5)
                packet, clientAddress = serverSocket.recvfrom(1000)
                header, data = Header.unpack_packet(packet,header_format)
                seq, ack, flags = Header.parse_header(header_format, header)
                
                if Header.fin_flag(flags):
                    connection_teardown(serverSocket, clientAddress)
                    break
                elif seq==last_seq_acked+1:
                    print(f"Server: {datetime.datetime.now()} -- packet {seq} is received")
                    file.write(data)
                    last_seq_acked=seq
                else: 
                    print(f"Server: {datetime.datetime.now()} -- out-of-order packet {seq} is received")
                #Create and send ACK packet.
                header = Header(seq,last_seq_acked,ackflag,header_format)
                data = b''
                packet = header.create_packet(header.get_header(),data)
                serverSocket.sendto(packet,clientAddress)
            except Exception as e:
                print(f"Exception: {e}")
        
        # Used code from this place: https://blog.enterprisedna.co/how-to-get-file-size-in-python-a-quick-guide/
        file_path = 'result.jpg'
        try:
            file_size = os.path.getsize(file_path)
            #TODO: should change this so the file size is in kB or MB
            print(f"File Size in Bytes is {file_size}")
        except FileNotFoundError:
            print("File not found.")
        except OSError:
            print("OS error occurred.")