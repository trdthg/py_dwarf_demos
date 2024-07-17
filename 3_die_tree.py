from elftools.dwarf.die import DIE
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
            for i, die in enumerate(cu.iter_DIEs()):
                process_die(die, "  ", i)


VISITED: dict = {}


def process_die(die: DIE, indent, index):
    if VISITED.get(die.offset) == True:
        # return
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
        if False:
            for i, child in enumerate(die.iter_children()):
                process_die(child, indent + "    ", i)


if __name__ == "__main__":
    process_file("./3_die_tree")
