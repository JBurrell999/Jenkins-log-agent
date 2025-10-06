ENTRY(start)

SECTIONS {
  . = 0x00100000;        /* load kernel at 1 MiB */

  .text : {
    *(.multiboot)
    *(.text*)
  }

  .rodata : { *(.rodata*) }
  .data   : { *(.data*) }
  .bss    : { *(.bss*)  }
}
