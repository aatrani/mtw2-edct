#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.17
# In conjunction with Tcl version 8.6
#    Oct 07, 2018 08:48:37 PM JST  platform: Windows NT
#    Oct 07, 2018 11:29:04 PM JST  platform: Windows NT
#    Oct 07, 2018 11:52:37 PM JST  platform: Windows NT
#    Oct 08, 2018 10:34:34 PM JST  platform: Windows NT
#    Oct 11, 2018 10:55:51 PM JST  platform: Linux
#    Oct 28, 2018 07:42:28 PM JST  platform: Windows NT

import traitclass
import os
import sys
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

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
    
def set_Tk_var():
    global TraitList
    TraitList = StringVar()
    global traitsearched
    traitsearched = StringVar()
    global triggersearched
    triggersearched = StringVar()
    global TriggerList
    TriggerList = StringVar()

def OpenFile():
    print('traitedit_support.OpenFile')
    filename = askopenfilename()
    if(not filename):
        print("ERROR: please choose a file")
        return
    if(not os.path.isfile(filename)):
        print("ERROR: file not found")
        return
    traitmod.parse_edct(filename)
    TraitList.set(traitmod.traits.names)
    TriggerList.set(traitmod.triggers.names)
    w.Viewer.delete('1.0', END)
    afterparse()
    sys.stdout.flush()

def SaveFile():
    print('traitedit_support.SaveFile')
    sys.stdout.flush()

def SaveFileAs():
    print('traitedit_support.SaveFileAs')
    sys.stdout.flush()

def FilterWin():
    print('traitedit_support.FilterWin')
    sys.stdout.flush()

def ValidateFile():
    print('traitedit_support.ValidateFile')
    sys.stdout.flush()

def Quit():
    print('traitedit_support.Quit')
    sys.stdout.flush()
    destroy_window()

def ReloadFile():
    print('traitedit_support.ReloadFile')
    traitmod.reload()
    TraitList.set(traitmod.traits.names)
    TriggerList.set(traitmod.triggers.names)
    w.Viewer.delete('1.0', END)
    afterparse()
    sys.stdout.flush()

def AddTrait():
    print('traitedit_support.AddTrait')
    sys.stdout.flush()

def FindAllTraits():
    print('traitedit_support.FindAllTraits')
    sys.stdout.flush()

def HideTrait():
    print('traitedit_support.HideTrait')
    sys.stdout.flush()

def ReloadTraitList():
    print('traitedit_support.ReloadTraitList')
    sys.stdout.flush()

def ReloadEdit():
    print('traitedit_support.ReloadEdit')
    #print(w.style.theme_names())
    #print(w.style.theme_use())
    #w.style.theme_use('clam')
    sys.stdout.flush()

def SaveEdit():
    print('traitedit_support.SaveEdit')
    sys.stdout.flush()

def ValidEdit():
    print('traitedit_support.ValidEdit')
    sys.stdout.flush()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    
    if sys.platform == "win32":
        w.style.theme_use('vista')
    w.TraitListt.bind('<Double-1>', lambda x: select_trait())
    w.TraitListt.config(selectmode=EXTENDED)
    w.Viewer.config(undo=True)

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

global traitmod
traitmod = traitclass.EDCT()

def select_trait():
    sel = w.TraitListt.curselection()
    print("sel:", sel)
    trat = w.TraitListt.get(sel)
    print("trait:", trat)
    if(traitmod.current_view):
        # Viewer
        print("was text modified?", w.Viewer.edit_modified())
        if(w.Viewer.edit_modified()):
            savebol=messagebox.askyesnocancel("Save workspace?", "Save changes before changing workspace?", default=messagebox.CANCEL)
            if(savebol==True): save_view()
            elif(savebol==False): pass
            else: return
        w.Viewer.delete('1.0', END)
    seltrait = traitmod.get_trait(trat)
    w.Viewer.insert(INSERT, seltrait.as_string())
    traitmod.current_view = seltrait.name
    w.Viewer.edit_modified(False)
    w.Viewer.edit_reset()

def add_trait():
    sel = w.TraitListt.curselection()
    print("sel:", sel)
    trat = w.TraitListt.get(sel)
    print("trait:", trat)
    if(traitmod.current_view):
        # Viewer
        print("was text modified?", w.Viewer.edit_modified())
        w.Viewer.delete('1.0', END)
    seltrait = traitmod.get_trait(trat)
    w.Viewer.insert(INSERT, seltrait.as_string())
    traitmod.current_view = seltrait.name
    w.Viewer.edit_modified(False)
    w.Viewer.edit_reset()

def save_view():
    print('saving view')
    sys.stdout.flush()
    
def changeview():
    messagebox.askyesnocancel("Save workspace?", "Save changes before changing workspace?", default=messagebox.CANCEL)
    
def afterparse():
    if(not (traitmod.traits.N + traitmod.triggers.N)):
        messagebox.showwarning("Parsing completed", "No triggers or traits found\n\n Please check your file\n({:s})".format(os.path.basename(traitmod.edct_file)))
    else:
        messagebox.showinfo("Parsing completed", "File: {:s}\nFound:\n  {:d} traits\n  {:d} triggers".format(os.path.basename(traitmod.edct_file), traitmod.traits.N, traitmod.triggers.N))
    

if __name__ == '__main__':
    import traitedit
    traitedit.vp_start_gui()

















