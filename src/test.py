#Testing splitting a file into data of size 994 byte 
# and creating data packets storing them in an array
#before re-assembling the file again.

import argparse
from header import *
import os

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
    print(seq)
    seq+=1
opened_file.close()

for packet in packets:
    print(packets.index(packet))
    header, data = Header.unpack_packet(packet,header_format)
    seq, ack, flags = Header.parse_header(header_format, header)
    result_file.write(data)
    
print(f"Number of packets: {len(packets)}")



# Replace 'your_file_path' with the actual file path
file_path = 'result.jpg'

try:
    file_size = os.path.getsize(file_path)
    print(f"File Size in Bytes is {file_size}")
except FileNotFoundError:
    print("File not found.")
except OSError:
    print("OS error occurred.")