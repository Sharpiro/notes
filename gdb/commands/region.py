import gdb
import re
from dataclasses import dataclass

@dataclass
class MemoryRegion:
    start: int
    end: int
    size: int
    offset: int
    permissions: str
    objfile: str
    order_number: int

class RegionCommand(gdb.Command):
    """
    Get a memory region from a provided address
    Usage: region address
    """

    def __init__(self):
        super(RegionCommand, self).__init__("region", gdb.COMMAND_USER)

    def invoke(self, arg: str, from_tty):
        try:
            if len(arg) == 0:
                raise Exception("Expected address")

            search_address = int(arg, 16)
            info_proc_map_output = gdb.execute("info proc map", to_string = True)
            split_lines = [
                re.sub("\s+", " ", l.strip()).split(" ")
                for l in info_proc_map_output.split("\n")[4:-1]
            ]
            memory_regions = [
                MemoryRegion(
                    start = int(l[0], 16),
                    end = int(l[1], 16),
                    size = int(l[2], 16),
                    offset = int(l[3], 16),
                    permissions = l[4],
                    objfile = l[5] if len(l) > 5 else "",
                    order_number = i + 1,
                )
                for [i, l] in enumerate(split_lines)
            ]

            found = False;
            for mr in memory_regions:
                if search_address >= mr.start and search_address < mr.end:
                    found = True;
                    print(
                        f"{mr.order_number} {mr.start:#x} {mr.end:#x} {mr.size:#x} {mr.offset:#x} {mr.permissions} {mr.objfile}"
                    )
                    break
            if (not found):
                print("Not found")
        except Exception as e:
            print(e)


RegionCommand()
