import json, struct
import zlib
""" 
#https://docs.python.org/3/library/zlib.html
def checksum(data):
    return zlib.crc32(data)

data = {
    "ACK_NUM": 25,
    "ACK_FLAG": 1
}

ACK = 0x01
DATA = 0x02
CMD = 0x03
EVENT = 0x04

method = ACK
sequence_number = 25
data = json.dumps(data).encode()
checksum_1 = checksum(data)
#https://docs.python.org/3/library/struct.html
header = struct.pack("!bhi", method, sequence_number, checksum_1)
package = header + data
print(checksum)

print(package)
sz = len(header)


udp_header = package[:sz]
udp_header = struct.unpack("!bhi", udp_header)
print(udp_header[2])
print(udp_header[1])
print(udp_header[0])

checksum_2 = checksum(package[sz:])
data = json.loads(package[sz:].decode())

print(checksum_2 == udp_header[2])
print(data) """

#todo: retransmission, keeping track of order, 
from .NetworkInterface import NetworkInterface
from crcmod import crcmod

class IntegrityMiddleware:

    counter: list[any]
    protocol: NetworkInterface

    def __init__(self, protocol: NetworkInterface) -> None:
        self.protocol = protocol
        

    def write(self) -> None:
        self.protocol.write()

    def read(self) -> None:
        self.protocol.read()

    def _calc_checksum(data: bytes) -> int:
        #https://crcmod.sourceforge.net/crcmod.html
        #crc16
        #TODO: check credentials
        return crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)




    #look at middleware pattern that goes between data storing/event handling and receicinv/writing data to network