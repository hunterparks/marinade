import struct

with open("temp_files/machine_code.bin", mode='rb') as binary_file:
    machine_code = binary_file.read()
    print(machine_code)
    program = struct.unpack('B' * len(machine_code), machine_code)
    for byte in program:
        print(hex(byte))
