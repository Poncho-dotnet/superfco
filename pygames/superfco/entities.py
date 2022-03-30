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

        BaseEntity.update_rect(self)

    def update_rect(self):
        self.rect.x = self.posx * self.screenrect.width / self.cols
        self.rect.y = self.posy * self.screenrect.height / self.rows

# represented by ascii character x01
class Player(BaseEntity):
    hmaxspeed = 10 # 10 tiles per second
    vmaxspeed = 2
    v_acceleration = 0.02
    v_jump = -7
    water_drag = 0.2
    air_drag = 0.05
    
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)
        self.vspeed = 0.0
        self.hspeed = 0
        self.is_dead = False
        self.has_oxygen = False

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

    def dive(self, ticks):
        self.vspeed = self.vspeed * (1-self.water_drag) * (1-ticks / 1000)
        self.hspeed = self.hspeed * (1-self.water_drag) * (1-ticks / 1000)

        # death by drowning
        if not self.has_oxygen:
            self.die()

    def die(self):
        self.is_dead = True
        self.image = self.images[1]

    def updatepos(self, collision):
        if self.posx < collision.izquierda:
            self.posx = collision.izquierda
            self.hspeed = 0

            # if hitting wall downwards, just fall
            if self.vspeed > -self.v_jump / 2: 
                self.posx += 0.01

        if self.posx > collision.derecha:
            self.posx = collision.derecha
            self.hspeed = 0

            # if hitting wall downwards, just fall
            if self.vspeed > -self.v_jump / 2:
                self.posx -= 0.01

        if self.posy < collision.arriba:
            self.posy = collision.arriba
            self.vspeed = 0
        if self.posy > collision.abajo:
            # death by falling too fast
            if self.vspeed > -self.v_jump * 2:
                self.die()

            self.posy = collision.abajo
            self.vspeed = 0

        # important!
        self.update_rect()

class Cannon(BaseEntity):
    maxbullets = 2
    firedelay = 3000

    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

        self.bullets = []
        self.lastfire = 0

        # first bullet
        self.fire(self.firedelay)

    def fire(self, ticks):
        self.lastfire += ticks
        numbullets = len(self.bullets)

        if numbullets < self.maxbullets and self.lastfire > self.firedelay:
            self.bullets.append(CannonBall(self.posx, self.posy, self.screenrect, self.cols, self.rows))
            self.lastfire = 0

class CannonBall(BaseEntity):
    speed = -8

    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

    def move(self, ticks):
        self.posx += self.speed * ticks / 1000
        self.update_rect()

class Wall(BaseEntity):
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

class Water(pygame.sprite.Sprite):
    def __init__(self, posx, posy, screen, cols, rows):
        BaseEntity.__init__(self, posx, posy, screen, cols, rows)

class OxygenTank(pygame.sprite.Sprite):
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