import sys
from Crypto.Cipher import AES

## SET 2
## cryptopals.com/sets/2/challenges

# Start 9

# Implementation of PKCS#7 padding
# msg is a bytearray
def pkcs7Padding(blockLength, msg):
    remainingBytes = blockLength % len(msg)
    theBuffer = bytearray()
    theBuffer[:] = msg
    theBuffer += bytearray([chr(remainingBytes)] * remainingBytes)
    return theBuffer




print pkcs7Padding(20, bytearray("YELLOW SUBMARINE")) #"YELLOW SUBMARINE\x04\x04\x04\x04"

# end 9 

# start 10


