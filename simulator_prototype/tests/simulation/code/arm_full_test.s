MOV		r0, #0xFF            ; 0xE3A000FF
MOV		r1, #0x01            ; 0xE3A01001
MOV		r2, r1               ; 0xE1A02001
MOV		r4, #0x100           ; 0xE3A04C01
STR		r0, [r4, #0x104]     ; 0xE5840104
ADD		r3, r0, r1           ; 0xE0803001
ADD		r4, r1, #2           ; 0xE2814002
AND		r4, r2, r1           ; 0xE0024001
AND		r4, r3, #0x100       ; 0xE2034C01
EOR		r5, r2, r3           ; 0xE0225003
EOR		r5, r2, r1           ; 0xE0225001
MOV		r4, #0x100           ; 0xE3A04C01
LDR		r5, [r4, #0x104]     ; 0xE5945104
MOV		r0, #0               ; 0xE3A00000
MOV		r1, #0               ; 0xE3A01000
MOV		r2, #0               ; 0xE3A02000
MOV		r3, #0               ; 0xE3A03000
MOV		r4, #0               ; 0xE3A04000
MOV		r5, #0               ; 0xE3A05000
B		#22                    ; 0xEAFFFFF0
ADD		r1, r1, #25          ; 0xE2811019
SUB		r1, r0, #1           ; 0xE2401001
SUB		r2, r0, r1           ; 0xE0402001
ORR		r3, r2, #0x8         ; 0xE3823008
ORR		r4, r2, r0           ; 0xE1824000
MOV		r5, #0x200           ; 0xE3A05C02
STR		r3, [r5]             ; 0xE5853000
CMP		r0, r0               ; 0xE1500000
BEQ		#31                  ; 0x0AFFFFE9
EOR		r4, r1, r2           ; 0xE0214002
LDR		r6, [r5]             ; 0xE5956000
BL		#41                  ; 0xEBFFFFE9
CMP		r0, #0               ; 0xE3500000
BNE		#38                  ; 0x1AFFFFE6
MOV		r1, #1               ; 0xE3A01001
MOV		r2, #0               ; 0xE3A02000
B		#31                    ; 0xEAFFFFE1
MOV		r1, #0               ; 0xE3A01000
MOV		r2, #0               ; 0xE3A02000
B		#31                    ; 0xEAFFFFDE
ADD		r0, r1, r2           ; 0xE0810002
MUL 		r2, r0, r1         ; 0xE0020190
MLA 		r3, r2, r1, r0     ; 0xE0230192
MOV		pc, lr               ; 0xE1A0F00E
