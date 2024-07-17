import posixpath
from typing import List
from elftools.elf.elffile import ELFFile
from elftools.dwarf.descriptions import describe_DWARF_expr
from elftools.dwarf.locationlists import LocationEntry
from elftools.dwarf.lineprogram import LineProgram, LineState


def process_file(filename):
    with open(filename, "rb") as f:
        elffile = ELFFile(f)

        # 获取所有的调试信息节
        dwarfinfo = elffile.get_dwarf_info()

        # 遍历每一个调试信息节
        for cu in dwarfinfo.iter_CUs():
            # 获取每一个调试信息单元的行信息
            line_program = dwarfinfo.line_program_for_CU(cu)
            if line_program is None:
                continue
            file_list = index2file(line_program)
            print(file_list)


def index2file(line_program: LineProgram):
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
