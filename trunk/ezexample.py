#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *
import ezscroll

ScrSize = (200,400)
Origin  = (0,0)
Red     = (255,0,0)
Gray    = (200,200,200)
ImageName = 'bgImage.bmp'

def main():
    """ Sample program for the ezscroll module.

    Tweak the ez constructor arguments.

    """
    
    pygame.init()
    screen = pygame.display.set_mode(ScrSize)
    world = loadImage(ImageName)

    if world:
        pygame.display.set_caption(ImageName)
    else:        
        pygame.display.set_caption(ImageName + " not found")
        world = pygame.Surface((ScrSize[0]*2, ScrSize[1]*2))
        world.fill(Gray)
 
    # Git it 'n' blit it:
    ez = ezscroll.EZScroll(
        world,             # pygame.Surface that needs to be scrolled
        screen.get_rect(), # porthole that limits view
        20,                # scroll bar 'thickness'
        ezscroll.BOTH,     # H scrollbars: TOP, BOTTOM, BOTH, or NEITHER
        ezscroll.BOTH,     # V scrollbars: LEFT, RIGHT, BOTH, or NEITHER
        Origin,            # initial position
        2,                 # internal padding
        True,              # use highlight and drop shadow
        None,              # (trackColor, knobColor)
        None,              # (highlightColor, shadowColor)
        None)              # user-supplied scrollPane
 
    scrollPane = ez.scrollPane
    screen.blit(scrollPane, Origin)
    pygame.display.flip()

    while 1:

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        # adjPos modifies event.pos by offsets and scrolled distance.        
        # adjPos is returned as None if the event passed has no pos,
        # but we'll still limit it to MOUSE events:
        if event.type in [MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN]:

            scrolling, adjPos = ez.handleEvent(event)

            if event.type == MOUSEBUTTONDOWN and adjPos and not scrolling:   
               pygame.draw.circle(world, Red, adjPos, 10, 4)  

        screen.blit(scrollPane, Origin)
        pygame.display.flip()

    


# utilty loads image whether example is run from
# current directory or from import of module.
def loadImage(ImageName):

    import os
    import sys
        
    try: return pygame.image.load(ImageName).convert()
    except: print ImageName, " not found:", sys.exc_info()[0]

    try:
        pathHere = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))    
        return pygame.image.load(os.path.join(pathHere,ImageName)).convert()
    except: # name __file__ not recognized -- running from curdir
        if pathHere: print "Not found in ", pathHere

    finally:
        print ImageName, " not found:", sys.exc_info()[0]
        return None  
    

if __name__ == '__main__': main()

