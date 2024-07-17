.section .text

.globl main

add:
   add a0, a0, a1
   ret

main:
   add t0, zero, zero   # t0 = 0
   addi t0, t0, 1       # t0 = t0 + 1
1:  beq zero, zero, 1b  # 死循环
