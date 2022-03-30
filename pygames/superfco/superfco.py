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
from terrainutils import EnumEntities
from entities import Player, Wall, Water, Goal, OxygenTank, Text, Cannon, CannonBall

# game constants
PLAYER_IMG = 'player.png'
WALL_IMG = 'wall.png'
WATER_IMG = 'water.png'
GOAL_IMG = 'goal.png'
OXYGENTANK_IMG = 'oxygentank.png'
CANNON_IMG = 'cannon.png'
CANNONBALL_IMG = 'cannonball.png'
IMAGES_FOLDER = 'images'
CURRENT_PATH = os.getcwd()
LEVEL_FOLDER = 'levels'
LEVEL_FILENAME = 'level{:02d}.dat'
SCREENRECT = pygame.Rect(0, 0, 800, 600)
FRAMERATE = 60

COLUMNS = 80
ROWS = 23

# ======================================================
#                      Level play
# ======================================================

def draw_level(structure):
    for idxrow, row in enumerate(structure):
        for idxcol, col in enumerate(row):
            if col == EnumEntities.WALL:
                Wall(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == EnumEntities.PLAYER:
                player = Player(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == EnumEntities.GOAL:
                Goal(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == EnumEntities.WATER:
                Water(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == EnumEntities.OXYGEN:
                OxygenTank(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)
            if col == EnumEntities.CANNON:
                Cannon(idxcol, idxrow, SCREENRECT, COLUMNS, ROWS)

    return player 


def play_level(screen, currentlvl, lives):
    # create the background
    background = pygame.Surface(SCREENRECT.size)
    background.fill(color = (0, 0, 0))
    screen.blit(background, (0, 0))    

    # Initialize Game Groups
    walls = pygame.sprite.Group()
    water = pygame.sprite.Group()
    oxygen = pygame.sprite.Group()
    cannons = pygame.sprite.Group()
    cannonballs = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    messages = pygame.sprite.Group()
    todos = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    Player.containers = todos
    Wall.containers = walls, todos
    Water.containers = water, todos
    OxygenTank.containers = oxygen, todos
    Cannon.containers = cannons, todos
    CannonBall.containers = cannonballs, todos
    Goal.containers = goals, todos
    Text.containers = messages, todos

    # initialize our starting sprites
    structure = terrainutils.get_level_structure(CURRENT_PATH, LEVEL_FOLDER, LEVEL_FILENAME.format(currentlvl))
    player = draw_level(structure)

    # debug text
    debugtext = Text("Starting...", 10, (200,200,200), 500, 20, [0,0])
    livestext = Text(f"LEVEL {currentlvl}, LIVES = {lives}", 20, (100,200,100), 200, 25, (SCREENRECT.width - 200,0))

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
        isfloating = terrainutils.is_floating(paredescercanas, player)    
        isdiving = paredescercanas.iswater

        if tienesustento:
            player.hspeed=0
            player.vspeed=0

        if keys[pygame.K_KP6]:
            if isdiving:
                player.move_lat(0.5, ticks)
            elif tienepiso:
                player.move_lat(1, ticks)
        if keys[pygame.K_KP4]: 
            if isdiving:
                player.move_lat(-0.5, ticks)
            elif tienepiso:
                player.move_lat(-1, ticks)
        
        if keys[pygame.K_KP8]:
            if paredescercanas.abajo == player.posy:
                player.jump(ticks)
                player.hspeed = 0   
            elif tienesustento or isdiving:
                player.move_vert(-1, ticks)             
        if keys[pygame.K_KP2] and tienesustento:
            player.move_vert(1, ticks)

        if keys[pygame.K_KP9] and tienepiso and player.posx < paredescercanas.derecha:
            player.jump_lat(1, ticks)
        if keys[pygame.K_KP7] and tienepiso and player.posx > paredescercanas.izquierda:
            player.jump_lat(-1, ticks)

        # grabbing oxygen tank
        if pygame.sprite.spritecollide(player, oxygen, 1):
            player.has_oxygen = True

        # if the player is in the air        
        if isfloating:
            player.fall(ticks)

        # if player is diving in the water
        if isdiving:
            player.dive(ticks)

        # update
        player.updatepos(paredescercanas)        

        # cannons
        for cannon in cannons:
            cannon.fire(ticks)
            
            for cannonball in cannon.bullets:
                cannonball.move(ticks)

                if pygame.sprite.spritecollide(cannonball, walls, 0):
                    cannonball.kill()
                    cannon.bullets.remove(cannonball)
        
        if pygame.sprite.spritecollide(player, cannonballs, 0):
            player.die()

        # display debug info
        debugtext.set_text(f'x: {player.posx:.2f}, y: {player.posy:.2f}, air? {isfloating}, paredes: {paredescercanas}')            

        # draw the scene
        dirty = todos.draw(screen)
        pygame.display.update(dirty)
        pygame.event.pump()

        # detect end of level
        if pygame.sprite.spritecollide(player, goals, 0):
            return "goal"

        # detect dead
        if player.is_dead:
            pygame.time.delay(1000)
            return "dead"

        # cap the framerate
        ticks = clock.tick(FRAMERATE)

# ======================================================
#                         Main
# ======================================================

# loads an image, prepares it for play
def load_image(file):
    file = os.path.join(CURRENT_PATH, IMAGES_FOLDER, file)

    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))

    result = surface.convert()
    result = pygame.transform.scale(result, (round(SCREENRECT.width / COLUMNS), round(SCREENRECT.height / ROWS)))
    result.set_colorkey((0,0,0))
    return result

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
    Wall.images = [wall_img]

    water_img = load_image(WATER_IMG)
    Water.images = [water_img]

    oxygen_img = load_image(OXYGENTANK_IMG)
    OxygenTank.images = [oxygen_img]

    cannon_img = load_image(CANNON_IMG)
    Cannon.images = [cannon_img]

    cannonball_img = load_image(CANNONBALL_IMG)
    CannonBall.images = [cannonball_img]

    goal_img = load_image(GOAL_IMG)
    Goal.images = [goal_img]

    player_img = load_image(PLAYER_IMG)
    Player.images = [player_img, pygame.transform.scale(player_img, (SCREENRECT.width / COLUMNS, SCREENRECT.height / ROWS / 2))]

    # global vars
    currentlvl = 1
    lives = 5
    
    # starto!
    while lives > 0:
        screen.fill( color = (0,0,0))
        pygame.display.update()

        result = play_level(screen, currentlvl, lives)

        if result == "goal":
            currentlvl += 1
        if result == "dead":
            lives -= 1
        if result == "quit":
            return

    if lives == 0:
        # come back to start screen
        pass


# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pygame.quit()