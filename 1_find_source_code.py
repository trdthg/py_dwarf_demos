import posixpath
from typing import List
from elftools.elf.elffile import ELFFile
from elftools.dwarf.lineprogram import LineProgram


def process_file(filename):
    with open(filename, "rb") as f:
        elffile = ELFFile(f)

        dwarfinfo = elffile.get_dwarf_info()

        for cu in dwarfinfo.iter_CUs():
            line_program = dwarfinfo.line_program_for_CU(cu)
            if line_program is None:
                continue
            file_list = get_files(line_program)
            print(file_list)


def get_files(line_program: LineProgram):
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


if __name__ == "__main__":
    process_file("instruction")
