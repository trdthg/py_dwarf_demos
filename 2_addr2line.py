from collections import defaultdict
import posixpath
from typing import List
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

        # CU 对象（编译单元对象）是在 ELF 文件中表示编译单元的一部分，它主要提供了一些基本信息，如编译单元的大小、偏移等。
        # 一个编译单元（CU）可能包含来自多个源文件的代码片段。这在 C/C++ 等语言中很常见，尤其是在使用头文件时。
        for cu in dwarfinfo.iter_CUs():
            line_program: LineProgram = cu.dwarfinfo.line_program_for_CU(cu)
            process_lineprogram(line_program)
            line_entry_mapping(line_program)


def process_lineprogram(line_program: LineProgram):
    # 每个 Entry 对应源代码中的一行，并包含了源文件路径、行号、列号等信息。
    entries: List[LineProgramEntry] = line_program.get_entries()
    for i, entry in enumerate(entries):
        state: LineState = entry.state
        if state == None or state.file == 0:
            continue

        # Line Program 是一个结构，它包含了一系列的 Line Table Entries
        print(
            f"addr: {hex(state.address)}, file_index: {state.file} loc: {state.line}:{state.column}"
        )


def get_index2file(line_program: LineProgram):
    lp_header: dict = line_program.header
    file_entries: List[str] = lp_header["file_entry"]
    directory = lp_header["include_directory"]

    res = {}
    for i, file_entry in enumerate(file_entries):
        dir_index = file_entry["dir_index"]
        if dir_index != 0:
            res[i] = posixpath.join(directory[dir_index - 1], file_entry.name).decode()
        else:
            res[i] = file_entry.name.decode()

    return res


def line_entry_mapping(line_program: LineProgram):
    filename_map = defaultdict(int)

    # The line program, when decoded, returns a list of line program
    # entries. Each entry contains a state, which we'll use to build
    # a reverse mapping of filename -> #entries.
    entries = line_program.get_entries()
    for entry in entries:
        state: LineState = entry.state
        # We skip LPEs that don't have an associated file.
        # This can happen if instructions in the compiled binary
        # don't correspond directly to any original source file.
        if not state or state.file == 0:
            continue
        filename = entry_filename(line_program, state.file)
        filename_map[filename] += 1

    for filename, lpe_count in filename_map.items():
        print("    filename=%s -> %d entries" % (filename, lpe_count))


def entry_filename(line_program, file_index):
    lp_header: dict = line_program.header
    file_entries = lp_header["file_entry"]

    # File and directory indices are 1-indexed.
    file_entry = file_entries[file_index - 1]
    dir_index = file_entry["dir_index"]

    # A dir_index of 0 indicates that no absolute directory was recorded during
    # compilation; return just the basename.
    if dir_index == 0:
        return file_entry.name.decode()

    directory = lp_header["include_directory"][dir_index - 1]
    return posixpath.join(directory, file_entry.name).decode()


if __name__ == "__main__":
    process_file("instruction")
