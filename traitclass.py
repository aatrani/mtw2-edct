import re
import os
from reprlib import recursive_repr

def strip_comments(line):
    #code = str(code)
    return re.sub(';.*', '', line)
    
comment_re = re.compile("^\s*;|^\s*$")
trait_re = re.compile("^\s*Trait\s+(\S+)")
trigg_re = re.compile("^\s*Trigger\s+(\S+)")

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

    def __init__(self):
        self.Nskipped = 0
        self.Ntriggers = 0
        self.Ntraits = 0
        self.traits = strlist()
        self.triggers = strlist()
        self.current_view = None
        self.edct_file = None
        
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
            if(comment_re.match(l)):
                self.Nskipped+=1
                continue
            l = strip_comments(l)
            #print(l,  end='')
            
            trait_ma = trait_re.match(l)
            
            if(trait_ma):
                parseTrait = True
                parseTrigg = False
                self.Ntraits+=1
                #if(self.Ntraits>10):
                    #break
                newtrait = Trait(trait_ma.group(1))
                self.traits.append(newtrait)
                continue
                
            if(parseTrait):
                ltrait = l.replace(",", "").split() 
                if(ltrait[0] == "Characters"):
                    for charac in ltrait[1:]:
                        newtrait.characters.append(charac)
                elif(ltrait[0] == "ExcludeCultures"):
                    for exclu in ltrait[1:]:
                        newtrait.exclude.append(exclu)
                elif(ltrait[0] == "AntiTraits"):
                    for ant in ltrait[1:]:
                        newtrait.anti.append(ant)
                elif(ltrait[0] == "NoGoingBackLevel"):
                    newtrait.nogoingback = int(ltrait[1])
                elif(ltrait[0] == "Hidden"):
                    newtrait.hidden = True
                    
                elif(ltrait[0] == "Level"):
                    newlev = TraitLevel(ltrait[1])
                    newtrait.levels.append(newlev)
                elif(ltrait[0] == "Description"):
                    newlev.description = ltrait[1]
                elif(ltrait[0] == "EffectsDescription"):
                    newlev.effdecription = ltrait[1]
                elif(ltrait[0] == "GainMessage"):
                    newlev.gainmessage = ltrait[1]
                elif(ltrait[0] == "LoseMessage"):
                    newlev.losemessage = ltrait[1]
                elif(ltrait[0] == "Epithet"):
                    newlev.epith = ltrait[1]
                elif(ltrait[0] == "Threshold"):
                    newlev.threshold = int(ltrait[1])
                elif(ltrait[0] == "Effect"):
                    neweff = TraitLevelEffect(ltrait[1], int(ltrait[2]))
                    newlev.effects.append(neweff)
                else:
                    if(not trigg_re.match(l)):
                        raise ValueError(l+" not recognized by the parser")
            
            trigg_ma = trigg_re.match(l)
            if(trigg_ma):
                parseTrait = False
                parseTrigg = True
                self.Ntriggers+=1
                #if(self.Ntriggers >1): print(newtrigg)
                newtrigg = Trigger(trigg_ma.group(1))
                self.triggers.append(newtrigg)
                continue
                
            if(parseTrigg):
                ltrigg = l.replace(",", "").split() 
                if(ltrigg[0] == "WhenToTest"):
                    newtrigg.when = ltrigg[1]
                
                elif(ltrigg[0] == "Condition"):
                    newtrigg.conditions.append(" ".join(ltrigg[1:]))
                elif(ltrigg[0] == "and"):
                    newtrigg.conditions.append(" ".join(ltrigg[1:]))
                elif(ltrigg[0] == "Affects"):
                    newaff = TriggerAffect(ltrigg[1], int(ltrigg[2]), int(ltrigg[4]))
                    newtrigg.affects.append(newaff)             
                else:
                    if(not trait_re.match(l)):
                        raise ValueError(l+" not recognized by the parser")
        
        self.update_names()
        print("-- Lines skipped: {:g}".format(self.Nskipped))
        print("-- Traits recorded: {:g}".format(self.Ntraits))
        print("-- Triggers recorded: {:g}".format(self.Ntriggers))
        edct.close()
        
    def affects(self, trait):
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
        
    def is_affected(self, trait):
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

class Trait():
    def __init__(self, name):
        self.name = name            # required
        self.characters = []        # required
        self.hidden = False
        self.exclude = []
        self.nogoingback = None
        self.anti = []
        self.levels = strlist()     # required

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
        base = "Trait {:s}".format(self.name) + "\n"
        base = base + "    Characters "+", ".join(self.characters) + "\n"
        if(self.hidden):
            base = base + "    Hidden" + "\n"
        if(self.exclude):
            base = base + "    ExcludeCultures "+", ".join(self.exclude) + "\n"
        if(self.nogoingback):
            base = base + "    NoGoingBackLevel {:d}".format(self.nogoingback) + "\n"   
        if(self.anti):
            base = base + "    AntiTraits "+", ".join(self.anti) + "\n"
        
        for lev in self.levels:
            base = base + lev.as_string()
        return base
    
class TraitLevel():
    def __init__(self, name):
        self.name = name
        self.description = None    # required
        self.effdecription = None  # required
        self.threshold = None      # required
        self.gainmessage = None
        self.losemessage = None
        self.epith = None
        self.effects = strlist()
    
    @recursive_repr()
    def __repr__(self):
        base = "\tLevel " + self.name + "\n"
        base = base + "\t\tThreshold {:g}\n".format(self.threshold)
        if(self.effects):
            base = base + "".join(map(repr, self.effects))
        return base
        
    def as_string(self):
        base = "    Level " + self.name + "\n"
        base = base + "        Description " + self.description + "\n"  
        base = base + "        EffectsDescription " + self.effdecription + "\n" 
        if(self.gainmessage):
            base = base + "        GainMessage " + self.gainmessage + "\n"
        if(self.losemessage):
            base = base + "        LoseMessage " + self.losemessage + "\n"
        if(self.epith):
            base = base + "        Epithet " + self.epith + "\n"
        base = base + "        Threshold {:d}".format(self.threshold) + "\n"
        
        for eff in self.effects:
            base = base + eff.as_string()
        return base
    
class TraitLevelEffect():
    def __init__(self, eff, numb):
        self.eff = eff
        self.val = int(numb)
    
    def __repr__(self):
        return "\t\t{:s} {:g}\n".format(self.eff, self.val)
    
    def as_string(self):
        return "        {:s} {:d}".format(self.eff, self.val) + "\n"
        
class Trigger():
    def __init__(self, name):
        self.name = name
        self.when = None
        self.conditions = []
        self.affects = strlist()
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

class TriggerAffect():
    def __init__(self, aff, numb, chanc):
        self.aff = aff
        self.val = int(numb)
        self.chance = int(chanc)
    def __repr__(self):
        return "\tAffects {:s} {:g} Chance {:g}\n".format(self.aff, self.val, self.chance)

if __name__ == "__main__":
    edcteb2 = EDCT()
    edcteb2.parse_edct(edcteb2.EDCT_fname)
    print(edcteb2.traits)
    print(edcteb2.traits[0].as_string())
