from socket import *
from header import *
import datetime
import os
import time

header_format = '!HHH'

finflag = 2
ackflag = 4
finackflag = 6
synflag = 8
synackflag = 12

start_time = None
end_time = None

#Three-way handshake
def successful_handshake(serverSocket):
    packet, clientAddress = serverSocket.recvfrom(1000)
    header, data = Header.unpack_packet(packet,header_format)
    seq, ack, flags = header.parse_header()
    
    #Only proceed with handshake if the syn_flag is activated.
    if (Header.syn_flag(flags)):
        print("SYN packet is received")
        sequence_number = 0
        acknowledgment_number = 0
        headerObject = Header(sequence_number,acknowledgment_number,synackflag,header_format)
        data = b''
        packet = headerObject.create_packet(headerObject.get_header(),data)
        serverSocket.sendto(packet,clientAddress)
        print("SYN-ACK packet is sent")
        packet, clientAddress = serverSocket.recvfrom(1000)
        header, data = Header.unpack_packet(packet,header_format)
        seq, ack, flags = header.parse_header()
        
        #Only proceed with handshake if the syn_flag is activated.
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

def print_throughput(start_time, end_time):
    #"Display the throughput based on how much data 
    #was received and how much time elapsed during the connection."
    #Assuming that time elapsed during the connection is from 
    # the client sends the first SYN to the connection is closed.
    
    #As stated in the assignment: For the sake of simplicity, 
    # assume 1 KB = 1000 Bytes, and 1 MB = 1000 KB. 
    try:
        if (end_time == None):
            print("End time not captured. Not possible to calculate Mbps.")
        elif (start_time == None):
            print("Start time not captured. Not possible to calculate Mbps.")
        else:
            total_time = end_time - start_time
        print(f"Total time elapsed: {total_time}")
        
        #Returns size in bytes and will therefore multiply with 8
        file_size = os.path.getsize("result.jpg")*8
        
        #Calculating bits per second
        file_size_ps = file_size/total_time
        
        if (file_size_ps>1000000):
            file_size_ps = file_size_ps/1000000
            unit = "Mbps"
        elif (file_size_ps>1000):
            file_size_ps = file_size_ps/1000
            unit = "Kbps"
        else:
            unit = "bps"
        print(f"The throughput is {file_size_ps:.2f} {unit}")
    except FileNotFoundError:
        print("File not found.")
    except OSError:
        print("OS error occurred.")

def connection_teardown(serverSocket, clientAddress):
    #Create ACK packet.
    header = Header(0,0,ackflag,header_format)
    data = b''
    packet = header.create_packet(header.get_header(),data)
    
    #Sending ACK packet before closing connection
    serverSocket.sendto(packet,clientAddress)
    print("ACK packet is sent\n")

def receive_packet(udpsocket):
    udpsocket.settimeout(0.5)
    packet, address = udpsocket.recvfrom(1000)
    header, data = Header.unpack_packet(packet,header_format)
    seq, ack, flags = header.parse_header()
    return address, header, data, seq, ack, flags

def serverFunction(ip, port, discard):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    
    #Creating a file where data from the received packets can be appended.
    file = open("result.jpg","wb")
    
    if successful_handshake(serverSocket):
        #Starting the timer when the server has connected to the client.
        start_time = time.time()
        
        last_seq_acked = 0
        while True:
            try:
                clientAddress, header, data, seq, ack, flags = receive_packet(serverSocket)
                
                if Header.fin_flag(flags):
                    print("FIN packet is received")
                    connection_teardown(serverSocket, clientAddress)
                    
                    #Stopping the timer.
                    end_time = time.time()
                    print_throughput(start_time, end_time)
                    
                    print("Connection closes")
                    serverSocket.close()
                    break
                
                if seq==discard:
                    discard=-1
                elif seq==last_seq_acked+1:
                    print(f"{datetime.datetime.now().time()} -- packet {seq} is received")
                    file.write(data)
                    last_seq_acked=seq
                else: 
                    print(f"{datetime.datetime.now().time()} -- out-of-order packet {seq} is received")
            except Exception as e:
                print(f"Exception: {e}")
            
            #Create and send ACK packet.
            try:
                header = Header(last_seq_acked,last_seq_acked,ackflag,header_format)
                data = b''
                packet = header.create_packet(header.get_header(),data)
                serverSocket.sendto(packet,clientAddress)
                print(f"{datetime.datetime.now().time()} -- sending ack for the received {last_seq_acked}")
            except Exception as e:
                print(f"Tried to send ACK for packet {last_seq_acked}, but failed: {e}")