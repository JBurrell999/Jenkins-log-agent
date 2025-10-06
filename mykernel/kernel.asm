; Minimal multiboot header + entry that calls kernelMain (C)

section .multiboot
align 4
    dd 0x1BADB002          ; magic
    dd 0x0                  ; flags (no special requests)
    dd -(0x1BADB002 + 0x0)  ; checksum so sum == 0

section .text
global start
extern kernelMain

start:
    cli
    call kernelMain
.hang:
    hlt
    jmp .hang
