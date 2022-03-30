""" superfco game
Classic pascal game from the 90s, refactored to modern style python
* full ascii art graphics
* full blown out 80x40 120fps resolution

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
import os
import terrainutils
import entities

# game constants
PLAYER_IMG = 'player.png'
WALL_IMG = 'wall.png'
WATER_IMG = 'water.png'
GOAL_IMG = 'goal.png'
CANNONBALL_IMG = 'cannonball.png'
CURRENT_PATH = os.getcwd()
LEVEL_FILENAME = 'ETAPA{:02d}.PAS'
SCREENRECT = pygame.Rect(0, 0, 800, 600)
FRAMERATE = 60

COLUMNS = 80
ROWS = 22

# loads an image, prepares it for play
def load_image(file):
    file = os.path.join(CURRENT_PATH, file)

    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()


# ======================================================
#                      Level play
# ======================================================

def draw_level(structure):
    for idxrow, row in enumerate(structure):
        for idxcol, col in enumerate(row):
            if col == 2:
                entities.Wall(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == 3:
                player = entities.Player(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == 4:
                entities.Goal(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == 6:
                entities.Water(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)

    return player 


def play_level(screen, currentlvl):
    # create the background
    background = pygame.Surface(SCREENRECT.size)
    background.fill(color = (0, 0, 0))
    screen.blit(background, (0, 0))    

    # Initialize Game Groups
    walls = pygame.sprite.Group()
    water = pygame.sprite.Group()
    cannons = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    messages = pygame.sprite.Group()
    todos = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    entities.Player.containers = todos
    entities.Wall.containers = walls, todos
    entities.Water.containers = water, todos
    entities.Text.containers = messages, todos
    entities.Goal.containers = goals, todos

    # initialize our starting sprites
    structure = terrainutils.get_level_structure(CURRENT_PATH, LEVEL_FILENAME.format(currentlvl))
    player = draw_level(structure)

    # debug text
    debugtext = entities.Text("Starting...", 10, (200,200,200), 500, 50)

    # setup clock
    clock = pygame.time.Clock()
    ticks = 0

    while True:
        # update all the sprites
        todos.clear(screen, background)
        todos.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # update movement
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            return "quit"

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
            if paredescercanas.abajo == player.posy:
                player.jump(ticks)
                player.hspeed = 0   
            elif tienesustento:
                player.move_vert(-1, ticks)             
        if keys[pygame.K_KP2] and tienesustento:
            player.move_vert(1, ticks)

        if keys[pygame.K_KP9] and tienepiso and player.posx < paredescercanas.derecha:
            player.jump_lat(1, ticks)
        if keys[pygame.K_KP7] and tienepiso and player.posx > paredescercanas.izquierda:
            player.jump_lat(-1, ticks)

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

        # detect end of level
        for goal in pygame.sprite.spritecollide(player, goals, 0):
            return "goal"

        # cap the framerate
        ticks = clock.tick(FRAMERATE)

# ======================================================
#                         Main
# ======================================================

def main():
    # init screen
    pygame.init()
    pygame.font.init()
    winstyle = 0 | pygame.DOUBLEBUF  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)    
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption("superfco")

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    wall_img = load_image(WALL_IMG)
    wall_img = pygame.transform.scale(wall_img, (SCREENRECT.width / COLUMNS, SCREENRECT.height / ROWS))
    wall_img.set_colorkey((0,0,0))
    entities.Wall.images = [wall_img]

    water_img = load_image(WATER_IMG)
    water_img = pygame.transform.scale(water_img, (SCREENRECT.width / COLUMNS, SCREENRECT.height / ROWS))
    water_img.set_colorkey((0,0,0))
    entities.Water.images = [water_img]

    goal_img = load_image(GOAL_IMG)
    goal_img = pygame.transform.scale(goal_img, (SCREENRECT.width / COLUMNS, SCREENRECT.height / ROWS))
    goal_img.set_colorkey((0,0,0))
    entities.Goal.images = [goal_img]

    player_img = load_image(PLAYER_IMG)
    player_img = pygame.transform.scale(player_img, (SCREENRECT.width / COLUMNS, SCREENRECT.height / ROWS))
    player_img.set_colorkey((0,0,0))
    entities.Player.images = [player_img]

    # global vars
    currentlvl = 3
    
    # starto!
    while True:
        screen.fill( color = (0,0,0))
        pygame.display.update()

        result = play_level(screen, currentlvl)

        if (result == "goal"):
            currentlvl += 1
        if (result == "quit"):
            return


# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pygame.quit()