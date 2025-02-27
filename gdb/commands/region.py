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


def print_regions(memory_regions: list[MemoryRegion]):
    print("No.\tStart Addr\tEnd Addr\tSize\t\tOffset\tPerms\tobjfile")
    for mr in memory_regions:
        print(
            f"{mr.order_number}\t{mr.start:#x}\t{mr.end:#x}\t{mr.size:#08x}\t{mr.offset:#x}\t{mr.permissions}\t{mr.objfile}"
        )


class RegionCommand(gdb.Command):
    """
    Get a memory region from a provided address
    Usage: region address
    """

    def __init__(self):
        super(RegionCommand, self).__init__("region", gdb.COMMAND_USER)

    def invoke(self, argument: str, from_tty: bool):
        try:
            info_proc_map_output = gdb.execute("info proc map", to_string=True)
            split_lines = [
                re.sub(r"\s+", " ", line.strip()).split(" ")
                for line in info_proc_map_output.split("\n")[4:-1]
            ]
            memory_regions = [
                MemoryRegion(
                    start=int(line[0], 16),
                    end=int(line[1], 16),
                    size=int(line[2], 16),
                    offset=int(line[3], 16),
                    permissions=line[4],
                    objfile=line[5] if len(line) > 5 else "",
                    order_number=i + 1,
                )
                for [i, line] in enumerate(split_lines)
            ]

            if len(argument) == 0:
                print_regions(memory_regions)
                return

            if not argument.startswith("0x"):
                raise Exception("Expected hex address")

            search_address = int(argument, 16)
            found_region: MemoryRegion | None = None
            for mr in memory_regions:
                if search_address >= mr.start and search_address < mr.end:
                    found_region = mr
                    break

            if found_region:
                print_regions([found_region])
            else:
                print("Not found")
        except Exception as e:
            print(e)


RegionCommand()
