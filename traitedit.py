#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.17
# In conjunction with Tcl version 8.6
#    Oct 28, 2018 08:18:05 PM JST  platform: Windows NT

import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import traitedit_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    traitedit_support.set_Tk_var()
    top = EDCT_Explore (root)
    traitedit_support.init(root, top)
    root.mainloop()

w = None
def create_EDCT_Explore(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    traitedit_support.set_Tk_var()
    top = EDCT_Explore (w)
    traitedit_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_EDCT_Explore():
    global w
    w.destroy()
    w = None


class EDCT_Explore:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font10 = "-family {Courier New} -size 10 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"
        font9 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1150x629+323+347")
        top.title("EDCT Explore")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")



        self.PaneWin = ttk.Panedwindow(top, orient="horizontal")
        self.PaneWin.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.TraitPane = ttk.Labelframe(width=338, text='Traits')
        self.PaneWin.add(self.TraitPane)
        self.EditPane = ttk.Labelframe(width=455, text='Workspace')
        self.PaneWin.add(self.EditPane)
        self.TriggerPane = ttk.Labelframe(text='Triggers')
        self.PaneWin.add(self.TriggerPane)
        self.__funcid0 = self.PaneWin.bind('<Map>', self.__adjust_sash0)

        self.TraitListt = ScrolledListBox(self.TraitPane)
        self.TraitListt.place(relx=0.0, rely=0.127, relheight=0.959
                , relwidth=0.988, bordermode='ignore')
        self.TraitListt.configure(background="white")
        self.TraitListt.configure(disabledforeground="#a3a3a3")
        self.TraitListt.configure(font=font10)
        self.TraitListt.configure(foreground="black")
        self.TraitListt.configure(highlightbackground="#d9d9d9")
        self.TraitListt.configure(highlightcolor="#d9d9d9")
        self.TraitListt.configure(selectbackground="#c4c4c4")
        self.TraitListt.configure(selectforeground="black")
        self.TraitListt.configure(width=10)
        self.TraitListt.configure(listvariable=traitedit_support.TraitList)

        self.TriggerEntry = ttk.Entry(self.TraitPane)
        self.TriggerEntry.place(relx=0.015, rely=0.079, relheight=0.041
                , relwidth=0.479, bordermode='ignore')
        self.TriggerEntry.configure(textvariable=traitedit_support.traitsearched)
        self.TriggerEntry.configure(takefocus="")
        self.TriggerEntry.configure(cursor="xterm")

        self.TraitGoToPrev = ttk.Button(self.TraitPane)
        self.TraitGoToPrev.place(relx=0.503, rely=0.079, height=26, width=23
                , bordermode='ignore')
        self.TraitGoToPrev.configure(takefocus="")
        self.TraitGoToPrev.configure(text='''<''')

        self.TraitGoToNext = ttk.Button(self.TraitPane)
        self.TraitGoToNext.place(relx=0.577, rely=0.079, height=26, width=23
                , bordermode='ignore')
        self.TraitGoToNext.configure(takefocus="")
        self.TraitGoToNext.configure(text='''>''')

        self.AddTrait = ttk.Button(self.TraitPane)
        self.AddTrait.place(relx=0.651, rely=0.079, height=26, width=48
                , bordermode='ignore')
        self.AddTrait.configure(command=traitedit_support.AddTrait)
        self.AddTrait.configure(takefocus="")
        self.AddTrait.configure(text='''Add''')
        self.AddTrait.configure(width=48)

        self.HideTrait = ttk.Button(self.TraitPane)
        self.HideTrait.place(relx=0.799, rely=0.079, height=26, width=58
                , bordermode='ignore')
        self.HideTrait.configure(command=traitedit_support.HideTrait)
        self.HideTrait.configure(takefocus="")
        self.HideTrait.configure(text='''Hide''')
        self.HideTrait.configure(width=58)

        self.FindAllTrait = ttk.Button(self.TraitPane)
        self.FindAllTrait.place(relx=0.015, rely=0.032, height=26, width=68
                , bordermode='ignore')
        self.FindAllTrait.configure(command=traitedit_support.FindAllTraits)
        self.FindAllTrait.configure(takefocus="")
        self.FindAllTrait.configure(text='''Find all''')
        self.FindAllTrait.configure(width=68)

        self.ReloadTraitList = ttk.Button(self.TraitPane)
        self.ReloadTraitList.place(relx=0.769, rely=0.032, height=26, width=68
                , bordermode='ignore')
        self.ReloadTraitList.configure(command=traitedit_support.ReloadTraitList)
        self.ReloadTraitList.configure(takefocus="")
        self.ReloadTraitList.configure(text='''Reload''')

        self.SaveEdit = ttk.Button(self.EditPane)
        self.SaveEdit.place(relx=0.198, rely=0.032, height=30, width=68
                , bordermode='ignore')
        self.SaveEdit.configure(command=traitedit_support.SaveEdit)
        self.SaveEdit.configure(takefocus="")
        self.SaveEdit.configure(text='''Save''')

        self.ValidEdit = ttk.Button(self.EditPane)
        self.ValidEdit.place(relx=0.022, rely=0.032, height=30, width=78
                , bordermode='ignore')
        self.ValidEdit.configure(command=traitedit_support.ValidEdit)
        self.ValidEdit.configure(takefocus="")
        self.ValidEdit.configure(text='''Validate''')
        self.ValidEdit.configure(width=78)

        self.ReloadEdit = ttk.Button(self.EditPane)
        self.ReloadEdit.place(relx=0.352, rely=0.032, height=30, width=78
                , bordermode='ignore')
        self.ReloadEdit.configure(command=traitedit_support.ReloadEdit)
        self.ReloadEdit.configure(takefocus="")
        self.ReloadEdit.configure(text='''Reload''')

        self.Viewer = ScrolledText(self.EditPane)
        self.Viewer.place(relx=0.0, rely=0.127, relheight=0.959, relwidth=1.0
                , bordermode='ignore')
        self.Viewer.configure(background="white")
        self.Viewer.configure(font=font9)
        self.Viewer.configure(foreground="black")
        self.Viewer.configure(highlightbackground="#d9d9d9")
        self.Viewer.configure(highlightcolor="black")
        self.Viewer.configure(insertbackground="black")
        self.Viewer.configure(insertborderwidth="3")
        self.Viewer.configure(selectbackground="#c4c4c4")
        self.Viewer.configure(selectforeground="black")
        self.Viewer.configure(width=10)
        self.Viewer.configure(wrap=NONE)

        self.TriggerListt = ScrolledListBox(self.TriggerPane)
        self.TriggerListt.place(relx=0.0, rely=0.127, relheight=0.959
                , relwidth=0.994, bordermode='ignore')
        self.TriggerListt.configure(background="white")
        self.TriggerListt.configure(disabledforeground="#a3a3a3")
        self.TriggerListt.configure(font=font10)
        self.TriggerListt.configure(foreground="black")
        self.TriggerListt.configure(highlightbackground="#d9d9d9")
        self.TriggerListt.configure(highlightcolor="#d9d9d9")
        self.TriggerListt.configure(selectbackground="#c4c4c4")
        self.TriggerListt.configure(selectforeground="black")
        self.TriggerListt.configure(width=10)
        self.TriggerListt.configure(listvariable=traitedit_support.TriggerList)

        self.TEntry2 = ttk.Entry(self.TriggerPane)
        self.TEntry2.place(relx=0.029, rely=0.064, relheight=0.041
                , relwidth=0.536, bordermode='ignore')
        self.TEntry2.configure(textvariable=traitedit_support.triggersearched)
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="xterm")

        self.TButton2 = ttk.Button(self.TriggerPane)
        self.TButton2.place(relx=0.634, rely=0.064, height=30, width=38
                , bordermode='ignore')
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Tbutton''')

        self.TButton3 = ttk.Button(self.TriggerPane)
        self.TButton3.place(relx=0.778, rely=0.064, height=30, width=38
                , bordermode='ignore')
        self.TButton3.configure(takefocus="")
        self.TButton3.configure(text='''Tbutton''')

        self.menubar = Menu(top,font=font9,bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.OpenFile,
                font="TkTextFont",
                foreground="#000000",
                label="Open")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.ReloadFile,
                font="TkTextFont",
                foreground="#000000",
                label="Reload")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.SaveFile,
                compound="left",
                font=font9,
                foreground="#000000",
                label="Save")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.SaveFileAs,
                font="TkTextFont",
                foreground="#000000",
                label="Save as")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.FilterWin,
                compound="left",
                font=font9,
                foreground="#000000",
                label="Filters")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.ValidateFile,
                font="TkTextFont",
                foreground="#000000",
                label="Validate")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=traitedit_support.Quit,
                font="TkTextFont",
                foreground="#000000",
                label="Quit")




    def __adjust_sash0(self, event):
        paned = event.widget
        pos = [338, 798, ]
        i = 0
        for sash in pos:
            paned.sashpos(i, sash)
            i += 1
        paned.unbind('<map>', self.__funcid0)
        del self.__funcid0




# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

if __name__ == '__main__':
    vp_start_gui()



