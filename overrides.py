import tkinter as tk
import tkinter.ttk as ttk

######################################################
###    GUI overrides for traitedit_support.py      ###
###    Once things are done, might integrate by    ###
###    editing directly traitedit.py, but for now  ###
###    best override in cleanest way               ###
######################################################
######################################################

class Resizer():
    def __init__(self, ButtonFrame, ListFrame, root):
        self.ButtFrame = ButtonFrame
        self.ListFrame = ListFrame
        self.root = root

    def resize(self):
        self.after = self.root.after(10, self.empty_after)

    def empty_after(self):
        self.root.after(10, self.resize_after)
        
    def resize_after(self):
        self.wfix()
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
        self.ButtFrame.pack_propagate(0)
    
        self.ListFrame.place_forget()
        self.ListFrame.pack(side="bottom", fill="both", expand=True) 

