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
    def __init__(self,seq,ack,flags):
        #The header gets created when you create a Header instance
        self.header = pack(HEADER_FORMAT, seq, ack, flags)
        self.seq = seq
        self.ack = ack
        self.flags = flags
    
    def get_header(self):
        return self.header

    def parse_header(self):
        #takes a header of as an argument,
        #unpacks the value based on the specified header_format
        #and returns a tuple with the values
        return unpack(HEADER_FORMAT, self.header)