#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.17
# In conjunction with Tcl version 8.6
#    Oct 07, 2018 08:48:37 PM JST  platform: Windows NT
#    Nov 15, 2018 12:24:43 PM JST  platform: Linux
#    Nov 15, 2018 02:35:51 PM JST  platform: Linux
#    Nov 15, 2018 02:59:24 PM JST  platform: Linux
#    Nov 21, 2018 11:25:53 PM JST  platform: Windows NT

import edctclass
from utils import strlist, remove_from_list
import os
import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from overrides import Resizer, Tooltip, menubar_highlight_linuxfix

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
    global TriggerList
    TriggerList = StringVar()
    global traitsearched
    traitsearched = StringVar()
    global triggersearched
    triggersearched = StringVar()
    global TraitCaseSens
    TraitCaseSens = IntVar()
    global TriggCaseSens
    TriggCaseSens = StringVar()


######################################################
###                 FILE MENU                      ###
######################################################

def OpenFile(filename=None):
    if(not filename):
        filename = askopenfilename(parent=root)
        if(not filename):
            print("ERROR: please choose a file")
            return
    if(not os.path.isfile(filename)):
        print("ERROR: file not found")
        return
    alcib.parse_edct(filename)
    TraitList.set(alcib.traits.names)
    TriggerList.set(alcib.triggers.names)
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
    destroy_window()
    sys.stdout.flush()

def ReloadFile():
    alcib.reload()
    TraitList.set(alcib.traits.names)
    TriggerList.set(alcib.triggers.names)
    ClearEdit()
    afterparse()
    sys.stdout.flush()

######################################################
###                  TRAIT BUTTONS                 ###
######################################################
    
def FindAllTraits():
    if(not tregex):
        return
    clist = w.TraitListt.get(0, END)
    match_ind = [i for i,name in enumerate(clist) if tregex.search(name)]

    w.TraitListt.selection_clear(0, END)
    for j in match_ind:
        w.TraitListt.selection_set(j)
    sys.stdout.flush()

def TraitGoToNext():
    if(not tregex):
        return
    current = w.TraitListt.index(ACTIVE)
    clist = w.TraitListt.get(0, END)
    match_ind = [i for i,name in enumerate(clist) if tregex.search(name)]
    cgreat = [i for i in match_ind if i>current]

    if(cgreat): mnext = cgreat[0]
    else: mnext = match_ind[0]
    
    w.TraitListt.selection_clear(0, END)
    
    w.TraitListt.see(mnext)
    w.TraitListt.activate(mnext)
    w.TraitListt.selection_set(mnext)
    #w.TraitListt.focus_set()
    sys.stdout.flush()

def TraitGoToPrev():
    if(not tregex):
        return
    current = w.TraitListt.index(ACTIVE)
    clist = w.TraitListt.get(0, END)
    match_ind = [i for i,name in enumerate(clist) if tregex.search(name)]
    csmall = [i for i in match_ind if i<current]

    if(csmall): mnext = csmall[-1]
    else: mnext = match_ind[-1]
    
    w.TraitListt.selection_clear(0, END)
    
    w.TraitListt.see(mnext)
    w.TraitListt.activate(mnext)
    w.TraitListt.selection_set(mnext)
    #w.TraitListt.focus_set()
    sys.stdout.flush()

def InvertTraitSelection():
    sel = w.TraitListt.curselection()
    w.TraitListt.selection_clear(0, END)
    i = 0
    for j in sel:
        if(i!=j):
            w.TraitListt.selection_set(i, j-1)
        i = j + 1
    w.TraitListt.selection_set(i, END)
    sys.stdout.flush()

def HideTrait():
    sel = w.TraitListt.curselection()
    clist = w.TraitListt.get(0, END)
    nlist = remove_from_list(clist, sel)
    TraitList.set(nlist)
    sys.stdout.flush()

def AddTrait(clear=False):
    sel = w.TraitListt.curselection()
    #print("selection:", sel)
    strat = [w.TraitListt.get(s) for s in sel]
    #print("traits:", strat)
    if(clear):
        # Clear Workspace
        ClearEdit()
    
    #alcib.current_view = strlist()    
    for tt in strat:
        seltrait = alcib.get_trait(tt)
        if(seltrait in alcib.current_view):
            print("WARN: Trait {:s} already present".format(seltrait.name))
            continue
        w.Viewer.insert(END, seltrait.as_string())
        alcib.current_view.append(seltrait)
        
    w.Viewer.edit_modified(False)
    w.Viewer.edit_reset()
    sys.stdout.flush()
    
def DeleteTrait():
    sel = w.TraitListt.curselection()
    strat = [w.TraitListt.get(s) for s in sel]
    if(len(sel)>1): ent = "traits"
    elif(len(sel)==1): ent = "trait"
    else: return
    tlist = ""
    for t in strat:
        tlist = tlist + t + "\n"
    
    delebol=messagebox.askokcancel("Delete the following {:s}?".format(ent), "{:s}".format(tlist), default=messagebox.CANCEL)

    if(delebol==False): return
    elif(delebol==True): pass

    for tt in strat:
        alcib.delete_trait(tt)

    ReloadTraitList()
    sys.stdout.flush()

def ReloadTraitList():
    TraitList.set(alcib.traits.names)
    sys.stdout.flush()

######################################################
###                TRIGGER BUTTONS                 ###
######################################################

def FindAllTriggers():
    print('traitedit_support.FindAllTriggers')
    sys.stdout.flush()

def TriggGoToNext():
    print('traitedit_support.TriggGoToNext')
    sys.stdout.flush()

