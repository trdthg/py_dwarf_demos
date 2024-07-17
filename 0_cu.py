from elftools.elf.elffile import ELFFile


def process_file(filename):
    with open(filename, "rb") as f:
        elffile = ELFFile(f)

        dwarfinfo = elffile.get_dwarf_info()

        for cu in dwarfinfo.iter_CUs():
            print(cu.header)


if __name__ == "__main__":
    process_file("./0_cu")
