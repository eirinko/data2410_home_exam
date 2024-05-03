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
    
    def get_seq(self):
        return self.seq
    
    def set_seq(self, new_seq):
        self.seq = new_seq
    
    def get_ack(self):
        return self.ack
    
    def set_ack(self, new_ack):
        self.ack = new_ack
    
    def get_flags(self):
        return self.flags
    
    def set_flags(self, new_flags):
        self.flags = new_flags
        
    def get_header(self):
        return self.header
    
    def set_flags(self, new_header):
        self.header = new_header
    
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
        syn = flags & (1 << 3)
        ack = flags & (1 << 2)
        fin = flags & (1 << 1)
        return syn, ack, fin

    @staticmethod
    def create_packet(header, data):
        #Adds the header and the data together and returns it.
        #packet = 
        return header + data
    
    @staticmethod
    def unpack_packet(packet):
        #Accepts a packet and
        #returns a tuple with the header and data
        header = packet[:calcsize(header_format)]
        data = packet[calcsize(header_format):]
        return header, data

header_format = '!HHH'
sequence_number = 1
acknowledgment_number = 0
flags = 8

headerObject = Header(sequence_number,acknowledgment_number,flags,header_format)

data = b''

packet = headerObject.create_packet(headerObject.get_header(),data)

#Unpacking the packet
header, message = Header.unpack_packet(packet)

#Unpacking the header
seq, ack, flags = Header.parse_header(header_format, header)
print(f'Seq no: {seq}')
print(f'Ack no: {ack}')

#Unpacking the flags
synflag, ackflag, finflag = Header.parse_flags(flags)
print(f'Syn flag: {synflag}')
print(f'Ack flag: {ackflag}')
print(f'Fin flag: {finflag}')
print(message) #Should be empty.