def TriggGoToPrev():
    print('traitedit_support.TriggGoToPrev')
    sys.stdout.flush()    

def InvertTriggerSelection():
    print('traitedit_support.InvertTriggerSelection')
    sys.stdout.flush()

def HideTrigger():
    print('traitedit_support.HideTrigger')
    sys.stdout.flush()

def AddTrigger():
    print('traitedit_support.AddTrigger')
    sys.stdout.flush()

def DeleteTrigger():
    print('traitedit_support.DeleteTrigger')
    sys.stdout.flush()

def ReloadTriggerList():
    print('traitedit_support.ReloadTriggerList')
    sys.stdout.flush()

######################################################
###              WORKSPACE BUTTONS                 ###
######################################################
    
def ReloadEdit():
    print('traitedit_support.ReloadEdit')
    TResize = Resizer(w.TraitButtonFrame, w.TraitListt, root)
    TResize.wgrid_double()
    sys.stdout.flush()

def SaveEdit():
    print('traitedit_support.SaveEdit')
    sys.stdout.flush()

def ValidEdit():
    print('traitedit_support.ValidEdit')
    sys.stdout.flush()

def ClearEdit():
    #print('traitedit_support.ClearEdit')
    #print("was text modified?", w.Viewer.edit_modified())
    if(w.Viewer.edit_modified()):
        savebol=messagebox.askyesnocancel("Save workspace?", "Save changes before changing workspace?", default=messagebox.CANCEL)
        if(savebol==True): SaveEdit()
        elif(savebol==None): return
        elif(savebol==False): pass
        
    w.Viewer.delete('1.0', END)
    alcib.current_view = strlist()
    w.Viewer.edit_modified(False)
    w.Viewer.edit_reset()
    
    sys.stdout.flush()

def ExportEdit():
    print('traitedit_support.ExportEdit')
    ValidateBeforeExport=False
    if(ValidateBeforeExport):
        ValidEdit()
    filename = asksaveasfilename(parent=root)
    if(not filename):
        print("ERROR: please choose a file")
        return
    
    exptext = w.Viewer.get("1.0",END)
    
    outf = open(filename, "w")
    outf.write(exptext)
    outf.close()

    messagebox.showinfo("Workspace exported", "Current workspace successfully exported to\n{:s}".format(filename), parent=root)
    
    sys.stdout.flush()

def ImportEdit():
    print('traitedit_support.ImportEdit')
    sys.stdout.flush()

######################################################
###          INIT AND HELPER FUNCTIONS             ###
######################################################    

global alcib, tregex
alcib = edctclass.EDCT()
tregex = None

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    
    if sys.platform == "win32":
        w.style.theme_use('vista')
    w.TraitListt.bind('<Double-1>', lambda x: AddTrait(clear=True))
    w.TraitListt.config(selectmode=EXTENDED, activestyle=UNDERLINE)
    w.Viewer.config(undo=True)

    traitsearched.trace("w", reload_tregex)
    
    TTResize = Resizer(w.TraitButtonFrame, w.TraitListt, root)
    TTResize.resize_double_grid()
    EResize = Resizer(w.EditButtonFrame, w.Viewer, top)
    EResize.resize_single_grid()
    TGResize = Resizer(w.TriggerButtonFrame, w.TriggerListt, root)
    TGResize.resize_double_grid()
    
    w.TraitCaseSensitive.config(command=reload_tregex)

    ### Menu Button Highlight fix for linux
    if sys.platform.startswith("linux"):
        menubar_highlight_linuxfix(w.menubar)

    ### TOOLTIPS ###
    Tooltip(w.TraitCaseSensitive, text="Enables case sensitive search.")
    Tooltip(w.FindAllTrait, text="Selects all traits with matching pattern.")
    Tooltip(w.InvertTraitSelection, text="Invert the current selection.")
    Tooltip(w.HideTrait, text="Hides selected traits from the list.")
    Tooltip(w.ReloadTraitList, text="Reloads the trait list.")
    Tooltip(w.TraitSearchEntry, text="Text or regex pattern to search for.")
    Tooltip(w.TraitGoToPrev, text="Find previous.")
    Tooltip(w.TraitGoToNext, text="Find next.")
    Tooltip(w.AddTrait, text="Add selected trait to current workspace.")
    Tooltip(w.DeleteTrait, text="Delete selected traits.")
    
    ### OPEN IMMEDIATELY FOR TESTING ###
    filename = "export_descr_character_traits.txt"
    OpenFile(filename)
    root.focus_force() # fix for windows not taking focus of entry widget
    
def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

def afterparse():
    if(not (alcib.traits.N + alcib.triggers.N)):
        messagebox.showwarning("Parsing completed", "No triggers or traits found\n\n Please check your file\n({:s})".format(os.path.basename(alcib.edct_file)), parent=root)
    else:
        messagebox.showinfo("Parsing completed", "File: {:s}\nFound:\n  {:d} traits\n  {:d} triggers".format(os.path.basename(alcib.edct_file), alcib.traits.N, alcib.triggers.N), parent=root)

def reload_tregex(*args):
    global tregex
    to_find=traitsearched.get()
    if(not to_find):
        #print("WARN: Empty trait search string")
        tregex = None
        return
    if(TraitCaseSens.get()):
        tregex = re.compile(to_find)
    else:
        tregex = re.compile(to_find, re.IGNORECASE)
    #print(tregex)

if __name__ == '__main__':
    import traitedit
    traitedit.vp_start_gui()
































