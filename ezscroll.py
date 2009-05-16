#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *

ScrSize = (300,600)
Origin  = (0,0)
Gray    = (200,200,200)
FGCOLOR = 220,220,200
BGCOLOR = 230,230,230
N='N'
S='S'
E='E'
W='W'

def examples():
    """ Two examples of how to use ezscroll.
        One is a scrollbar, the other is a scrollpane.
        The scrollpane handles some things like offsets better,
        puts the scrollbars in a sprite group, and blits the world.
        If you just want one scrollbar, still may be easier to
        use ScrollPane and pass [S] or [E], etc.
    """
    exampleOneRunning = True
    exampleTwoRunning = True    
    pygame.init()
    screen = pygame.display.set_mode(ScrSize)
    bg = pygame.Surface(ScrSize).convert()
    bg.fill(Gray)    
    world = pygame.Surface((ScrSize[0]*2, ScrSize[1]*2))
    world.fill(Gray)
    for x in xrange(100, world.get_size()[0], 200):
        for y in xrange(100, world.get_size()[1], 200):
            pygame.draw.circle(world, (225,34,43), (x,y), 100, 10)          

    ###  EXAMPLE 1
    pygame.display.set_caption("Example 1: ScrollBar")
    thick = 30
    scrollRect = pygame.Rect(0, 0, ScrSize[0], thick)
    excludes = ((0, thick), ScrSize) # limits start-scrolling area
    sb = ScrollBar(world.get_width(), scrollRect, bg, 0, excludes)    
    group = pygame.sprite.RenderPlain()
    group.add(sb)
    screen.blit(bg, Origin)
    pygame.display.flip()
    while exampleOneRunning:
        event = pygame.event.wait()
        if event.type is QUIT:
            exampleOneRunning = False        
        sb.update(event)
        sb.draw(bg)
        bg.blit(world, (0,thick),
            (sb.get_offsets(),(ScrSize[0],ScrSize[1]-thick)))
        screen.blit(bg,Origin)
        pygame.display.flip()

    ###  EXAMPLE 2
    pygame.display.set_caption("Example 2: ScrollPane")
    initRect = pygame.Rect(0 ,0,ScrSize[0],ScrSize[1])
    sp = ScrollPane(world.get_size(), initRect, world, bg, [S, E, W, N])
    sp.draw(bg)
    screen.blit(bg,Origin)
    pygame.display.flip()
    while exampleTwoRunning:
        event = pygame.event.wait()
        if event.type is QUIT:
            exampleTwoRunning = False        
        sp.update(event)
        sp.draw(bg)
        screen.blit(bg,Origin)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


class ScrollPane():
    """ Coordinates two ScrollBars """
    
    def __init__(
        self,
        worldSize,
        initRect,
        world,
        pane=None,
        nsew=[S,E],
        thick=20,
        fgColor=FGCOLOR,
        bgColor=BGCOLOR):

        self.world = world
        self.pane = pane
        self.group = pygame.sprite.RenderPlain()
        self.nsew = nsew
        self.thick = thick
        self.viewRect = win = self.initViewRect(initRect, self.nsew, self.thick)
        self.sbs = []
        if E in self.nsew or W in self.nsew:
            scrollRect = pygame.Rect(0, win.top, initRect.width, win.height)
            sb = ScrollBar(worldSize[1], scrollRect, self.pane, 1,
                win.inflate(0, self.thick).move(0,-self.thick/2), fgColor, bgColor)
            self.sbs.append(sb)
            self.group.add(sb)        
        if N in self.nsew or S in self.nsew:
            scrollRect = pygame.Rect(win.left, 0, win.width, initRect.height)
            sb = ScrollBar(worldSize[0], scrollRect, self.pane, 0,
                win.inflate(self.thick, 0).move(-self.thick/2,0), fgColor, bgColor)
            self.sbs.append(sb)
            self.group.add(sb)

    def initViewRect(self, initRect, nsew, thick):
        """ Subtract width of scrollbars from viewable area """
        win = pygame.Rect(initRect)
        if N in nsew:
            win.top = thick
            win.height -= thick            
        if S in nsew:
            win.height -= thick         
        if E in nsew:
            win.width -= thick
        if W in nsew:
            win.left = thick
            win.width -= thick               
        return win

    def clear(self, bg, archive):
        pass
        
    def update(self, event):
        for sb in self.sbs:
            sb.update(event)
            if sb.scrolling:
                break
                
    def draw(self, surface):
        offsets = [0,0]
        for sb in self.sbs:
            offsets[sb.axis] = sb.get_offsets()[sb.axis]
            sb.draw(surface)
        surface.blit(self.world, self.viewRect.topleft, (offsets, self.viewRect.size))
        return self.pane.get_rect()

    def get_pane(self):
        """ Called by end user to get the scroll pane """
        return self.pane


