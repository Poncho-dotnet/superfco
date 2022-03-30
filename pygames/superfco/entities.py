import pygame

# ======================================================
#                     Game classes
# ======================================================

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, posx, posy, screen, cols, rows):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        self.posx = posx
        self.posy = posy

        self.screenrect = screen
        self.cols = cols
        self.rows = rows

        self.rect.x = self.posx * screen.width / cols
        self.rect.y = self.posy * screen.height / rows

# represented by ascii character x01
class Player(BaseEntity):
    hmaxspeed = 10 # 10 tiles per second
    vmaxspeed = 2
    v_acceleration = 0.02
    v_jump = -7
    
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)
        self.vspeed = 0.0
        self.hspeed = 0
        self.is_dead = False

    def move_lat(self, direction, ticks):
        self.posx += direction * self.hmaxspeed * ticks / 1000

    def move_vert(self, direction, ticks):
        self.posy += direction * self.vmaxspeed * ticks / 1000
        
    def jump(self, ticks):  
        self.vspeed = self.v_jump
        self.posy += self.vspeed * ticks / 1000

    def jump_lat(self, direction, ticks):  
        self.jump(ticks)        
        self.hspeed = direction * self.hmaxspeed / 1.3
        self.posx += self.hspeed * ticks / 1000

    def fall(self, ticks):
        self.vspeed += ticks * self.v_acceleration
        self.posy += self.vspeed * ticks / 1000
        self.posx += self.hspeed * ticks / 1000

    def updatepos(self, borde):
        if self.posx < borde.izquierda:
            self.posx = borde.izquierda
            self.hspeed = 0

            # if hitting wall downwards, just fall
            if self.vspeed > 0.1:
                self.posx -= 0.01

        if self.posx > borde.derecha:
            self.posx = borde.derecha
            self.hspeed = 0

            # if hitting wall downwards, just fall
            if self.vspeed > 0.1:
                self.posx -= 0.01

        if self.posy < borde.arriba:
            self.posy = borde.arriba
            self.vspeed = 0
        if self.posy > borde.abajo:
            if self.vspeed > 1.0:
                self.is_dead = True
                self.image = self.images[1]

            self.posy = borde.abajo
            self.vspeed = 0

        self.rect.x = self.posx * self.screenrect.width / self.cols
        self.rect.y = self.posy * self.screenrect.height / self.rows

class Wall(BaseEntity):
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

class Water(pygame.sprite.Sprite):
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

class Goal(pygame.sprite.Sprite):
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height, position):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.color = color
        self.width = width
        self.height = height
        self.position = position

        self.font = pygame.font.SysFont("Comic Sans MS", size)
        self.surface = self.font.render(text, 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.blit(self.surface, [0,0])
        
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def set_text(self, text):
        self.surface = self.font.render(text, 1, self.color)
        self.image = pygame.Surface((self.width, self.height))
        self.image.blit(self.surface, [0,0])