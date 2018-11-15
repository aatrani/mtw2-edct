import os
from reprlib import recursive_repr
from utils import fulcom_re, incom_re, trait_re
from reprlib import recursive_repr
import re

class Trigger():
    def __init__(self, name, incom=None):
        self.name = name         
        self.when = None            # required
        self.conditions = []         
        self.affects = []    # required (only in edct), maximum 9
        
        self.comment_head = ""
        self.comment_dict = {}        
        if(incom): self.comment_dict["Trigger"] = incom
        self.commflag = "aTrigger"
       
    def parse_line(self, l):
        if(fulcom_re.match(l)):
            # add full lines to fulcom
            if((self.commflag == "aCondition") or (self.commflag == "aand")):
                # trigger condition comment
                self.conditions[-1].fullline_comment = self.conditions[-1].fullline_comment + l.replace("\t", "    ")
                return True
            elif(self.commflag == "aAffects"):
                # trigger affects comment
                self.affects[-1].fullline_comment = self.affects[-1].fullline_comment + l.replace("\t", "    ")
                return True
            else:
                # main trigger comment
                fcom = self.comment_dict.get(self.commflag, "")
                fcom = fcom + l.replace("\t", "    ")
                self.comment_dict[self.commflag] = fcom
                return True
        else:
            #if we are here it's not a full line comment
            # simplify in 3.8 with assignment expression
            incom_ma = incom_re.match(l) 
            if(incom_ma):
                incom = "    " + incom_ma.group(1) 
                l = re.sub(';.*', '', l)
            else:
                incom = None

        ltrigg = l.replace(",", "").split()
        if(ltrigg[0] == "WhenToTest"):
            self.when = ltrigg[1]
            if(incom): self.comment_dict["WhenToTest"] = incom

        elif(ltrigg[0] == "Condition"):
            newcond = TriggerCondition(" ".join(ltrigg[1:]), incom)
            self.conditions.append(newcond)
        elif(self.conditions and (ltrigg[0] == "and")):
            newcond = TriggerCondition(" ".join(ltrigg[1:]), incom)
            self.conditions.append(newcond)

        elif(ltrigg[0] == "Affects"):
            newaff = TriggerAffect(ltrigg[1], int(ltrigg[2]), int(ltrigg[4]), incom)
            self.affects.append(newaff)
        else:
            # if it's not any of those, return False
            if(not trait_re.match(l)):
                print("ERROR: can't parse line\n{:s}".format(l))
            return False
        # set full comment flag
        self.commflag = "a" + ltrigg[0]

        # if we are here we parsed successfully, return True
        return True

    @recursive_repr()
    def __repr__(self):
        base = "Trigger {:s}\n".format(self.name)
        base = base + "\tWhenToTest {:s}\n".format(self.when)
        if(self.conditions):
            base = base + "\t{:>9s} {:s}\n".format("Condition", self.conditions[0])
            if(self.conditions[1:]):
                for cond in self.conditions[1:]:
                    base = base + "\t{:>9s} {:s}\n".format("and", cond)
        base = base + "".join(map(repr, self.affects))
        return base
    
    def as_string(self):
        base = self.comment_head
        base = base + "Trigger {:s}".format(self.name) + self.comment_dict.get("Trigger", "")  + "\n"
        base = base + self.comment_dict.get("aTrigger", "")
        base = base + "  WhenToTest {:s}".format(self.when) + "\n\n"
        base = base + self.comment_dict.get("aWhenToTest", "")

        if(self.conditions):
            base = base + self.conditions[0].as_string(first=True)
            for cond in self.conditions[1:]:
                base = base + cond.as_string(first=False)
            base = base + "\n"
        for aff in self.affects:
            base = base + aff.as_string()
        return base + "\n"

class TriggerCondition():
    def __init__(self, cond, incom=None):
        self.cond = cond
        if(incom): self.inline_comment = incom
        else: self.inline_comment = ""
        self.fullline_comment = ""

    def __repr__(self):
        return "\tCondition {:s}".format("Condition", self.cond) + "\n"
    
    def as_string(self, first):
        if(first):
            base = "  {:>9s} {:s}".format("Condition", self.cond) + self.inline_comment + "\n"
        else:
            base = "  {:>9s} {:s}".format("and", self.cond) + self.inline_comment + "\n"
        base = base + self.fullline_comment 
        return base

    def evaluate(self, something):
        pass
        
class TriggerAffect():
    def __init__(self, aff, numb, chanc, incom=None):
        self.aff = aff
        self.val = int(numb)
        self.chance = int(chanc)
        if(incom): self.inline_comment = incom
        else: self.inline_comment = ""
        self.fullline_comment = ""

    def __repr__(self):
        return "\tAffects {:s} {:g} Chance {:g}\n".format(self.aff, self.val, self.chance)
    
    def as_string(self):
        base = "  Affects {:s}  {:d}  Chance  {:d}".format(self.aff, self.val, self.chance) + self.inline_comment + "\n"
        base = base + self.fullline_comment
        return base
        

