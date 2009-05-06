#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *

ScrSize = (300,600)
Origin  = (0,0)
ImageName = 'bgImage.bmp'

def main():
    """ A basic example of scrollbar code inline.
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
        world.fill((200,200,200))
        pygame.display.set_caption(ImageName + " not found")
        
    worldRect     = world.get_rect()
    ratio       = (1.0 * screenRect.width) / worldRect.width
    scrollThick = 20
    scroll      = pygame.Rect(
        screenRect.left,
        screenRect.bottom - scrollThick,
        screenRect.width, scrollThick )
    
    bar         = pygame.Rect(scroll)  
    bar.width   = scroll.width * ratio
    scrolling   = False

    while 1:

            event = pygame.event.wait()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
            
            elif ( event.type == MOUSEMOTION and
                 scrolling and
                 scroll.contains(bar.move(event.rel[0],0)) ):
                
                bar.center = bar.center[0] + event.rel[0], bar.center[1]

            elif event.type == MOUSEBUTTONDOWN and bar.collidepoint(event.pos):
                scrolling = True                    
                    
            elif event.type == MOUSEBUTTONUP:
                scrolling = False

                
            screen.fill( (192,188,180) )
            screen.blit(world, ( (bar.left / ratio) * -1 , 0) )
            pygame.draw.rect( screen, (180,180,180), scroll, 0 )
            pygame.draw.rect( screen, (140,140,140), bar.inflate(0,-5), 0 )

            pygame.display.flip()

### Tells what to launch in IDE and windows double click of file.
if __name__ == '__main__': main()
