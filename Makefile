build:
	gcc -g -O0 -o 4_pointer 4_pointer.c
	gcc -g -O0 -o 3_die_tree 3_die_tree.c
	gcc -g -O0 -o 0_cu 0_cu_add.c 0_cu_main.c
	# riscv64-unknown-elf-gcc -g -O0 instruction.s -o instruction