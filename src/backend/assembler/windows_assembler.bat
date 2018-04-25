@echo off

:: Get number of arguments
set argC=0
for %%x in (%*) do (
    set /A argC+=1
)

:: Check to make sure correct number of args were supplied
if not %argC% == 1 (
    echo "Incorrect amount of argurments supplied."
    echo "Usage: ./windows_assembler.bat <assembly_file>"
    EXIT /B 1
)

:: Generate machine code
arm-none-eabi-as %1 -march=armv4 -mbig-endian -o generated_machine_code/object.o
if exist "generated_machine_code\\object.o" (
    arm-none-eabi-objcopy -O binary generated_machine_code/object.o generated_machine_code/machine_code.bin
    del "generated_machine_code\\object.o"
)
