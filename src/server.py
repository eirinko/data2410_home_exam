from socket import *
from header import *
import datetime
import time
from utils import *

g_start_time = None
end_time = None

#Three-way handshake
def successful_handshake(serverSocket):
    clientAddress, header, data, seq, ack, flags = receive_packet(serverSocket)
    
    #Only proceed with handshake if the SYN-flag is activated.
    if (flags == SYNFLAG):
        global g_start_time
        g_start_time = time.time()
        
        print("SYN packet is received")
        sequence_number = 0
        acknowledgment_number = 0
        headerObject = Header(sequence_number,acknowledgment_number,SYNACKFLAG)
        data = b''
        packet = create_packet(headerObject.get_header(),data)
        serverSocket.sendto(packet,clientAddress)
        print("SYN-ACK packet is sent")
        clientAddress, header, data, seq, ack, flags = receive_packet(serverSocket)
        
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

def connection_teardown(serverSocket, clientAddress):
    #Create ACK packet.
    header = Header(0,0,ACKFLAG)
    data = b''
    packet = create_packet(header.get_header(),data)
    
    #Sending ACK packet before closing connection
    serverSocket.sendto(packet,clientAddress)
    print("ACK packet is sent\n")

def serverFunction(ip, port, discard):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((ip, port))
    
    #Creating a file where data from the received packets can be appended.
    file = open("result.jpg","wb")
    
    if successful_handshake(serverSocket):
        #Starting the timer when the server has connected to the client.
        
        
        last_seq_acked = 0
        while True:
            try:
                serverSocket.settimeout(0.5)
                clientAddress, header, data, seq, ack, flags = receive_packet(serverSocket)
                
                if flags == FINFLAG:
                    print("FIN packet is received")
                    connection_teardown(serverSocket, clientAddress)
                    
                    #Stopping the timer.
                    end_time = time.time()
                    print_throughput(g_start_time, end_time)
                    
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
                header = Header(last_seq_acked,last_seq_acked,ACKFLAG)
                data = b''
                packet = create_packet(header.get_header(),data)
                serverSocket.sendto(packet,clientAddress)
                print(f"{datetime.datetime.now().time()} -- sending ack for the received {last_seq_acked}")
            except Exception as e:
                print(f"Tried to send ACK for packet {last_seq_acked}, but failed: {e}")