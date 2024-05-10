from socket import *
from header import *
import utils

'''Function initiating a three-way handshake: It receives the parameters clientSocket, ip and port.
Starts by sending a SYN-packet and checking if it receives a SYN-ACK-packet in return.
If it receives the SYN-ACK-packet, it sends an ACK-packet, and the handshake is successful.
If something fails along the way, the handshake is unsuccessful.
Returns True for success and False if it fails. '''
def successful_handshake(clientSocket, ip, port):
    synheader = Header(flags=SYNFLAG) # (seg=0) header.create_syn_header()
    data = b''
    packet = utils.create_packet(synheader.get_header(),data)
    clientSocket.sendto(packet, (ip, port))
    print("SYN packet is sent")
    
    try:
        clientSocket.settimeout(0.5)
        _, _, data, _, _, flags = utils.receive_packet(clientSocket)
        # flags
        # header, date = receive_packet(clientSocket)
        # if header.flags() == SYNACKFLAG
        #Checking if it receives a SYN-ACK packet.
        if (flags == SYNACKFLAG):
            print("SYN-ACK packet is received")
            
            #If SYN-ACK is received, send an ACK.
            ackheader = Header(flags=ACKFLAG) # header_create_syn_ack_header() , header.create_packet_ack_header(ack)?
            data = b''
            packet = utils.create_packet(ackheader.get_header(),data)
            clientSocket.sendto(packet, (ip, port))
            print("ACK packet is sent")
            
            #The connection is successful from the client side.
            print("Connection established\n")
            return True
        else:
            print("No SYN-ACK packet received.")
            return False
    except Exception as e:
        print(f"Timeout exception: {e}.")
        clientSocket.close()


'''Function used to stop the connection and close the socket.
Takes clientSocket, ip and port as arguments. Initiates by sending a FIN-packet to the server.
If it receives an ACK-packet in return, the client Socket can close. Returns nothing.'''
def connection_teardown(clientSocket, ip, port):
    print("Connection Teardown:\n")
    data = b''
    finheader = Header(flags=FINFLAG)
    packet = utils.create_packet(finheader.get_header(),data)
    clientSocket.sendto(packet,(ip,port))
    print("FIN packet is sent")
    
    #Checking if the socket receives an ACK-packet.
    try:
        clientSocket.settimeout(0.5)
        _, _, _, _, _, flags = utils.receive_packet(clientSocket)
        if flags == ACKFLAG:
            print("ACK packet is received")
            clientSocket.close()
            print("Connection Closes")
    except TimeoutError as e:
        print(f"Didn't receive an ACK for the FIN. Exception: {e}")


'''Function takes file path as argument and creates packets of data size 994 bytes.
Returns a list with all the packets stored.'''
def prepare_packets(file):
    seq = 1
    with open(file, "rb") as opened_file:
        data = opened_file.read(994)
        packets = []
        while data:
            synheader = Header(seq=seq,flags=SYNFLAG)
            packet = utils.create_packet(synheader.get_header(),data)
            packets.append(packet)
            data = opened_file.read(994)
            seq+=1
    return packets


'''Function for creating a string for visualizing the sliding window.'''
def sliding_window_print(lowest_seq, windowsize):
    output = "{" + str(lowest_seq)
    for i in range(windowsize-1):
        output += ", " + str(lowest_seq+1)
        lowest_seq+=1
    output += "}"
    return output


'''Function for initiating client: starting a UDP socket and using a three-way handshake to connect
to the server. Prepares all the packets in a list, and sends packets based on the window size. 
It also resends packets if no ACK is received before the time-out (Go-Back-N). After all packets are send and ACK'ed,
the client initiates a connection teardown, and closes the socket after receiving an ACK. Returns nothing.'''
def clientFunction(ip, port, file, window):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("Connection Establishment Phase:\n")
    
    if successful_handshake(clientSocket, ip, port):
        #Creating a list of all the packets that will be sent
        packets = prepare_packets(file)
        lowest_seq = 1
        highest_seq = window
        
        print("Data Transfer:\n")
        for i in range(lowest_seq-1,highest_seq): #To reflect index of packets
            seq = i+1
            clientSocket.sendto(packets[i],(ip,port))
            print(f"{utils.timestamp()} -- packet with seq = {seq} is sent, sliding window = {sliding_window_print(lowest_seq, window)}")
        while True:
            #TODO: What if the cumulative window size of file is smaller than window size?
            try:
                clientSocket.settimeout(0.5)
                _, _, _, seq, ack, _ = utils.receive_packet(clientSocket)
                if (ack==lowest_seq):
                    print(f"{utils.timestamp()} -- ACK for packet = {ack} is received")
                    lowest_seq+=1
                    
                    if (len(packets)>highest_seq):
                        clientSocket.sendto(packets[highest_seq],(ip,port))
                        highest_seq+=1
                        print(f"{utils.timestamp()} -- packet with seq = {highest_seq} is sent, sliding window = {sliding_window_print(lowest_seq, window)}")
                    
                    elif (len(packets)==ack):
                        print("DATA Finished\n")
                        connection_teardown(clientSocket,ip,port)
                        break
                else:
                    clientSocket.sendto(packets[ack],(ip,port))
                    print(f"{utils.timestamp()} -- packet with seq = {seq} is sent")
                    #TODO: def sendPacket(packet), but might be to many variations?
            except Exception as e:
                print(f"Wasn't able to receive any acks. Exception: {e}")
    else:
        print("The handshake was unsuccessful.")