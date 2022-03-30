import math

class Coordenadas:
    def __init__(self, abajo, arriba, derecha, izquierda) -> None:
        self.abajo = abajo
        self.arriba = arriba
        self.derecha = derecha
        self.izquierda = izquierda
        self.esesquina = False
        self.esbordemapa = False

    def __str__(self):
        return f'd={self.derecha},i={self.izquierda},ab={self.abajo},ar={self.arriba},esq={self.esesquina},borde={self.esbordemapa}'


def get_paredes_cercanas(level_structure, player):
    rows = len(level_structure)
    cols = len(level_structure[0])
    playerx, playery = player.posx, player.posy
    
    # inicializamos con condiciones de borde
    result = Coordenadas(abajo=rows-1, arriba=0, derecha=cols-1, izquierda=0)
    result.esbordemapa = True if playerx == result.izquierda or playerx == result.derecha else False
    
    for wally, row in enumerate(level_structure):
        for wallx, col in enumerate(row):
            # pared
            if col == 2:
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

    # revisamos si el player está justo al lado de una cornisa
    intx, inty = round(playerx), round(playery)

    # necesitamos comprobar primero que el player esté cerca del borde
    if abs(inty - playery) < 0.05 and abs(intx - playerx) < 0.05:
        if intx < cols and level_structure[inty+1][intx] == 1 and level_structure[inty+1][intx+1] == 2:
            result.esesquina = True
        if intx > 0 and level_structure[inty+1][intx] == 1 and level_structure[inty+1][intx-1] == 2:
            result.esesquina = True

    return result

def is_floating(paredes: Coordenadas, player):
    playerx, playery = player.posx, player.posy

    if tiene_sustento(paredes, player):
        return False
    if paredes.esesquina:
        return False

    if playery < paredes.abajo and playery >= paredes.arriba:
        return True
    else:
        return False

def tiene_sustento(paredes: Coordenadas, player):
    playerx, playery = player.posx, player.posy

    if playery == paredes.abajo:
        return True
    elif paredes.esbordemapa:
        return False

    if playerx == paredes.derecha:
        return True
    if playerx == paredes.izquierda: 
        return True

    return False

def tiene_piso(paredes: Coordenadas, player):
    playerx, playery = player.posx, player.posy

    if paredes.esesquina:
        return True
    if playery == paredes.abajo:
        return True

    return False