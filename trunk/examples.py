import sys
import pygame
import ezscroll
from ezscroll import N,S,E,W, ScrollBar, ScrollPane

ScrSize = (300,600)
Origin  = (0,0)
Gray    = (200,200,200)

def examples():
    """ Examples of how to use ezscroll.
    One is a scrollpane, the other is a scrollbar.
    The scrollpane handles some things like offsets,
    puts the scrollbars in a sprite group, and blits the world.
    If you just want one scrollbar, still may be easier to
    use ScrollPane and pass [S] or [E], etc.
    Closing window of first example proceeds to next.
    """    
    pygame.init()
    screen = pygame.display.set_mode(ScrSize)
    world = pygame.Surface((ScrSize[0]*2, ScrSize[1]*2))
    world.fill(Gray)
    for x in xrange(100, world.get_size()[0], 200):
        for y in xrange(100, world.get_size()[1], 200):
            pygame.draw.circle(world, (225,34,43), (x,y), 100, 10)          
    bg = pygame.Surface(ScrSize).convert()
    
    ###  EXAMPLE 1
    bg.fill(Gray)
    pygame.display.set_caption("Example 1:  ScrollPane")
    initRect = pygame.Rect(screen.get_rect())
    sp = ScrollPane(world.get_size(), initRect, world, bg, [S, W, N])
    sp.draw(bg)
    screen.blit(bg,Origin)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type is pygame.QUIT: break       
        sp.update(event)
        sp.draw(bg)
        screen.blit(bg,Origin)
        pygame.display.flip()

    ###  EXAMPLE 2
    pygame.display.set_caption("Example 2:    ScrollBar")
    thick = 10
    scrollRect = pygame.Rect(0, 0, ScrSize[0], thick)
    excludes = ((0, thick), ScrSize)
    group = pygame.sprite.RenderPlain()    
    sb = ScrollBar(group, world.get_width(), scrollRect, bg, 0,
                   excludes, (170,220,180), (240,210,225))    
    sb.draw(bg)
    bg.blit(world, (0,thick),
            (sb.get_offsets(),(ScrSize[0],ScrSize[1]-thick)))   
    screen.blit(bg, Origin)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type is pygame.QUIT: break        
        sb.update(event)
        changes = sb.draw(bg)
        if len(changes) > 0:
            changes.append(bg.blit(world, (0,thick),
                          (sb.get_offsets(),(ScrSize[0],ScrSize[1]-thick))))
        screen.blit(bg,Origin)
        pygame.display.update(changes)


    pygame.quit()
    sys.exit(0)

if __name__ == '__main__':
    examples()
