#!/bin/bash
if [ $# -eq 0 ]
    then
        echo "Configuration error: No file supplied to assembler."
        exit $ERRCODE
fi
arm-none-eabi-as "$1" -march=armv4 -mbig-endian -o temp_files/object.o 
arm-none-eabi-objdump -D temp_files/object.o > temp_files/dump.txt 
