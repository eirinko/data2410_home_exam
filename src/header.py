from struct import *
#Using a modified version of the code by Safiqul on his Github:
# https://github.com/safiqul/2410/blob/main/header/header.py
#Restructured so the header functions are a part of a class Header.

header_format = '!HHH'

class Header:
    def __init__(self,seq,ack,flags, header_format):
        #The header gets created when you create a Header instance
        self.header = pack(header_format, seq, ack, flags)
        self.seq = seq
        self.ack = ack
        self.flags = flags
        self.header_format = header_format
    
    def get_header(self):
        return self.header

    def parse_header(self):
        #takes a header of as an argument,
        #unpacks the value based on the specified header_format
        #and returns a tuple with the values
        return unpack(self.header_format, self.header)

    @staticmethod
    def create_packet(header, data):
        #Adds the header and the data together and returns it.
        return header + data
    
    @staticmethod
    def create_header_from_packet(packet):
        header = packet[:calcsize(header_format)]
        seq, ack, flags = unpack(header_format, header)
        return Header(seq, ack, flags, header_format)
    
    @staticmethod
    def unpack_packet(packet, header_format):
        #Accepts a packet and
        #returns a tuple with the header and data
        header = Header.create_header_from_packet(packet)
        data = packet[calcsize(header_format):]
        return header, data
    
    @staticmethod
    def syn_flag(flags):
        return bool(flags & (1 << 3))
    
    @staticmethod
    def ack_flag(flags):
        return bool(flags & (1 << 2))
    
    @staticmethod
    def fin_flag(flags):
        return bool(flags & (1 << 1))