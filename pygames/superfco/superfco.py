""" superfco game
Classic pascal game from de 90s, refactored to modern style python
* full ascii art graphics
* full out blown 80x40 120fps resolution

Controls
--------
* Numpad used
* 4 -> left
* 6 -> right
* 2 -> crouch, swim down
* 3 -> swim down-right
* 1 -> swim down-left
* 8 -> jump up
* 9 -> jump up-right
* 7 -> jump up-left
"""

# import modules
import pygame
import lvlutils
import os
import terrainutils

# game constants
PLAYER_IMG = 'player.png'
WALL_IMG = 'wall.png'
CANNONBALL_IMG = 'cannonball.png'
SCREENRECT = pygame.Rect(0, 0, 800, 600)
FRAMERATE = 60

COLUMNS = 80
ROWS = 22


# initialization
currentpath = os.getcwd()
level_file = 'ETAPA01.PAS'

# loads an image, prepares it for play
def load_image(file):
    file = os.path.join(currentpath, file)

    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()

# representado por un caracter ascii
class Player(pygame.sprite.Sprite):
    hmaxspeed = 10 # 10 espacios por segundo
    vmaxspeed = 2
    v_acceleration = 0.02
    v_jump = -8
    
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        self.posx = posx
        self.posy = posy
        self.vspeed = 0.0
        self.hspeed = 0
        
        self.rect.x = self.posx * SCREENRECT.width / COLUMNS
        self.rect.y = self.posy * SCREENRECT.height / ROWS

    def move_lat(self, direction, ticks):
        self.posx += direction * self.hmaxspeed * ticks / 1000

    def move_vert(self, direction, ticks):
        self.posy += direction * self.vmaxspeed * ticks / 1000
        
    def jump(self, ticks):  
        self.vspeed = self.v_jump
        self.posy += self.vspeed * ticks / 1000

    def fall(self, ticks):
        self.vspeed += ticks * self.v_acceleration
        self.posy += self.vspeed * ticks / 1000
        self.posx += self.hspeed * ticks / 1000

    def updatepos(self, borde):
        if (self.posx < borde.izquierda):
            self.posx = borde.izquierda
            self.hspeed = 0
        if (self.posx > borde.derecha):
            self.posx = borde.derecha
            self.hspeed = 0
        if (self.posy < borde.arriba):
            self.posy = borde.arriba
            self.vspeed = 0
        if (self.posy > borde.abajo):
            self.posy = borde.abajo
            self.vspeed = 0

        self.rect.x = self.posx * SCREENRECT.width / COLUMNS
        self.rect.y = self.posy * SCREENRECT.height / ROWS

class Wall(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = posx * SCREENRECT.width / COLUMNS
        self.rect.y = posy * SCREENRECT.height / ROWS
        self.posx = posx
        self.posy = posy


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.color = color
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Comic Sans MS", size)
        self.surface = self.font.render(text, 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.blit(self.surface, [0, 0])
        self.rect = self.image.get_rect()
    
    def set_text(self, text):
        self.surface = self.font.render(text, 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.blit(self.surface, [0, 0])


# ======================================================
#                         Main
# ======================================================

def main():
    # init screen
    pygame.init()
    pygame.font.init()
    fullscreen = False
    winstyle = 0 | pygame.DOUBLEBUF  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption("superfco")

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    wall_img = load_image(WALL_IMG)
    wall_img = pygame.transform.scale(wall_img, (SCREENRECT.width/80, SCREENRECT.height / 22))
    wall_img.set_colorkey((0,0,0))
    Wall.images = [wall_img]

    player_img = load_image(PLAYER_IMG)
    player_img = pygame.transform.scale(player_img, (SCREENRECT.width/80, SCREENRECT.height / 22))
    player_img.set_colorkey((0,0,0))
    Player.images = [player_img]

    # create the background, tile the bgd image
    background = pygame.Surface(SCREENRECT.size)
    background.fill(color = (0, 0, 0))
    screen.blit(background, (0, 0))    
    #pygame.display.flip()

    # Initialize Game Groups
    walls = pygame.sprite.Group()
    cannons = pygame.sprite.Group()
    mensajes = pygame.sprite.Group()
    todos = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    Player.containers = todos
    Wall.containers = walls, todos
    Text.containers = mensajes, todos

    # initialize our starting sprites
    structure = lvlutils.get_level_structure(currentpath, level_file)
    player = lvlutils.draw_level(structure, Player, Wall)

    # debug text
    debugtext = Text("Inicializando", 10, (200,200,200), 300, 50)

    # starting vars
    clock = pygame.time.Clock()
    ticks = 0
    #pygame.key.set_repeat(1000)    

    while True:
        # update all the sprites
        todos.clear(screen, background)
        todos.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_KP4:
            #         player.move(-1)
            #     elif event.key == pygame.K_KP6:
            #         player.move(1)

        # update movement
        keys = pygame.key.get_pressed()
        
        # calculamos espacio de maniobra
        paredescercanas = terrainutils.get_paredes_cercanas(structure, player)
        tienesustento = terrainutils.tiene_sustento(paredescercanas, player)
        tienepiso = terrainutils.tiene_piso(paredescercanas, player) or tienesustento

        if tienesustento:
            player.hspeed=0
            player.vspeed=0

        if keys[pygame.K_KP6] and tienepiso:
            player.move_lat(1, ticks)
        if keys[pygame.K_KP4] and tienepiso: 
            player.move_lat(-1, ticks)
        
        if keys[pygame.K_KP8]:
            if paredescercanas.derecha == player.posx or paredescercanas.izquierda == player.posx:
                player.move_vert(-1, ticks)
            elif paredescercanas.abajo == player.posy:
                player.jump(ticks)
                player.hspeed = 0                
        if keys[pygame.K_KP2] and tienesustento:
            player.move_vert(1, ticks)

        if keys[pygame.K_KP9] and tienepiso and player.posx < paredescercanas.derecha:
            player.jump(ticks)
            player.move_lat(1, ticks)
            player.hspeed = Player.hmaxspeed
        if keys[pygame.K_KP7] and tienepiso and player.posx > paredescercanas.izquierda:
            player.jump(ticks)
            player.move_lat(-1, ticks)
            player.hspeed = -Player.hmaxspeed

        # si está en el aire....
        isfloating = terrainutils.is_floating(paredescercanas, player)
        if isfloating == True:
            player.fall(ticks)

        # update
        player.updatepos(paredescercanas)

        # display debug info
        debugtext.set_text(f'x: {player.posx:.2f}, y: {player.posy:.2f}, air? {isfloating}, paredes: {paredescercanas}')
        
        # draw the scene
        dirty = todos.draw(screen)
        pygame.display.update(dirty)
        pygame.event.pump()

        # cap the framerate
        ticks = clock.tick(FRAMERATE)
        
        
# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pygame.quit()