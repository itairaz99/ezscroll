### **ezscroll** makes it super easy to add scrollbars to your pygame Surfaces. ###

Now completely overhauled, using sprites and with decoupled update() and draw(), like sprite groups. Better code, easier to understand and change.  If you hated it before, you may love it now!

[ezscroll.py](http://code.google.com/p/ezscroll/source/browse/trunk/ezscroll.py) contains two classes: `ScrollBar` and `ScrollPane`. `ScrollPane` coordinates multiple scrollbars, adds them to a sprite group, and blits the moving world at update(), etc. Scrollbars are specified by cardinal direction, N, S, E, W.

The examples are now in [examples.py](http://code.google.com/p/ezscroll/source/browse/trunk/examples.py)
They run one after another by closing the window.

There is also a separate example of basic scrollbar code inline, without using ezscroll. About 18 lines for the scrollbar part. That file is called [inlineScroll.py](http://code.google.com/p/ezscroll/source/browse/trunk/inlineScroll.py)

v.09 fixed some bugs, download cheese from downloads today!

Thinking of making a version without some of the options, to focus on the basics and provide a cleaner starting point for others to modify.