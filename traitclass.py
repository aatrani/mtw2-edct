import os
from reprlib import recursive_repr
from utils import strlist, fulcom_re, incom_re, trigg_re
from reprlib import recursive_repr
import re

class Trait():
    def __init__(self, name, incom=None):
        self.name = name            # required
        self.characters = []        # required
        self.hidden = False
        self.exclude = []
        self.nogoingback = None
        self.anti = []
        self.levels = strlist()     # required, min 1 max 9
        
        self.comment_dict = {}
        if(incom): self.comment_dict["Trait"] = incom
        self.commflag = "aTrait"
        
    def parse_line(self, l):
        if(fulcom_re.match(l)):
            # add full lines to fulcom
            if(self.levels):
                # trait level comment
                if((self.commflag == "aDescription") or (self.commflag == "aLevel") or
                   (self.commflag == "aEffectsDescription") or (self.commflag == "aGainMessage") or
                   (self.commflag == "aLoseMessage") or (self.commflag == "aEpithet") or (self.commflag == "aThreshold")):
                    fcom = self.levels[-1].comment_dict.get(self.commflag, "")
                    fcom = fcom + l.replace("\t", "    ")
                    self.levels[-1].comment_dict[self.commflag] = fcom
                    return True
                elif(self.commflag == "aEffect"):
                    # trait effect comment
                    self.levels[-1].effects[-1].fullline_comment = self.levels[-1].effects[-1].fullline_comment + l.replace("\t", "    ")
                    return True
            else:
                # main trait comment
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
        
        ltrait = l.replace(",", "").split() 
        toadd_inline = self
        if(ltrait[0] == "Characters"):
            for charac in ltrait[1:]:
                self.characters.append(charac) 
        elif(ltrait[0] == "ExcludeCultures"):
            for exclu in ltrait[1:]:
                self.exclude.append(exclu)
        elif(ltrait[0] == "AntiTraits"):
            for ant in ltrait[1:]:
                self.anti.append(ant)
        elif(ltrait[0] == "NoGoingBackLevel"):
            self.nogoingback = int(ltrait[1])
        elif(ltrait[0] == "Hidden"):
            self.hidden = True
            
        elif(ltrait[0] == "Level"):
            # Level gets appended to list. when finding level attributes, we look for the last level in the trait level list
            self.levels.append(TraitLevel(ltrait[1], incom))
                        
        elif(self.levels):
            toadd_inline = self.levels[-1]
            if(ltrait[0] == "Description"):
                self.levels[-1].description = ltrait[1]
            elif(ltrait[0] == "EffectsDescription"):
                self.levels[-1].effdecription = ltrait[1]
            elif(ltrait[0] == "GainMessage"):
                self.levels[-1].gainmessage = ltrait[1]
            elif(ltrait[0] == "LoseMessage"):
                self.levels[-1].losemessage = ltrait[1]
            elif(ltrait[0] == "Epithet"):
                self.levels[-1].epith = ltrait[1]
            elif(ltrait[0] == "Threshold"):
                self.levels[-1].threshold = int(ltrait[1])
            elif(ltrait[0] == "Effect"):
                neweff = TraitLevelEffect(ltrait[1], int(ltrait[2]), incom)
                self.levels[-1].effects.append(neweff)
            else:
                # if it's not any of those, return False
                if(not trigg_re.match(l)):
                    print("ERROR: can't parse line\n{:s}".format(l))
                return False
                
        # set inline comment
        if(incom):
            # Effect inline comments get stored in Effect object itself 
            if(ltrait[0] != "Effect"):
                toadd_inline.comment_dict[ltrait[0]] = incom
        # set full comment flag
        self.commflag = "a" + ltrait[0]

        # if we are here we parsed successfully, return True
        return True
        
    def validate_simple(self):
        pass
        
    @recursive_repr()
    def __repr__(self):
        base = "Trait {:s}\n".format(self.name)
        base = base + "\tCharacters "+" ".join(self.characters) + "\n"
        if(self.hidden):
            base = base + "\tHidden\n"
        if(self.exclude):
            base = base + "\tExclude "+" ".join(self.exclude) + "\n"
        base = base + "".join(map(repr, self.levels))
        return base
                    
    def as_string(self):
        base = "Trait {:s}".format(self.name) + self.comment_dict.get("Trait", "") + "\n"
        base = base + self.comment_dict.get("aTrait", "")
        base = base + "    Characters "+", ".join(self.characters) + self.comment_dict.get("Characters", "") + "\n"
        base = base + self.comment_dict.get("aCharacters", "")
        if(self.hidden):
            base = base + "    Hidden" + self.comment_dict.get("Hidden", "") + "\n"
            base = base + self.comment_dict.get("aHidden", "")
        if(self.exclude):
            base = base + "    ExcludeCultures "+", ".join(self.exclude) + self.comment_dict.get("ExcludeCultures", "") + "\n"
            base = base + self.comment_dict.get("aExcludeCultures", "")
        if(self.nogoingback):
            base = base + "    NoGoingBackLevel {:d}".format(self.nogoingback) + self.comment_dict.get("NoGoingBackLevel", "") + "\n"
            base = base + self.comment_dict.get("aNoGoingBackLevel", "")
        if(self.anti):
            base = base + "    AntiTraits "+", ".join(self.anti) + self.comment_dict.get("AntiTraits", "") + "\n"
            base = base + self.comment_dict.get("aAntiTraits", "")
        for lev in self.levels:
            base = base +"\n"+ lev.as_string()
        return base + "\n"
    
