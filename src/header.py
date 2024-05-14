from struct import *
#Using a modified version of the code by Safiqul on his Github:
# https://github.com/safiqul/2410/blob/main/header/header.py
#Restructured so the header functions are a part of a class Header.

HEADER_FORMAT = '!HHH'
FINFLAG = 2
ACKFLAG = 4
FINACKFLAG = 6
SYNFLAG = 8
SYNACKFLAG = 12

class Header:
    def __init__(self,seq=0,ack=0,flags=0):
        #The header gets created when you create a Header instance
        self.header = pack(HEADER_FORMAT, seq, ack, flags)
        self.seq = seq
        self.ack = ack
        self.flags = flags
    
    '''Returns the header.'''
    def get_header(self):
        return self.header

    '''Takes a header of as an argument,
    unpacks the value based on the specified header_format
    and returns a tuple with the values seq, ack, flags'''
    def parse_header(self):
        return unpack(HEADER_FORMAT, self.header)


    '''Takes a packet as an argument and returns a Header.'''
    def create_header_from_packet(packet):
        header = packet[:calcsize(HEADER_FORMAT)]
        seq, ack, flags = unpack(HEADER_FORMAT, header)
        return Header(seq, ack, flags)