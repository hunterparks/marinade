'''
This module is used to parse object dump files generated by a bash or batch
script and feed the parsed machine code to the simulator.
'''

import sys
sys.path.insert(0, '../')
from main import Interface


def main():
    obj_dump = open("temp_files/dump.txt", 'r')
    program_bytes = []
    start_flag = False
    for line in obj_dump:
        if line.find(" 0:") != -1:
            start_flag = True
        if start_flag and (line != '\n' or line != '\r\n'): 
            program_bytes.append(int(line[6:8], 16))
            program_bytes.append(int(line[8:10], 16))
            program_bytes.append(int(line[10:12], 16))
            program_bytes.append(int(line[12:14], 16))
        elif start_flag and (line == '\n' or line == '\r\n'):
            break
    obj_dump.close()
    simulator = Interface()
    simulator.program(program_bytes)


if __name__ == '__main__':
    main()