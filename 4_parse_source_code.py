from __future__ import print_function
from collections import defaultdict
import os
import sys
import posixpath
from typing import List

import elftools.dwarf
import elftools.dwarf.die
import elftools.dwarf.dwarf_expr
import elftools.dwarf.lineprogram

# If pyelftools is not installed, the example can also run from the root or
# examples/ dir of the source distribution.
sys.path[0:0] = [".", ".."]

import elftools
from elftools.dwarf.die import DIE, AttributeValue
from elftools.dwarf.dwarfinfo import CompileUnit
from elftools.dwarf.lineprogram import LineProgram, LineProgramEntry, LineState
from elftools.elf.elffile import ELFFile


def process_file(filename):
    print("Processing file:", filename)
    with open(filename, "rb") as f:
        elffile = ELFFile(f)

        if not elffile.has_dwarf_info():
            print("  file has no DWARF info")
            return

        dwarfinfo = elffile.get_dwarf_info()

        for cu in dwarfinfo.iter_CUs():
            # die = cu.get_DIE_from_refaddr(76)
            # read_value(die)
            for i, die in enumerate(cu.iter_DIEs()):
                process_die(die, "  ", i)
                pass


def read_memory():
    pass


def read_value(DIE: DIE):
    if "DW_AT_location" in DIE.attributes:
        loc_attr: AttributeValue = DIE.attributes["DW_AT_location"]
        loc_value = loc_attr.value
        print(f"DW_AT_location value: {loc_value}")
        res = read_memory(loc_value)
        print(res)
    else:
        print("Variable 'a' does not have DW_AT_location attribute.")


VISITED: dict = {}


def process_die(die: DIE, indent, index):
    if VISITED.get(die.offset) == True:
        return
    VISITED[die.offset] = True

    print(f"{indent}[{index:2}]DIE tag:", die.tag, f"offset: [{die.offset}]")

    if (len(die.attributes.keys())) != 0:
        print(f"{indent}    DIE attributes:")
        for i, (attr, value) in enumerate(die.attributes.items()):
            print(f"{indent}        attr[{i}] {attr:20}: {value}")
            pass
        if not die.has_children:
            return

    if (len(list(die.iter_children()))) != 0:
        for i, child in enumerate(die.iter_children()):
            process_die(child, indent + "    ", i)


if __name__ == "__main__":
    process_file("./4_pointer")
