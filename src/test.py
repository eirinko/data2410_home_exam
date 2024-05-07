#Testing splitting a file into data of size 994 byte 
# and creating data packets storing them in an array
#before re-assembling the file again.

import argparse
from header import *

header_format = '!HHH'
finflag = 2
ackflag = 4
finackflag = 6
synflag = 8
synackflag = 12

parser = argparse.ArgumentParser(description='simple args')
parser.add_argument('-f', '--file', type=str)
args = parser.parse_args()

opened_file = open(args.file,"rb")
result_file = open("result.jpg","wb")
seq = 1
ack = 0
packets = []
data = opened_file.read(994)

while data:
    #Now it just sends all the information without waiting for acks. 
    synheader = Header(seq,ack,synflag,header_format)
    packet = synheader.create_packet(synheader.get_header(),data)
    packets.append(packet)
    data = opened_file.read(994)
    seq+=1
    
opened_file.close()

for packet in packets:
    header, data = Header.unpack_packet(packet,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    result_file.write(data)
    
print(f"Number of packets: {len(packets)}")