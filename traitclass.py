import re
import os
from reprlib import recursive_repr

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
        
class EDCT():
    EDCT_fname = "export_descr_character_traits.txt"

    comment_re = re.compile("^\s*;|^\s*$")
    incom_re = re.compile('[^;\.]*(;+.*)')
    fulcom_re = re.compile('^\s*;.*')
    whitel_re = re.compile('^\s*$')

    trait_re = re.compile("^\s*Trait\s+(\S+)([ \t]*;?.*)") #re.compile("^\s*Trait\s+(\S+)")
    trigg_re = re.compile("^\s*Trigger\s+(\S+)([ \t]*;?.*)")    
    
    def __init__(self):
        self.Nwhite = 0
        self.Ntriggers = 0
        self.Ntraits = 0
        self.Nfulcom = 0
        self.Ntot = 0
        self.traits = strlist()
        self.triggers = strlist()
        self.current_view = None
        self.edct_file = None
        self.comment_header = ""
        
    @recursive_repr()
    def __repr__(self):
        return "Traits: {:g} \n".format(self.Ntraits) + "\n".join(map(repr, self.traits)) + "Triggers: {:g} \n".format(self.Ntriggers) + "\n".join(map(repr, self.triggers))
    
    def update_names(self):
        self.traits.update_names()
        self.triggers.update_names()
        
    def parse_edct(self, folder):
        self.__init__()
        
        self.edct_file = folder
        edct = open(folder, "r",   encoding="utf8")
        parseTrait = False
        parseTrigg = False

        for l in edct:
            self.Ntot+=1
            if(self.fulcom_re.match(l)):
                self.Nfulcom+=1
            if(self.whitel_re.match(l)):
                # skip whitelines
                self.Nwhite+=1
                continue

            if((not parseTrait) and (not parseTrigg)):
                if(self.fulcom_re.match(l)):
                    # add full lines to fulcom
                    self.comment_header = self.comment_header + l
                    continue
            
            trait_ma = EDCT.trait_re.match(l)
            
            if(trait_ma):
                parseTrait = True
                parseTrigg = False
                self.Ntraits+=1
                newtrait = Trait(trait_ma.group(1), trait_ma.group(2))
                self.traits.append(newtrait)
                continue
                
            if(parseTrait):
                parsed = newtrait.parse_line(l)
                if(parsed): continue
            
            trigg_ma = EDCT.trigg_re.match(l)
            if(trigg_ma):
                parseTrait = False
                parseTrigg = True
                self.Ntriggers+=1
                #if(self.Ntriggers >1): print(newtrigg)
                newtrigg = Trigger(trigg_ma.group(1), trigg_ma.group(2))
                self.triggers.append(newtrigg)
                continue
                
            if(parseTrigg):
                newtrigg.parse_line(l)
                continue

            # if we are here, something is wrong
            print("ERROR: can't parse line\n{:s}".format(l))
                
        
        self.update_names()
        print("-- Total lines {:d}".format(self.Ntot))
        print("-- White lines skipped: {:d}".format(self.Nwhite))
        print("-- Full line comments found: {:d}".format(self.Nfulcom))
        print("-- Traits recorded: {:d}".format(self.Ntraits))
        print("-- Triggers recorded: {:d}".format(self.Ntriggers))
        edct.close()

    ### Filters    
    def affects_traits(self, trait):
        if((not self.Ntraits) or (not self.Ntriggers)):
            return {}
        affects = {}
        
        for trig in self.triggers:
            hasit = False
            for cond in trig.conditions:
                if(trait in cond):
                    hasit = True
                    break
            if(hasit):
                for aff in trig.affects:
                    affects.setdefault(aff.aff, []).append(trig.name)
        return affects
        
    def is_affected_traits(self, trait):
        if((not self.Ntraits) or (not self.Ntriggers)):
            return {}
        affected = {}
        
        for trig in self.triggers:
            hasit = False
            for aff in trig.affects:
                if(trait in aff.aff):
                    hasit = True
                    break
            if(hasit):
                for cond in trig.conditions:
                    lcond = cond.split()
                    if(lcond[0] == "Trait"):
                        affected.setdefault(lcond[1], []).append(trig.name)
        return affected
            
    def get_trait(self, name):
        try:
            it = self.traits.names.index(name)
            return self.traits[it]
        except ValueError:
            print("ERROR: not present")

    def reload(self):
        if(not self.edct_file):
            print("ERROR: file not specified")
            return
        if(not os.path.isfile(self.edct_file)):
            print("ERROR: file not found")
            return
        self.parse_edct(self.edct_file)

    def save(self, fname):
        f = open(fname, "w")
        f.write(self.comment_header)
        for tt in edcteb2.traits:
            f.write(tt.as_string())
        for tt in edcteb2.triggers:
            f.write(tt.as_string())
        f.close()
            
        
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
        if(EDCT.fulcom_re.match(l)):
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
            incom_ma = EDCT.incom_re.match(l) 
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
                if(not EDCT.trigg_re.match(l)):
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
        self.effects = strlist()

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
        
class Trigger():
    def __init__(self, name, incom=None):
        self.name = name         
        self.when = None            # required
        self.conditions = strlist()         
        self.affects = strlist()    # required (only in edct), maximum 9
        
        self.comment_head = ''
        self.comment_dict = {}        
        if(incom): self.comment_dict["Trigger"] = incom
       
    def parse_line(self, l):
        if(EDCT.fulcom_re.match(l)):
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
            incom_ma = EDCT.incom_re.match(l) 
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
            if(not EDCT.trait_re.match(l)):
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
        base = "Trigger {:s}".format(self.name) + self.comment_dict.get("Trigger", "")  + "\n"
        base = base + "  WhenToTest {:s}".format(self.when) + "\n\n"
        
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
        else: self.inline_comment = ''
        self.fullline_comment = ""

    def __repr__(self):
        return "\tAffects {:s} {:g} Chance {:g}\n".format(self.aff, self.val, self.chance)
    
    def as_string(self):
        base = "  Affects {:s}  {:d}  Chance  {:d}".format(self.aff, self.val, self.chance) + self.inline_comment + "\n"
        base = base + self.fullline_comment
        return base
        
if __name__ == "__main__":
    edcteb2 = EDCT()
    edcteb2.parse_edct(edcteb2.EDCT_fname)
    #print(edcteb2.traits[0].comment_head)
    for tt in edcteb2.triggers:
        for x in tt.comment_dict.items():
            if(x[0].startswith("a")):
                #print(x)
                pass
        #print(tt.comment_dict, end='')
        #print(tt.as_string())
    #for tt in edcteb2.triggers:
        #print(tt.name)
    #    print(tt.comment_head, end='')
    #    print(tt.as_string())
    edcteb2.save("test.txt")
        #print(edcteb2.traits)
    #print(edcteb2.triggers[0]) #.as_string())
