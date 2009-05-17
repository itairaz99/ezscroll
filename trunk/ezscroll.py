#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *


FGCOLOR = 220,220,200
BGCOLOR = 235,235,230
N='N'
S='S'
E='E'
W='W'

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
        self.group = pygame.sprite.RenderUpdates()
        self.nsew = nsew
        self.thick = thick

        win = self.initViewRect(initRect, self.nsew, self.thick)
        self.sprites = []
        if E in self.nsew or W in self.nsew:
            scrollRect = pygame.Rect(0, win.top, initRect.width, win.height)
            exclude = win.inflate(0, self.thick).move(0,-self.thick/2)
            sb = ScrollBar(self.group, worldSize[1], scrollRect, self.pane, 1,
                           exclude, fgColor, bgColor)
            self.sprites.append(sb)
        if N in self.nsew or S in self.nsew:
            scrollRect = pygame.Rect(win.left, 0, win.width, initRect.height)
            exclude = win.inflate(self.thick, 0).move(-self.thick/2,0)
            sb = ScrollBar(self.group, worldSize[0], scrollRect, self.pane, 0,
                           exclude, fgColor, bgColor)
            self.sprites.append(sb)
        self.viewRect = win

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
        for sb in self.sprites:
            sb.update(event)
            if sb.scrolling:
                break
                
    def draw(self, surface):
        offsets = [0,0]
        for sb in self.sprites:
            offsets[sb.axis] = sb.get_offsets()[sb.axis]
            sb.draw(surface)
        # Comment out this blit to see just the scrollbars.    
        surface.blit(self.world, self.viewRect.topleft,
                     (offsets, self.viewRect.size))
        return self.pane.get_rect()

    def get_pane(self):
        """ Called by end user to get the scroll pane """
        return self.pane


class ScrollBar(pygame.sprite.DirtySprite):
    """ Same interface as sprite.Group.
    Get result of update() in pixels scrolled, from get_offsets()
    """

    def __init__(
        self,
        group,
        worldDim,
        initRect,
        surface=None,
        axis=0,
        exclude=(0,0,0,0),
        fgColor=FGCOLOR,
        bgColor=BGCOLOR):
        
        pygame.sprite.Sprite.__init__(self,group)
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
        self.scrolling = False
        self.leftTop = [0,0]
        self.diff = [0,0]
        self.diff[self.axis] = self.initTopleft[self.axis]
##        if self.drawAuto == True:
##            self.draw(self.surface) # todo 1 option for this 

    def update(self, event): # event must not be None
        
            if self.scrolling and event.type is MOUSEMOTION:
                rel = self.scroll(event.rel)
                if rel != 0:
                    self.leftTop[self.axis] += (rel / self.ratio)

            elif event.type is MOUSEBUTTONDOWN and (
                self.knob.move(self.diff).collidepoint(event.pos) and (
                    self.exclude and not (
                        self.exclude.collidepoint(event.pos)))):
                self.scrolling = True                

            elif event.type is MOUSEBUTTONUP:
                self.scrolling = False
        
    def scroll(self, rel):
        """ Moves knob based on [x,y] change like mouse event rel
        Called internally by update(). Knob travel limited to track.
        """
        if rel and rel[self.axis] != 0:
            axis = self.axis
            relax = rel[axis]
            rect = self.rect
            knob = self.knob
            knobMove = max(relax, rect.topleft[axis] - knob.topleft[axis])
            knobMove = min(knobMove, rect.bottomright[axis] - knob.bottomright[axis])
            if knobMove != 0:
                knobMoves = [0,0]
                knobMoves[axis] = knobMove
                self.knob.move_ip(knobMoves)
                return knobMove
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



if __name__ == '__main__':
    import examples
    examples.examples()