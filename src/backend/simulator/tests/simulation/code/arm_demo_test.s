
.global _start
.global _exit

.start:
mov	r8, #10             @ 0xE3A0800A
add	r9, r8, #1          @ 0xE2889001
mul	r9, r8, r9          @ 0xE0090998
mov	r10, #0             @ 0xE3A0A000
sub	r10, r10, #32       @ 0xE24AA020
ands	r10, r9, r10      @ 0xE019A00A
beq	0x00000028          @ 0x0A000002
mov	r11, #1             @ 0xE3A0B001
mov	r12, #4             @ 0xE3A0C004
str	r11, [r12]          @ 0xE58CB000
ldr	r6, [r12]           @ 0xE59C6000
b	0x00000028            @ 0xEAFFFFFD

.end
