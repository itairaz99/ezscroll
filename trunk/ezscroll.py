#! %PYTHONPATH%\python

import pygame.display
import pygame.draw
from pygame import Rect, Surface
from pygame.locals import MOUSEBUTTONUP, MOUSEMOTION, MOUSEBUTTONDOWN

LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1
BOTH = 2
NEITHER = -1

class EZScroll(object):

    """ A tightly bound set of scrolls.

    world       --  Surface, too-large view requires scrolling
    winRect     --  Rect,    porthole limits the view 
    scrollThick --  int,     thickness of scrollbars
    horzSBs     --  int,     TOP, BOTTOM, NEITHER, or BOTH bars
    vertSBs     --  int,     LEFT, RIGHT, NEITHER, or BOTH bars
    initPos     --  tuple,   initial scrollbar position
    pad         --  int,     bg space around knobs, default 0
    pretty      --  bool,    draw knobs with drop shadow, highlight
    fgBgColors  --  tuples,  scrollbar knob and track colors.
    hiLoColors  --  tuples,  highlight and drop shadow colors
    retSurface  --  Surface, user can provide their own pane 
    
    Draws scrollbars and scrolled view onto a pane.
    After init, get ezScroll.scrollPane and blit it.
    In event handling code, call handleEvent(e) with mouse events.
    Blit again. Voila.  Check out ezexample.py

    """

    FgColor = (200,200,200)
    BgColor = (225, 225, 225)
    HiColor = (255,255,255)
    LoColor = (40,40,40)
    FgBgColors = (FgColor, BgColor)
    HiLoColors = (HiColor, LoColor)

    def __init__(
        self,
        world,
        winRect,
        scrollThick,
        horzSBs,
        vertSBs,
        initPos=(0,0),
        pad=0,
        pretty=False,                 
        fgBgColors=FgBgColors,
        hiLoColors=HiLoColors,
        retSurface=None
        ):

        self.world      = world
        self.winRect    = winRect
        self.thick      = scrollThick
        self.leftTop    = list(initPos)
        self.pad        = pad    
        self.axes       = [0,1]
        self.tracks     = [None, None]
        self.knobs      = [None, None]
        self.ratios     = [0.0, 0.0]
        self.offsets    = [0,0]
        self.windowSize = list(winRect.size)     
        self.scrolling  = [False, False]
        self.active     = 0

        if fgBgColors and fgBgColors[0]: self.FgColor = fgBgColors[0] 
        if fgBgColors and fgBgColors[1]: self.BgColor = fgBgColors[1]
        if hiLoColors and hiLoColors[0]: self.HiColor = hiLoColors[0]
        if hiLoColors and hiLoColors[1]: self.LoColor = hiLoColors[1]
            
        self.scrollPane = retSurface
        if retSurface is None:
            self.scrollPane = pygame.Surface(self.winRect.size).convert()
        self.scrollPane.fill(self.BgColor)
        worldSize = self.world.get_size()

        # Figure out which scrollbars and the space to leave
        numHorzSBs, numVertSBs = 0, 0
        if horzSBs == BOTH: numHorzSBs = 2
        elif horzSBs > -1:  numHorzSBs = 1
        if vertSBs == BOTH: numVertSBs = 2
        elif vertSBs > -1:  numVertSBs = 1
        
        removes = [numVertSBs * self.thick, numHorzSBs * self.thick]
        tooMuchSpaceH = self.winRect.size[0] - removes[0] > worldSize[0]
        tooMuchSpaceV = self.winRect.size[1] - removes[1] > worldSize[1]
        if not tooMuchSpaceH and (numHorzSBs == BOTH or horzSBs == TOP):
            self.offsets[1] = self.thick
        if not tooMuchSpaceV and (numVertSBs == BOTH or vertSBs == LEFT):
            self.offsets[0] = self.thick
        if tooMuchSpaceV or numVertSBs == 0: del self.axes[1]
        if tooMuchSpaceH or numHorzSBs == 0: del self.axes[0]        
        self.viewRect = pygame.Rect(
            self.offsets[0],
            self.offsets[1],
            (self.winRect.size[0] - removes[0]),
            (self.winRect.size[1] - removes[1]))
        
        # reassign some methods, depending
        if not self.axes: self.handleEvent = self.noHandleEvents
        if pretty: self.draw = self.drawPretty

        # make each scoll bar and draw initial view
        for ax in self.axes:
            if self.viewRect.size[ax] < worldSize[ax]:

                leftOrTop = [self.winRect.left, self.winRect.top]
                leftOrTop[ax] = self.offsets[ax]
                wideOrHigh = [self.winRect.width, self.winRect.height]
                wideOrHigh[ax] -= removes[ax]   
                self.windowSize[ax] -= removes[ax]
                self.tracks[ax] = pygame.Rect((leftOrTop, wideOrHigh))
                self.knobs[ax] = pygame.Rect(self.tracks[ax])
                self.ratios[ax] = 1.0* self.tracks[ax].size[ax] / worldSize[ax]
                barSizeList = list(self.knobs[ax].size)
                barSizeList[ax] = self.knobs[ax].size[ax] * self.ratios[ax]
                self.knobs[ax].size = barSizeList
                initKnobPosList = [0,0]
                initKnobPosList[ax] = (
                    (self.leftTop[ax] * self.ratios[ax]) + self.offsets[ax] )
                self.knobs[ax].topleft = initKnobPosList
                self.draw(ax)

        self.scrollPane.blit(
        self.world,
        self.offsets,
        (self.leftTop[0],
         self.leftTop[1],
         self.viewRect.width,
         self.viewRect.height))
      

    #skip handling events at all if there are no scrollbars in self.axes
    def noHandleEvents(self, e):  return False, None

    def handleEvent(self, e):
        
        """ Called by user code in their event handling of mouse actions.

        Polls the different axis scrollbars for scroll values,
        then draws the scrollbars, and the scrolled view onto the scrollPane.
        See def example() below.

        """
        if e.type in [ MOUSEMOTION, MOUSEBUTTONDOWN ]:
            
            for ax in self.axes:
                knob = self.knobs[ax]
                track = self.tracks[ax]
                
                hitOrUsing = (
                    knob.collidepoint(e.pos) or
                    (True in self.scrolling and ax == self.active))

                # scrolling happens here
                if e.type == MOUSEMOTION and self.scrolling[ax] and hitOrUsing:

                    if e.rel[ax] != 0:
                        
                        move = e.rel[ax]
                        move = max(move, track.topleft[ax] - knob.topleft[ax])
                        move = min(move, track.bottomright[ax] - knob.bottomright[ax])

                        if move != 0:
                            moves = [0,0]
                            moves[ax] = move        
                            knob.move_ip(moves)                       

                            pygame.draw.rect(self.scrollPane, self.BgColor, self.tracks[ax], 0)

                            self.leftTop[ax] = (
                                ((knob.center[ax] -
                                knob.size[ax]/2) -
                                self.offsets[ax]) / self.ratios[ax])
                            self.draw(ax)
                        

                elif e.type == MOUSEBUTTONDOWN and \
                    knob.collidepoint(e.pos) and not \
                    self.viewRect.collidepoint(e.pos):

                    self.scrolling[ax] = True
                    self.active = ax
                   
        elif e.type == MOUSEBUTTONUP:

            self.scrolling[self.active] = False        

        self.scrollPane.blit(
        self.world,
        self.offsets,
        (self.leftTop[0],
         self.leftTop[1],
         self.viewRect.width,
         self.viewRect.height))

        # return scrolling, e.pos plus scrolled minus offsets
        try:
            return (
                self.scrolling[self.active],
                (e.pos[0]+ self.leftTop[0] - self.offsets[0],
                 e.pos[1]+ self.leftTop[1] - self.offsets[1]) )

        except AttributeError: # was sent an event with no pos
            return False, None

    def draw(self, ax):

        """ Called internally. Draws flat bars if pretty is False.

        This drawing method only requires the rendering of 3 rects.
        One for each knob, and one that goes around the view rect
        which is drawn in the track color to trim them away.
        Comment out the blit of world here to see exactly.

        """

        #draw the knob
        pygame.draw.rect(
            self.scrollPane,
            self.FgColor,
            (self.knobs[ax].left + self.pad,
             self.knobs[ax].top + self.pad,
             self.knobs[ax].width - 2*self.pad,
             self.knobs[ax].height - 2*self.pad),
            0)

        # Draw a rect around viewRect that trims the scrollbars away from view.
        pygame.draw.rect(
            self.scrollPane,
            self.BgColor,
            self.viewRect,
            2 * self.pad + 1)

            
    def drawPretty(self, ax):

        """ Used internally. Draws drop-shadowed knob if not pretty.

        This drawing method requires the rendering of 6 rects.
        Three for each knob end, overlapping HiColor, LoColor, FgColor
        Both are drawn regardless if hidden.
        Comment out the blit of world here to see exactly.

        """
        oppAxis = cmp(0,ax)+1
        knob = self.knobs[ax]
        size = [knob.width - (self.pad *2), knob.height - (self.pad * 2)]
        size[oppAxis] = self.thick - (2*self.pad)
        hiRect = pygame.Rect((knob.left + self.pad, knob.top + self.pad), size)
        loRect = hiRect.inflate(-1,-1).move(1,1)
        fgRect = loRect.inflate(-1,-1)
        rectAggr = ( (self.HiColor, hiRect, 1),
                     (self.LoColor, loRect, 1),
                     (self.FgColor, fgRect, 0) )

        self.drawRectAggr(rectAggr)
        moves = [0,0]
        moves[oppAxis] = knob.size[oppAxis] - size[oppAxis] - (2*self.pad)
        self.moveRectAggr(rectAggr, moves)
        self.drawRectAggr(rectAggr)
           
        
    def moveRectAggr(self, aggregate, moves):
        for item in aggregate:
            item[1].move_ip(moves)

    def drawRectAggr(self, aggregate):
        for item in aggregate:
            pygame.draw.rect(self.scrollPane,item[0],item[1], item[2])