class ScrollBar(pygame.sprite.Sprite):
    """ Same interface as sprite.Group.
    Get result of update() in pixels scrolled, from get_offsets()
    """

    def __init__(
        self,
        worldDim,
        initRect,
        surface=None,
        axis=0,
        exclude=(0,0,0,0),
        fgColor=FGCOLOR,
        bgColor=BGCOLOR):
        
        pygame.sprite.Sprite.__init__(self)
        self.initTopleft = initRect.topleft
        self.exclude = pygame.Rect(exclude)
        self.image = pygame.Surface(initRect.size).convert()      
        self.rect = self.image.get_rect()
        self.surface = surface
        self.axis = axis
        self.fgColor = fgColor
        self.bgColor = bgColor        
        self.knob = pygame.Rect(self.rect)
        self.ratio = 1.0* initRect.size[self.axis] / worldDim
        knoblist = list(self.knob.size)
        knoblist[self.axis] = (self.knob.size[self.axis] * self.ratio)
        self.knob.size = knoblist
        self.draw(self.surface)
        self.scrolling = False
        self.leftTop = [0,0]
        self.diff = [0,0]
        self.diff[self.axis] = self.initTopleft[self.axis]

    def update(self, event):
        if event and event.type in [MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN]:

            if event.type is MOUSEMOTION and self.scrolling:
                step = self.scroll(event.rel)
                if step != 0:
                    self.leftTop[self.axis] += (step / self.ratio)

            elif event.type is MOUSEBUTTONDOWN:
                if self.knob.move(self.diff).collidepoint(event.pos) and (
                    self.exclude and not (
                        self.exclude.collidepoint(event.pos))):
                    self.scrolling = True                

            elif event.type is MOUSEBUTTONUP:
                self.scrolling = False
        
    def scroll(self, rel):
        """ Moves knob based on [x,y] change like mouse event rel
        Called internally by update()
        """
        if rel and rel[self.axis] != 0:
            axis = self.axis
            relax = rel[axis]
            rect = self.rect
            knob = self.knob
            # limit knob travel
            step = max(relax, rect.topleft[axis] - knob.topleft[axis])
            step = min(step, rect.bottomright[axis] - knob.bottomright[axis])
            if step != 0:
                steps = [0,0]
                steps[axis] = step
                self.knob.move_ip(steps)
                return step
        return 0      

    def draw(self, surface):
        """ Blits sprite image to a surface if it exists.
        Called by update()>updateViews() if self.auto is True.
        Also mimics group.draw, returning rectangle.
        """
        pygame.draw.rect(self.image, self.bgColor, self.rect, 0) 
        pygame.draw.rect(self.image, self.fgColor, self.knob, 0)
        
        if surface:
            return surface.blit(self.image, self.initTopleft)
        else:
            return None

    def get_offsets(self):
        """ Called by end user to get pixels scrolled,
        as result of update()

        """
        return self.leftTop



if __name__ == '__main__': examples()
