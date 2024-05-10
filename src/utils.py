import ipaddress
import os
from header import *
import sys

'''Function for checking if the IP address is ok, returns boolean'''
def ip_ok(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

'''Function for checking if the port is in range, returns boolean'''
def port_ok(port):
    return port in range(1024,65536)

'''Function for printing the throughput based on how much data
was received and how much time elapsed during the connection.
Takes start_time and end_time as arguments and prints the result.'''
def print_throughput(start_time, end_time):
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
        
        #As stated in the assignment: For the sake of simplicity, 
        # assume 1 KB = 1000 Bytes, and 1 MB = 1000 KB. 
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
        sys.exit(1)
    except OSError:
        print("OS error occurred.")

'''Function for receiving packets via UDP.
It unpacks the packet and 
returns sender address, header, data, seq, ack and flags.'''
def receive_packet(udpsocket):
    packet, address = udpsocket.recvfrom(1000)
    header, data = unpack_packet(packet)
    seq, ack, flags = header.parse_header()
    return address, header, data, seq, ack, flags

'''
''' # geir part of header module?
def create_header_from_packet(packet):
    header = packet[:calcsize(HEADER_FORMAT)]
    seq, ack, flags = unpack(HEADER_FORMAT, header)
    return Header(seq, ack, flags)

'''Accepts a packet and returns a tuple with the header and data'''
def unpack_packet(packet):
    header = create_header_from_packet(packet)
    data = packet[calcsize(HEADER_FORMAT):]
    return header, data

'''Adds the header and the data together and returns it.'''
def create_packet(header, data):
    return header + data