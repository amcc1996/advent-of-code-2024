import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def defragment_block(id_defrag, pos_block, pos_start, files, empty):
    while files[pos_block] > 0:
        id_defrag.append(pos_block)
        files[pos_block] -= 1
        empty[pos_start] -= 1
        if empty[pos_start] == 0 and pos_block > pos_start + 1:
            while empty[pos_start] == 0:
                pos_start += 1
                id_defrag.extend([pos_start for _ in range(files[pos_start])])

    return pos_block, pos_start

def fill_empty_space(id_defrag, pos_block, pos_start, files, empty):
    print("fillin position : ", pos_start, " with space : ", empty[pos_start])
    found = False
    while empty[pos_start] > 0 and pos_block > pos_start:
        print("  trying to fill block position : ", pos_block, " with space : ", files[pos_block])
        if (files[pos_block] > 0 and files[pos_block] <= empty[pos_start]):
            found = True
            print("  block position : ", pos_block, " with space : ", files[pos_block], " can be moved")
            id_defrag.extend([pos_block for _ in range(files[pos_block])])
            empty[pos_start] -= files[pos_block]
            files[pos_block] = 0
            pos_block -= 1
        else:
            pos_block -= 1

    return pos_block, pos_start, found

def move_file(id_defrag, pos_block, files, empty, empty_new_files):
    pos_start = 0
    found = False
    while not found and pos_start < pos_block:
        if empty[pos_start] > files[pos_block]:
            found = True
            empty[pos_start] -= files[pos_block]
            empty_new_files[pos_start] = (pos_block, files[pos_block])
        else:
            pos_start += 1

def build_id_defrag(files, empty, emtpy_new_files):
    id_defrag = []
    pos = 0
    for iblock in range(len(files)):
        id_defrag.append([iblock for _ in range(files[iblock])])
        empty_size = empty[iblock]
        for ifile in emtpy_new_files:
            id_defrag.append([ifile for _ in range(files[iblock])])

    return id_defrag

def compute_checksum(id_defrag):
    return sum(i * idx for idx, i in enumerate(id_defrag))

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0][0]
    files = [int(data[i]) for i in range(0,len(data),2)]
    empty = [int(data[i]) for i in range(1,len(data),2)]

    if part == '1':
        pos_start = 0
        pos_block = len(files) - 1
        id_defrag = [pos_start for _ in range(files[pos_start])]
        while pos_start < pos_block:
            pos_block, pos_start = defragment_block(id_defrag, pos_block, pos_start, files, empty)
            pos_block -= 1

        print("Result of part 1: ", compute_checksum(id_defrag))

    elif part == '2':
        pos_start = 0
        id_defrag = []
        found = True
        while found:
            id_defrag = id_defrag + [pos_start for _ in range(files[pos_start])]
            pos_block = len(files) - 1
            pos_block, pos_start, found = fill_empty_space(id_defrag, pos_block, pos_start, files, empty)
            pos_start += 1
            print(id_defrag)

        print("Result of part 2: ", compute_checksum(id_defrag))