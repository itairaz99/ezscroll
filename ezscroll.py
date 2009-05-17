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
    """ Coordinates up to four scrollbars on a panel.
    Uses two ScrollBars offset, and blits world view on top.
    Use like a sprite group: update(), draw(). See examples.py
    """
    
    def __init__(
        self,
        worldSize,
        initRect,
        world,
        pane=None,
        nsew=[S,E],
        thick=20,
        drawAtUpdate=False,        
        fgColor=FGCOLOR,
        bgColor=BGCOLOR):
        """ Figures layout and inits ScrollBars """

        self.world = world
        self.pane = pane
        self.group = pygame.sprite.RenderUpdates()
        self.nsew = nsew
        self.thick = thick
        self.drawAtUpdate = drawAtUpdate

        win = self.initViewRect(initRect, self.nsew, self.thick)
        self.viewRect = win
        self.sprites = [] # the scrollbars
        if E in self.nsew or W in self.nsew:
            scrollRect = pygame.Rect(0, win.top, initRect.width, win.height)
            exclude = win.inflate(0, self.thick).move(0,-self.thick//2)
            sb = ScrollBar(self.group, worldSize[1], scrollRect, self.pane, 1,
                           exclude, fgColor, bgColor)
            self.sprites.append(sb)

        if N in self.nsew or S in self.nsew:
            scrollRect = pygame.Rect(win.left, 0, win.width, initRect.height)
            exclude = win.inflate(self.thick, 0).move(-self.thick//2,0)
            sb = ScrollBar(self.group, worldSize[0], scrollRect, self.pane, 0,
                           exclude, fgColor, bgColor)
            self.sprites.append(sb)

    def initViewRect(self, initRect, nsew, thick):
        """ Used by init(), subtract width of scrollbars from viewable area """
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
        pass # todo
        
    def update(self, event):
        """ Called by end user to update scroll state """
        for sb in self.sprites:
            sb.update(event)
        if self.drawAtUpdate:
            self.draw(self.pane)
                
    def draw(self, surface):
        """ Called by end user to draw state to the surface """
        offsets = [0,0]
        changes = []
        for sb in self.sprites:
            offsets[sb.axis] = sb.get_offsets()[sb.axis]
            changes.extend(sb.draw(surface))        
            # Comment out this blit to see just the scrollbars.    
        if changes:
            changes.append(surface.blit(self.world, self.viewRect.topleft,
                    (offsets, self.viewRect.size)))
            pygame.draw.rect(self.pane, BGCOLOR, self.viewRect.inflate(3,3).move(-1,-1), 3)
            
        return changes

    def get_pane(self):
        """ Called by end user to get the scroll pane results """
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
        self.dirty = True

    def update(self, event): # event must not be None
        """ Called by user with mouse events. event must not be none. """        
        if self.scrolling and event.type is MOUSEMOTION:
            relax = self.scroll(event.rel[self.axis])
            if relax != 0:
                self.leftTop[self.axis] += (relax / self.ratio)
                self.dirty = True
                
        elif event.type is MOUSEBUTTONDOWN and (
            self.knob.move(self.diff).collidepoint(event.pos) and (
                self.exclude and not (
                    self.exclude.collidepoint(event.pos)))):
            self.scrolling = True                

        elif event.type is MOUSEBUTTONUP:
            self.scrolling = False
        
    def scroll(self, relax):
        """ Moves knob based on mouse events rel change along axis.
        Called internally by update(). Knob travel limited to track.
        """
        if relax and relax != 0:
            axis = self.axis
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
        todo: Called by update()>updateViews() if self.auto is True.
        Also mimics group.draw, returning rectangle.
        """
        if self.dirty == True and surface is not None:
            self.dirty = False
            pygame.draw.rect(self.image, self.bgColor, self.rect, 0) 
            pygame.draw.rect(self.image, self.fgColor, self.knob, 0)            
            return [surface.blit(self.image, self.initTopleft)]
        else:
            return []

    def get_offsets(self):
        """ Called by end user to get pixels scrolled,
        as result of update()
        """
        return self.leftTop



if __name__ == '__main__':
    import examples
    examples.examples()
