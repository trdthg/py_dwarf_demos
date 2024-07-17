from __future__ import print_function
from collections import defaultdict
import os
import sys
import posixpath
from typing import List

import elftools.dwarf
import elftools.dwarf.die
import elftools.dwarf.lineprogram

# If pyelftools is not installed, the example can also run from the root or
# examples/ dir of the source distribution.
sys.path[0:0] = [".", ".."]

import elftools
from elftools.dwarf.die import DIE
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

        # get all entries in the .debug_info section
        # for loop over all entries in the .debug_info section, print tag and attributes

        # for loop over all entries in the .debug_info section, print tag and attributes
        for cu in dwarfinfo.iter_CUs():
            process_cu(cu)
            for i, die in enumerate(cu.iter_DIEs()):
                process_die(die, "  ", i)


def process_cu(cu: CompileUnit):
    line_program: LineProgram = cu.dwarfinfo.line_program_for_CU(cu)
    entries: List[LineProgramEntry] = line_program.get_entries()
    for i, entry in enumerate(entries):
        state: LineState = entry.state

        if state == None:
            continue

        # print(f"addr: {hex(state.address)}, loc: {state.line}:{state.column}")


VISITED: dict = {}


def process_die(die: DIE, indent, index):
    if VISITED.get(die.offset) == True:
        return
        pass
    VISITED[die.offset] = True

    print(f"{indent}[{index:2}]DIE tag:", die.tag, f"offset: [{die.offset}]")

    if (len(die.attributes.keys())) != 0:
        if False:
            print(f"{indent}    DIE attributes:")
            for i, (attr, value) in enumerate(die.attributes.items()):
                print(f"{indent}        attr[{i}] {attr:20}: {value}")
                pass
            if not die.has_children:
                return

    if (len(list(die.iter_children()))) != 0:
        if True:
            for i, child in enumerate(die.iter_children()):
                process_die(child, indent + "    ", i)


if __name__ == "__main__":
    process_file("./3_die_tree")
