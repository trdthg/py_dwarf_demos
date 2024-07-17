import posixpath
from typing import List
from elftools.elf.elffile import ELFFile
from elftools.dwarf.descriptions import describe_DWARF_expr
from elftools.dwarf.locationlists import LocationEntry
from elftools.dwarf.lineprogram import LineProgram, LineState


def process_file(filename):
    with open(filename, "rb") as f:
        elffile = ELFFile(f)

        dwarfinfo = elffile.get_dwarf_info()

        for cu in dwarfinfo.iter_CUs():
            print(cu.header)


if __name__ == "__main__":
    process_file("/home/trdthg/plct/qtrvsim-template/tmp/instruction")
