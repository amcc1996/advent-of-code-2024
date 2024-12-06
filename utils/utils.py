import os
import sys


def get_input_filename(path):
    DATAFILE = 'data.txt'
    VALIDATION_PT1 = 'validation-part1.txt'
    VALIDATION_PT2 = 'validation-part2.txt'

    if len(sys.argv) < 2:
        print('Usage: python main.py <part> [v]')
        sys.exit(1)

    part = sys.argv[1]
    validation = False
    if len(sys.argv) > 2:
        validation = (sys.argv[2] == 'v')

    datafile = DATAFILE
    if validation:
        if part == '1':
            datafile = VALIDATION_PT1
        else:
            datafile = VALIDATION_PT2

    return os.path.join(path, datafile), part


def read_input_file(filename, n_blocks=1):
    with open(filename) as f:
        return [x.splitlines() for x in f.read().split('\n\n')]