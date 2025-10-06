// Write a message to VGA text buffer at 0xB8000 (80x25 text mode)
void kernelMain(void) {
    volatile char* vga = (volatile char*)0xB8000;
    const char* msg = "Hello from macOS-built i386 ELF kernel!";
    for (int i = 0; msg[i]; ++i) {
        vga[i*2] = msg[i];     // character
        vga[i*2+1] = 0x0F;     // attribute: white on black
    }
    for(;;) { __asm__ __volatile__("hlt"); }
}
