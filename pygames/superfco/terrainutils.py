from enum import IntEnum
import math
import os

def get_level_structure(*argv) -> str:
    level_structure = []

    with open(os.path.join(*argv), 'r') as f:
        for line in f:
            level_structure.append(get_level_row_structure(line.strip()))

    return level_structure


def get_level_row_structure(line: str) -> str:
    if not line:
        return [1 for i in range(80)]
    if line == "0":
        return [1 for i in range(80)]
    
    if len(line) != 80:
        print ("Line must have 80 chars length")
        print (line)
        raise ValueError

    return [int(char) for char in line]


class CollisionModel:
    def __init__(self, abajo, arriba, derecha, izquierda) -> None:
        self.abajo = abajo
        self.arriba = arriba
        self.derecha = derecha
        self.izquierda = izquierda
        self.isterraincorner = False
        self.ismapborder = False
        self.iswater = False

    def __str__(self):
        return f'd={self.derecha},i={self.izquierda},ab={self.abajo},ar={self.arriba},esq={self.isterraincorner},borde={self.ismapborder}'

class EnumEntities(IntEnum):
    EMPTY = 1,
    WALL = 2,
    PLAYER = 3,
    GOAL = 4,
    WATER = 6,
    CANNON = 7,
    OXYGEN = 8

# userful vars
passable_terrain = [EnumEntities.EMPTY, EnumEntities.WATER, EnumEntities.GOAL]
blocked_terrain = [EnumEntities.WALL, EnumEntities.CANNON]

def get_paredes_cercanas(level_structure, player):
    rows = len(level_structure)
    cols = len(level_structure[0])
    playerx, playery = player.posx, player.posy
    
    # border conditions
    result = CollisionModel(abajo=rows-1, arriba=0, derecha=cols-1, izquierda=0)
    result.ismapborder = True if playerx == result.izquierda or playerx == result.derecha else False
    
    for wally, row in enumerate(level_structure):
        for wallx, col in enumerate(row):
            if col in blocked_terrain:
                if wallx-1 >= playerx and abs(playery - wally) < 1:
                    if wallx - 1 < result.derecha:
                        result.derecha = wallx - 1
                if wallx+1 <= playerx and abs(playery - wally) < 1:
                    if wallx + 1 > result.izquierda:
                        result.izquierda = wallx + 1
                
                if wally-1 >= playery and abs(playerx - wallx) < 1:
                    if wally - 1 < result.abajo:
                        result.abajo = wally - 1
                if wally+1 <= playery and abs(playerx - wallx) < 1:
                    if wally + 1 > result.arriba:
                        result.arriba = wally + 1
            if col == EnumEntities.WATER:
                if abs(playerx - wallx) < 1 and abs(playery - wally) < 1:
                    result.iswater = True

    # first we check if player is near border/grid
    intx, inty = round(playerx), round(playery)

    # ??????  is not corner    ???   is corner     ???    is not corner
    #  ???                    ???                ??????

    if abs(inty - playery) < 0.05 and abs(intx - playerx) < 0.05:
        # then we check if down is empty and diagonal is blocked
        if intx < cols and level_structure[inty+1][intx] in passable_terrain and level_structure[inty][intx+1] in passable_terrain and level_structure[inty+1][intx+1] in blocked_terrain:
            result.isterraincorner = True
        if intx > 0 and level_structure[inty+1][intx] in passable_terrain and level_structure[inty][intx-1] in passable_terrain  and level_structure[inty+1][intx-1] in blocked_terrain:
            result.isterraincorner = True

    return result

def is_floating(paredes: CollisionModel, player):
    playerx, playery = player.posx, player.posy

    if tiene_sustento(paredes, player):
        return False
    if paredes.isterraincorner:
        return False

    if playery < paredes.abajo and playery >= paredes.arriba:
        return True
    else:
        return False

def tiene_sustento(paredes: CollisionModel, player):
    playerx, playery = player.posx, player.posy

    if playery == paredes.abajo:
        return True
    elif paredes.ismapborder:
        return False

    if playerx == paredes.derecha:
        return True
    if playerx == paredes.izquierda: 
        return True

    return False

def tiene_piso(paredes: CollisionModel, player):
    playerx, playery = player.posx, player.posy

    if paredes.isterraincorner:
        return True
    if playery == paredes.abajo:
        return True

    return False