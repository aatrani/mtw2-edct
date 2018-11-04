import re
from reprlib import recursive_repr

incom_re = re.compile('[^;\.]*(;+.*)')
fulcom_re = re.compile('^\s*;.*')
whitel_re = re.compile('^\s*$')
trait_re = re.compile("^\s*Trait\s+(\S+)([ \t]*;?.*)") #re.compile("^\s*Trait\s+(\S+)")
trigg_re = re.compile("^\s*Trigger\s+(\S+)([ \t]*;?.*)")
    
class strlist(list):
    @recursive_repr()
    def __repr__(self):
        return "\n".join(map(repr, self))

    def update_names(self):
        self.names = [x.name for x in self]
        self.N = len(self.names)
        
    def __init__(self, *args):
        list.__init__(self, *args)
        self.names = []
        self.N = len(self.names)
