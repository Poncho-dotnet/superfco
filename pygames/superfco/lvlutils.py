import os
import superfco

def get_level_structure(currentpath: str, level_file: str) -> str:
    level_structure = []

    with open(os.path.join(currentpath, level_file), 'r') as f:
        for line in f:
            level_structure.append(get_level_row_structure(line.strip()))

    return level_structure


def get_level_row_structure(line: str) -> str:
    if not line:
        return [1 for i in range(80)]
    if line == "0":
        return [1 for i in range(80)]
    
    if len(line) != 80:
        print ("Línea no tiene largo 80")
        print (line)
        raise ValueError

    return [int(char) for char in line]


def draw_level(level_structure, playerclass, wallclass, goalclass):    
    for idxrow, row in enumerate(level_structure):
        for idxcol, col in enumerate(row):
            if col == 2:
                wallclass(idxcol, idxrow)
            if col == 3:
                player = playerclass(idxcol, idxrow)
            if col == 4:
                goalclass(idxcol, idxrow)

    return player 