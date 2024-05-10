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

# factory method
# create_header_with_certain_setup -> Header

"""
class Header:
    def __init__(self,seq=0,ack=0,flags):

syn_ack_header = Header(flags=SYNACKFLAG)

""" 

class Header:
    def __init__(self,seq=0,ack=0,flags=0):
        #The header gets created when you create a Header instance
        self.header = pack(HEADER_FORMAT, seq, ack, flags)
        self.seq = seq
        self.ack = ack
        self.flags = flags
    
    '''Returns the header.
    '''
    def get_header(self):
        return self.header

    '''Takes a header of as an argument,
    unpacks the value based on the specified header_format
    and returns a tuple with the values'''
    def parse_header(self):
        return unpack(HEADER_FORMAT, self.header)
    
    # def is_syn_ack_set
        #"syn, ack, flgs = parse_header()
        #"return syn == 
    
# todo test that take in header, test flag etc

# 

if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    #main()