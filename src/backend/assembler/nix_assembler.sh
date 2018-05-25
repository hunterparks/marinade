#!/bin/bash

# Check to make sure correct number of args were supplied
if [ $# -ne 1 ]; then
    echo "Incorrect amount of arguments supplied."
    echo "Usage: ./linux_assembler.sh <assembly_file>"
    exit $ERRCODE
fi

mkdir -p ./src/backend/assembler/generated_machine_code

# Generate machine code
arm-none-eabi-as "$1" -march=armv4 -mbig-endian -o ./src/backend/assembler/generated_machine_code/object.o
if [ -f ./src/backend/assembler/generated_machine_code/object.o ]; then
    arm-none-eabi-objcopy -O binary ./src/backend/assembler/generated_machine_code/object.o ./src/backend/assembler/generated_machine_code/machine_code.bin
    rm ./src/backend/assembler/generated_machine_code/object.o
fi
