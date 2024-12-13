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

def move_file(pos_block, files, empty, files_id, empty_id):
    if (files[pos_block] == 0):
        return

    found = False
    pos_start = 0
    while not found and pos_start < pos_block:
        if empty[pos_start] >= files[pos_block]:
            found = True
            empty[pos_start] -= files[pos_block]
            empty_id[pos_start].extend([pos_block for _ in range(files[pos_block])])
            files_id[pos_block] = [0 for _ in range(files[pos_block])]
            files[pos_block] = 0
        else:
            pos_start += 1

def build_id_defrag(files, empty, files_id, empty_id):
    id_defrag = files_id[0]
    for i in range(1, len(files)):
        id_defrag = id_defrag + empty_id[i-1] + [0 for _ in range(empty[i-1])] + files_id[i]

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
        files_id = [[i for _ in range(files[i])] for i in range(len(files))]
        empty_id = [[] for _ in range(len(empty))]
        pos_block = len(files) - 1
        while sum(empty[0:pos_block]) > 0:
            move_file(pos_block, files, empty, files_id, empty_id)
            pos_block -= 1

        id_defrag = build_id_defrag(files, empty, files_id, empty_id)

        print("Result of part 2: ", compute_checksum(id_defrag))