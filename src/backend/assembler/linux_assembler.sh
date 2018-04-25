#!/bin/bash

# Check to make sure correct number of args were supplied
if [ $# -ne 1 ]
    then
        echo "Incorrect amount of argurments supplied."
        echo "Usage: ./linux_assembler.sh <assembly_file>"
        exit $ERRCODE
fi

# Generate machine code
arm-none-eabi-as "$1" -march=armv4 -mbig-endian -o generated_machine_code/object.o
if [ -f generated_machine_code/object.o ]; then
    arm-none-eabi-objcopy -O binary generated_machine_code/object.o generated_machine_code/machine_code.bin
    rm generated_machine_code/object.o
fi