from socket import *
from header import *
import utils

'''Function initiating a three-way handshake: It receives the parameters clientSocket, ip and port.
Starts by sending a SYN-packet and checking if it receives a SYN-ACK-packet in return.
If it receives the SYN-ACK-packet, it sends an ACK-packet, and the handshake is successful.
If something fails along the way, the handshake is unsuccessful.
Returns True for success and False if it fails. '''
def successful_handshake(clientSocket, ip, port):
    synheader = Header(flags=SYNFLAG)
    data = b''
    packet = utils.create_packet(synheader.get_header(),data)
    clientSocket.sendto(packet, (ip, port))
    print("SYN packet is sent")
    
    try:
        clientSocket.settimeout(0.5)
        _, _, data, _, _, flags = utils.receive_packet(clientSocket)
        
        #Checking if it receives a SYN-ACK packet.
        if (flags == SYNACKFLAG):
            print("SYN-ACK packet is received")
            
            #If SYN-ACK is received, send an ACK.
            ackheader = Header(flags=ACKFLAG)
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
    except TimeoutError as e:
        print(f"Timeout exception: {e}.")
        clientSocket.close()


'''Function used to stop the connection and close the socket.
Takes clientSocket, ip and port as arguments. Initiates by sending a FIN-packet to the server.
If it receives an ACK-packet in return, the client Socket can close. Returns nothing.'''
def connection_teardown(clientSocket, ip, port):
    print("Connection Teardown:\n")
    data = b''
    finheader = Header(flags = FINFLAG)
    packet = utils.create_packet(finheader.get_header(),data)
    clientSocket.sendto(packet,(ip,port))
    print("FIN packet is sent")
    
    #Checking if the socket receives an ACK-packet
    # and that it doesn't refer to a seq-no.
    try:
        clientSocket.settimeout(0.5)
        _, _, _, seq, _, flags = utils.receive_packet(clientSocket)
        if flags == FINACKFLAG and seq == 0:
            print("FIN ACK packet is received")
            clientSocket.close()
            print("Connection Closes")
    except TimeoutError as e:
        print(f"Didn't receive a FIN ACK for the FIN. Exception: {e}")


'''Function takes file path as argument and creates packets of data size 994 bytes.
Returns a list with all the packets stored.'''
def prepare_packets(file):
    seq = 1
    with open(file, "rb") as opened_file:
        data = opened_file.read(994)
        packets = []
        while data:
            synheader = Header(seq = seq,flags = SYNFLAG)
            packet = utils.create_packet(synheader.get_header(),data)
            packets.append(packet)
            data = opened_file.read(994)
            seq += 1
    return packets


'''Function for creating a string for visualizing the sliding window.'''
def sliding_window(window_array):
    output = "{"
    for number in window_array:
        output += str(number)
        if window_array.index(number) < len(window_array) - 1:
            output += ", "
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
        
        #In case the file is smaller than the window size.
        if len(packets) < window:
            window = len(packets)
        
        #For storing the sequence numbers in the window.
        window_array = []
        
        #Sending the packets of the first window. 
        print("Data Transfer:\n")
        for i in range(0, window):
            seq = i + 1
            window_array.append(seq)
            clientSocket.sendto(packets[i],(ip,port))
            print(f"{utils.timestamp()} -- packet with seq = {seq} is sent, sliding window = {sliding_window(window_array)}")
        
        while True:
            try:
                clientSocket.settimeout(0.5)
                _, _, _, seq, ack, _ = utils.receive_packet(clientSocket)
                if (ack == window_array[0]):
                    print(f"{utils.timestamp()} -- ACK for packet = {ack} is received")
                    window_array.pop(0) #Remove the first, no need to send this again.
                    
                    if (len(packets) == ack):
                        print("DATA Finished\n")
                        connection_teardown(clientSocket,ip,port)
                        break
                    
                    window_array.append(window_array[-1] + 1)
                    if (window_array[-1] <= len(packets)):
                        clientSocket.sendto(packets[window_array[-1]-1],(ip,port))
                        print(f"{utils.timestamp()} -- packet with seq = {window_array[-1]} is sent, sliding window = {sliding_window(window_array)}")
                
                else:
                    print(f"Received the wrong ACK: {ack}. Retransmitting the whole window: {sliding_window(window_array)}.")
                    for seq in window_array:
                        if (seq <= len(packets)):
                            clientSocket.sendto(packets[seq-1],(ip,port))
                            print(f"{utils.timestamp()} -- packet with seq = {seq} is sent, sliding window = {sliding_window(window_array)}")

            except TimeoutError as e:
                print(f"Wasn't able to receive any acks. Exception: {e}")
    else:
        print("The handshake was unsuccessful.")