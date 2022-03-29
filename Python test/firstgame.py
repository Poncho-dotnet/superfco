import pygame

screen = pygame.display.set_mode((500, 500))
screen.fill((255, 255, 255))


# pick a font you have and set its size
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)
# apply it to text on a label
label = myfont.render("Python and Pygame are Fun!", 1, (100,100,100))
# put the label object on the screen at point x=100, y=100
screen.blit(label, (100, 100))

while True:
    pygame.display.update()

    pygame.time.delay(100)