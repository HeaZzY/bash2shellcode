import random
import struct
import sys

def find_valid_xor_byte(bytes, bad_chars):
    for i in random.sample(range(1, 256), 255):
        matched_a_byte = False

        # Check if the potential XOR byte matches any of the bad chars.
        for byte in bad_chars:
            if i == byte:
                matched_a_byte = True
                break

        for byte in bytes:
            # Check that the current byte is not the same as the
            # XOR byte, otherwise null bytes will be produced.
            if i == byte:
                matched_a_byte = True
                break

            # Check if XORing using the current byte would result in any
            # bad chars ending up in the final shellcode.
            for bad_byte in bad_chars:
                if struct.pack('B', byte ^ i) == bad_byte:
                    matched_a_byte = True
                    break

            # If a bad char would be encountered when XORing with the
            # current XOR byte, skip continuing checking the bytes and
            # try the next candidate.
            if matched_a_byte:
                break

        if not matched_a_byte:
            return i



def encodeShellcode(shellcode,bad_chars=[0x00]):
    encoded = []
    chunk_no = 0



    while len(shellcode) > 0:
        chunk_no += 1
        xor_byte = 0
        chunk = shellcode[0:2]

        xor_byte = find_valid_xor_byte(chunk, bad_chars)

        if xor_byte == 0:
            exit(2)

        encoded.append(struct.pack('B', xor_byte))
        for i in range(0, 2):
            if i < len(chunk):
                encoded.append(struct.pack('B', (chunk[i] ^ xor_byte)))
            else:
                encoded.append(struct.pack('B', xor_byte))

        shellcode = shellcode[2::]



    if xor_byte == 0:
        exit(3)

    encoded.append(struct.pack('B', xor_byte))

    shellcoded = ""
    for char in encoded:
        shellcoded += "\\x" + str(hex(ord(char))).split('x')[1]     
    return shellcoded
