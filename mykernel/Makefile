CC   := /opt/homebrew/opt/llvm/bin/clang
LD   := /opt/homebrew/bin/ld.lld
NASM := /opt/homebrew/bin/nasm

ASFLAGS = -f elf32
CFLAGS  = --target=i386-unknown-elf -m32 -ffreestanding -fno-pie -fno-stack-protector -O2 -Wall -Wextra
LDFLAGS = -m elf_i386 -T link.ld

all: kernel.bin

kernel_asm.o: kernel.asm
	$(NASM) $(ASFLAGS) $< -o $@

kernel.o: kernel.c
	$(CC) $(CFLAGS) -c $< -o $@

kernel.bin: kernel_asm.o kernel.o link.ld
	$(LD) $(LDFLAGS) -o $@ kernel_asm.o kernel.o

run: kernel.bin
	qemu-system-i386 -kernel kernel.bin

clean:
	rm -f *.o kernel.bin
