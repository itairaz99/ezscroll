#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *

ScrSize = (300,600)
Origin  = (0,0)
Gray    = (200,200,200)
ImageName = 'bgImage.bmp'

def main():
    """ A basic example of scrollknob code inline.
        Does not use ezscroll module.
    """
    
    pygame.init()
    screen      = pygame.display.set_mode(ScrSize)
    screenRect  = screen.get_rect()
    world       = None

    try:
        world = pygame.image.load(ImageName).convert()
    except:
        print "Can't find ", ImageName
        world = pygame.Surface((ScrSize[0]*2, ScrSize[1]*2))
        world.fill(Gray)
        pygame.display.set_caption(ImageName + " not found")
        
    worldRect   = world.get_rect()
    ratio       = (1.0 * screenRect.width) / worldRect.width
    scrollThick = 20
    track = pygame.Rect(
        screenRect.left,
        screenRect.bottom - scrollThick,
        screenRect.width, scrollThick )
    
    knob        = pygame.Rect(track)  
    knob.width   = track.width * ratio
    scrolling   = False

    while 1:

            event = pygame.event.wait()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
            
            elif ( event.type == MOUSEMOTION and
                 scrolling):

                if event.rel[0] != 0:
                    move = max(event.rel[0], track.left - knob.left)
                    move = min(move, track.right - knob.right)

                    if move != 0:
                        knob.move_ip((move, 0))
                            
            elif event.type == MOUSEBUTTONDOWN and knob.collidepoint(event.pos):
                scrolling = True                    
                    
            elif event.type == MOUSEBUTTONUP:
                scrolling = False

                
            screen.fill( (192,188,180) )
            screen.blit(world, ( (knob.left / ratio) * -1 , 0) )
            pygame.draw.rect( screen, (180,180,180), track, 0 )
            pygame.draw.rect( screen, (140,140,140), knob.inflate(0,-5), 0 )

            pygame.display.flip()

### Tells what to launch in IDE and windows double click of file.
if __name__ == '__main__': main()
