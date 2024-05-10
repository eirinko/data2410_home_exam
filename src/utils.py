import ipaddress
import os
from header import *

def ip_ok(ip):
    '''Function for checking if the IP address is ok'''
    try:
        val = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def port_ok(port):
    '''Function for checking if the port is in range'''
    return port in range(1024,65536)

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
        
def receive_packet(udpsocket):
    packet, address = udpsocket.recvfrom(1000)
    header, data = unpack_packet(packet)
    seq, ack, flags = header.parse_header()
    return address, header, data, seq, ack, flags

def create_header_from_packet(packet):
    header = packet[:calcsize(HEADER_FORMAT)]
    seq, ack, flags = unpack(HEADER_FORMAT, header)
    return Header(seq, ack, flags)

def unpack_packet(packet):
    #Accepts a packet and
    #returns a tuple with the header and data
    header = create_header_from_packet(packet)
    data = packet[calcsize(HEADER_FORMAT):]
    return header, data

def create_packet(header, data):
    #Adds the header and the data together and returns it.
    return header + data
