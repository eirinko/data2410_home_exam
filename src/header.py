from struct import *
#Using a modified version of the code by Safiqul on his Github:
# https://github.com/safiqul/2410/blob/main/header/header.py
#Restructured so the header functions are a part of a class Header.

class Header:
    def __init__(self,seq,ack,flags, header_format):
        #The header gets created when you create a Header instance
        self.header = pack(header_format, seq, ack, flags)
        self.seq = seq
        self.ack = ack
        self.flags = flags
        self.header_format = header_format
        #self.packetsize = 1000
        #Maybe have packetsize outside of the header instead...
    
    def get_header(self):
        return self.header
    
    def create_header(self):
        self.header = pack(self.header_format, self.seq, self.ack, self.flags)
    
    def get_sequence_number(self):
        return self.seq
    
    def set_sequence_number(self, new_sequence_number):
        self.seq = new_sequence_number
        self.create_header()
        
    def get_acknowledgement(self):
        return self.ack
    
    def set_acknowledgement(self, new_acknowledgement):
        self.ack = new_acknowledgement
        self.create_header()
    
    def get_flags(self):
        return self.flags
    
    def set_flags(self, new_flags):
        self.flags = new_flags
        self.create_header()
        
    def get_header_format(self):
        return self.header_format
    
    #No setter for header format, don't want to change this.
    
    @staticmethod
    def parse_header(given_header_format, given_header):
        #takes a header of as an argument,
        #unpacks the value based on the specified header_format
        #and returns a tuple with the values
        return unpack(given_header_format, given_header)
    
    @staticmethod
    def parse_flags(flags):
        #we only parse the first 3 fields because we're not 
        #using rst in our implementation
        syn = bool(flags & (1 << 3))
        ack = bool(flags & (1 << 2))
        fin = bool(flags & (1 << 1))
        return syn, ack, fin

    @staticmethod
    def create_packet(header, data):
        #Adds the header and the data together and returns it.
        #packet = 
        return header + data
    
    @staticmethod
    def unpack_packet(packet, header_format):
        #Accepts a packet and
        #returns a tuple with the header and data
        header = packet[:calcsize(header_format)]
        data = packet[calcsize(header_format):]
        return header, data
    
    #activate syn flag
    #deactivate syn flag
    
    @staticmethod
    def syn_flag(flags):
        return bool(flags & (1 << 3))
    
    @staticmethod
    def ack_flag(flags):
        return bool(flags & (1 << 2))
    
    @staticmethod
    def fin_flag(flags):
        return bool(flags & (1 << 1))
    
    #not done.
    def data_length():
        return 994
