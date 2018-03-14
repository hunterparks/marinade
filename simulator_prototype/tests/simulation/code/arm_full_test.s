;|   Code               |         Result                |     Binary
MOV r2, #10             ; A                             ; 0xe3, 0xa0, 0x20, 0x0a
MOV r3, r2              ; A                             ; 0xe1, 0xa0, 0x30, 0x02
MOV r4, r3              ; A                             ; 0xe1, 0xa0, 0x40, 0x03
ADD r1, r2, r3          ; 14                            ; 0xe0, 0x82, 0x10, 0x03
ADD r1, r2, #1          ; B                             ; 0xe2, 0x82, 0x10, 0x01
AND r1, r2, r3          ; A                             ; 0xe0, 0x02, 0x10, 0x03
AND r1, r2, #1          ; 0                             ; 0xe2, 0x02, 0x10, 0x01
CMP r1, r1              ; Z = 1                         ; 0xe1, 0x51, 0x00, 0x01
CMP r1, #1              ; Z = 0                         ; 0xe3, 0x51, 0x00, 0x01
EOR r1, r2, r3          ; 0                             ; 0xe0, 0x22, 0x10, 0x03
EOR r1, r2, #1          ; B                             ; 0xe2, 0x22, 0x10, 0x01
MUL r1, r2, r3          ; 64                            ; 0xe0, 0x01, 0x03, 0x92
MLA r1, r2, r3, r4      ; 74                            ; 0xe0, 0x21, 0x43, 0x92
ORR r1, r2, r3          ; A                             ; 0xe1, 0x82, 0x10, 0x03
ORR r1, r2, #1          ; B                             ; 0xe3, 0x82, 0x10, 0x01
SUB r1, r2, r3          ; 0                             ; 0xe0, 0x42, 0x10, 0x03
SUB r1, r2, #1          ; 9                             ; 0xe2, 0x42, 0x10, 0x01
LDR r1, [r2]            ; 9 -> MEM[A]                   ; 0xe5, 0x92, 0x10, 0x00
LDR r2, [r3, #4]        ; A -> MEM[E]                   ; 0xe5, 0x93, 0x20, 0x04
STR r5, [r2]            ; MEM[A] -> 9                   ; 0xe5, 0x82, 0x50, 0x00
STR r5, [r3, #4]        ; MEM[E] -> A                   ; 0xe5, 0x83, 0x50, 0x04
B #96                   ; Take Branch                   ; 0xea, 0x00, 0x00, 0x01
ADD r0, r0, #0          ; <should not calculate> 0      ; 0xe2, 0x80, 0x00, 0x00
BL #112                 ; Take Branch                   ; 0xeb, 0x00, 0x00, 0x03
ADD r0, r0, #0          ; <should not calculate> 0      ; 0xe2, 0x80, 0x00, 0x00
ADD r0, r0, #0          ; <should not calculate> 0      ; 0xe2, 0x80, 0x00, 0x00
ADD r0, r0, #0          ; <should not calculate> 0      ; 0xe2, 0x80, 0x00, 0x00
MOV r1, #1              ; 1                             ; 0xe3, 0xa0, 0x10, 0x01
MOV r0, #0              ; 0                             ; 0xe3, 0xa0, 0x00, 0x00
ADD r2, r1, r0, LSL #2  ; 4                             ; 0xe0, 0x81, 0x21, 0x00
ADD r2, r2, r0, ROR #3  ; 80000000                      ; 0xe0, 0x82, 0x21, 0xe0
BEQ #144                ; Don't Take Branch             ; 0x0a, 0x00, 0x00, 0x03
ADD r0, r0, #0          ; 0                             ; 0xe2, 0x80, 0x00, 0x00
BNE #144                ; Take Branch                   ; 0x1a, 0x00, 0x00, 0x01
ADD r0, r0, #0          ; <should not calculate> 0      ; 0xe2, 0x80, 0x00, 0x00
B #0                    ; Take Branch                   ; 0xea, 0xff, 0xff, 0xdb
