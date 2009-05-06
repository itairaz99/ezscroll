#! %PYTHONPATH%\python
import pygame, os, sys
from pygame import *
import ezscroll

ScrSize = (200,400)
Origin  = (0,0)
Color   = (255,0,0)
ImageName = 'bgImage.bmp'

def main():
    
    pygame.init()
    screen = pygame.display.set_mode(ScrSize)
    image = loadImage(ImageName)
    print image

    ez = ezscroll.EZScroll(
        image,             # what needs to be scrolled
        screen.get_rect(), # porthole that limits view
        20,                # scroll thickness
        ezscroll.BOTH,   # which horiz scrollbars
        ezscroll.BOTH,     # which vertical scrollbars
        Origin,            # initial position
        0,                 # internal padding
        True,              # use highlight and drop shadow
        None,              # (trackColor, knobColor)
        None,              # (highlightColor, shadowColor)
        None)              # user-supplied scrollPane

    scrollPane = ez.scrollPane
    screen.blit(scrollPane, (0,0))
    pygame.display.flip()

    while 1:

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
            
        # Note: offset event pos by thickness and scrolled distance
        scrolling, adjPos = ez.handleEvent(event)
        if event.type == MOUSEBUTTONDOWN and adjPos and not scrolling:   
           pygame.draw.circle(image, Color, adjPos, 10, 4)  

        screen.blit(scrollPane, Origin)
        pygame.display.flip()

    

# loads image whether example is run from
# current directory or from import of module.
def loadImage(ImageName):

    import os
    import sys
        
    try: return pygame.image.load(ImageName).convert()
    except :
        print "\nUnexpected error:", sys.exc_info()[0]
        print "probably can't find the image file: ", ImageName

    try:
        print "\nTrying to find it as if running from Python shell..."
        pathHere = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))    
        return pygame.image.load(os.path.join(pathHere,ImageName)).convert()
    except NameError: # name __file__ not recognized -- running from curdir
        print "Error again!"

    else:
        print "\nNo luck finding your image file ",\
              ImageName," in the same dir as ezScroll.py"
        return None  
    

if __name__ == '__main__': main()