class TraitLevel():
    def __init__(self, name, incom=None):
        self.name = name
        self.description = None    # required, name must match
        self.effdecription = None  # required, name must match
        self.threshold = None      # required
        self.gainmessage = None
        self.losemessage = None
        self.epith = None
        self.effects = []

        self.comment_dict = {}
        if(incom): self.comment_dict["Level"] = incom
        self.commflag = "aTrigger"

    @recursive_repr()
    def __repr__(self):
        base = "\tLevel " + self.name + "\n"
        base = base + "\t\tThreshold {:g}\n".format(self.threshold)
        if(self.effects):
            base = base + "".join(map(repr, self.effects))
        return base
        
    def as_string(self):
        base = "    Level " + self.name + self.comment_dict.get("Level", "") + "\n"
        base = base + self.comment_dict.get("aLevel", "")
        base = base + "        Description " + self.description + self.comment_dict.get("Description", "") + "\n"  
        base = base + self.comment_dict.get("aDescription", "")
        base = base + "        EffectsDescription " + self.effdecription + self.comment_dict.get("EffectsDescription", "") + "\n"
        base = base + self.comment_dict.get("aEffectsDescription", "")
        if(self.gainmessage):
            base = base + "        GainMessage " + self.gainmessage + self.comment_dict.get("GainMessage", "") + "\n"
            base = base + self.comment_dict.get("aGainMessage", "")
        if(self.losemessage):
            base = base + "        LoseMessage " + self.losemessage + self.comment_dict.get("LoseMessage", "") + "\n"
            base = base + self.comment_dict.get("aLoseMessage", "")
        if(self.epith):
            base = base + "        Epithet " + self.epith + self.comment_dict.get("Epithet", "") + "\n"
            base = base + self.comment_dict.get("aEpithet", "")
        base = base + "        Threshold {:d}".format(self.threshold) + self.comment_dict.get("Threshold", "") + "\n"
        base = base + self.comment_dict.get("aThreshold", "")
        
        if(self.effects):
            base = base + "\n"
            for eff in self.effects:
                base = base + eff.as_string()
        return base
    
class TraitLevelEffect():
    def __init__(self, eff, numb, incom=None):
        self.eff = eff
        self.val = int(numb)
        if(incom): self.inline_comment = incom
        else: self.inline_comment = ""
        self.fullline_comment = ""
        
    def __repr__(self):
        return "\t\t{:s} {:g}\n".format(self.eff, self.val)
    
    def as_string(self):
        base = "        Effect  {:s} {:d}".format(self.eff, self.val) + self.inline_comment + "\n"
        base = base + self.fullline_comment
        return base

