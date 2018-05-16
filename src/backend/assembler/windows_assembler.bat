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

if not exist ".\\src\\backend\\assembler\\generated_machine_code" mkdir ".\\src\\backend\\assembler\\generated_machine_code"

:: Generate machine code
arm-none-eabi-as %1 -march=armv4 -mbig-endian -o ./src/backend/assembler/generated_machine_code/object.o
if exist ".\\src\\backend\\assembler\\generated_machine_code\\object.o" (
    arm-none-eabi-objcopy -O binary ./src/backend/assembler/generated_machine_code/object.o ./src/backend/assembler/generated_machine_code/machine_code.bin
    del ".\\src\\backend\\assembler\\generated_machine_code\\object.o"
)
