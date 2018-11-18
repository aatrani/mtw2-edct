import tkinter as tk
import tkinter.ttk as ttk
from math import floor

######################################################
###    GUI overrides for traitedit_support.py      ###
###    Once things are done, might integrate by    ###
###    editing directly traitedit.py, but for now  ###
###    best override in cleanest way               ###
######################################################
######################################################

class Resizer() :
    def __init__(self, ButtonFrame, ListFrame, root):
        self.ButtFrame = ButtonFrame
        self.ListFrame = ListFrame
        self.root = root

    def resize(self):
        self.after = self.root.after(50, self.empty_after_resize)
        
    def empty_after_resize(self):
        self.root.after(50, self.resize_after)
        
    def resize_after(self):
        self.wfix()
        self.wgrid_single()
        self.root.after_cancel(self.after)

    def resize_and_grid(self):
        self.after = self.root.after(50, self.empty_after_grid)

    def empty_after_grid(self):
        self.root.after(50, self.grid_after)
        
    def grid_after(self):
        self.wfix()
        self.wgrid_double()
        self.root.after_cancel(self.after)
        
    def wfix(self):
        wx=self.ButtFrame.winfo_x()
        wy=self.ButtFrame.winfo_y()
        ww=self.ButtFrame.winfo_width()
        wh=self.ButtFrame.winfo_height()
        #print(wx, wy, wh, ww)
        self.ButtFrame.place_forget()
        self.ButtFrame.config(height=wh, borderwidth=1, relief="flat")
        self.ButtFrame.pack(side="top", fill="x") 
        #self.ButtFrame.pack_propagate(0)
    
        self.ListFrame.place_forget()
        self.ListFrame.pack(side="bottom", fill="both", expand=True) 

    def wgrid_double(self):
        ch=self.ButtFrame.winfo_children()
        for w in ch:
            w.place_forget()

        #print(ch[5].winfo_x())
        #print(ch[5].winfo_y())
        #print(ch[5].winfo_width())
        #print(ch[5].winfo_height())
        #print("frame:", self.ButtFrame.winfo_width())
        # top row
        ch[0].grid(row=0, column=0, columnspan=2, sticky="w") # find all
        ch[1].grid(row=0, column=2, columnspan=2, sticky="e") # check case
        ch[2].grid(row=0, column=30, columnspan=2) # invert
        ch[3].grid(row=0, column=50, sticky="we") # hide
        ch[4].grid(row=0, column=60, sticky="we") # reload

        #print(floor(self.ButtFrame.winfo_width()))
        #ch[5].grid_propagate(0)
        ch[5].configure(width = 32)
        #print(ch[5].winfo_width())
        
        # bottom row
        ch[5].grid(row=1, column=0, columnspan=4, sticky="we") # entry
        ch[6].grid(row=1, column=30) # previous
        ch[7].grid(row=1, column=31) # next
        ch[8].grid(row=1, column=50, sticky="we") # add
        ch[9].grid(row=1, column=60, sticky="we") # delete
 
        self.ButtFrame.columnconfigure(0, weight=3)
        self.ButtFrame.columnconfigure(2, weight=3)
        #self.ButtFrame.columnconfigure(2, weight=1)
        self.ButtFrame.columnconfigure(30, weight=5)
        self.ButtFrame.columnconfigure(31, weight=5)
        self.ButtFrame.columnconfigure(50, weight=4)
        self.ButtFrame.columnconfigure(60, weight=4)

    def wgrid_single(self):
        ch=self.ButtFrame.winfo_children()
        for w in ch:
            w.place_forget()

        for i, w in enumerate(ch):
            w.grid(row=0, column=i)
            self.ButtFrame.columnconfigure(i, weight=1)
 
class Tooltip():
    '''
    It creates a tooltip for a given widget as the mouse goes on it.

    see:

    http://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-
           in-tkinter/36221216#36221216

    http://www.daniweb.com/programming/software-development/
           code/484591/a-tooltip-class-for-tkinter

    - Originally written by vegaseat on 2014.09.09.

    - Modified to include a delay time by Victor Zaccardo on 2016.03.25.

    - Modified
        - to correct extreme right and extreme bottom behavior,
        - to stay inside the screen whenever the tooltip might go out on
          the top but still the screen is higher than the tooltip,
        - to use the more flexible mouse positioning,
        - to add customizable background color, padding, waittime and
          wraplength on creation
      by Alberto Vassena on 2016.11.05.

      Tested on Ubuntu 16.04/16.10, running Python 3.5.2

    TODO: themes styles support
    '''

    def __init__(self, widget,
                 *,
                 bg='#ffffcc',
                 pad=(5, 3, 5, 3),
                 text='widget info',
                 waittime=700,
                 wraplength=250):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label,
                               *,
                               tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = tk.Toplevel(widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=1,
                       relief=tk.SOLID)
        label = tk.Label(win,
                          text=self.text,
                          justify=tk.LEFT,
                          background=bg,
                          relief=tk.SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None
