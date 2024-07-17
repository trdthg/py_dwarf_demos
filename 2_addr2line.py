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

        for cu in dwarfinfo.iter_CUs():
            line_program: LineProgram = cu.dwarfinfo.line_program_for_CU(cu)
            process_lineprogram(line_program)


def process_lineprogram(line_program: LineProgram):
    entries: List[LineProgramEntry] = line_program.get_entries()
    for i, entry in enumerate(entries):
        state: LineState = entry.state
        if state == None or state.file == 0:
            continue

        print(
            f"addr: {hex(state.address)}, file_index: {entry_filename(line_program, state.file)} loc: {state.line}:{state.column}"
        )


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
