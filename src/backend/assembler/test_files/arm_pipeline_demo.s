@***************************************************************
@* sumn(int n) 
@* - implemented as long string of instructions with data hazards
@* - to test CE1921 basic pipeline with data hazard management 
@* - no branch hazards 
@***************************************************************
main:		MOV	R10,#10		@ preload some
			MOV	R9,#9		@ constants
		 	MOV	R8,#8	 	@ to fill pipe
			MOV	R7,#7		@ and avoid data
			MOV R6,#6	    @ hazards
			MOV	R5,#5	  	@ 	
			MOV	R4,#4		@
			MOV	R3,#3		@
			MOV	R2,#2		@
			MOV	R1,#1		@
			ADD	R12,R10,R9	@ Start summing
			ADD	R12,R12,R8	@ 
			ADD	R12,R12,R7	@ 
		    ADD	R12,R12,R6	@ 	
		    ADD	R12,R12,R5	@ 	
		    ADD	R12,R4,R12	@ 	
		    ADD	R12,R3,R12	@ 	
		    ADD	R12,R2,R12	@ 	
			ADD	R12,R1,R12	@ R12=sumn(10)

@ algorithm to determine if the number is >= 32
@ 32 is a binary value: 0000 0000 0000 0000 0000 0000 0010 0000
@ sum will be some num: yyyy yyyy yyyy yyyy yyyy yyyy yyyy yyyy
@
@ if we zero out the bits to the right of the power-32 bit
@ sum will then be:     yyyy yyyy yyyy yyyy yyyy yyyy yyy0 0000
@
@ if any of the y values are 1 then the value is >=32.
@ we can use AND to zero out those bits
@                       yyyy yyyy yyyy yyyy yyyy yyyy yyyy yyyy
@                 AND   1111 1111 1111 1111 1111 1111 1110 0000
@ If none of the y's are 1 then the AND result will be 0.
@ If 0 then the number was not >=32 since no y was a 1.

if:			MOV R0,#0		
			MOV	R1,#1		
			MOV	R2,#4
			SUB	R0,R0,#32	@ 0 â€“ 32 = -32 = FFFFFFE0
			AND	R12,R12,R0	@ >32 leaves 1s
			STR R12,[R2]	@ memory[4] = R12
 			LDR R6,[R2]		@

@ ensure that end of IROM VHDL is LDR "when others" to force
@ an artificial loop as PC just updates constantly to PC+4 and 
@ IROM produces LDR as "when others" output
